import logging
import time
from typing import Iterator, Literal, Generator, Type

from box import Box
from elastic_transport import RequestsHttpNode, NodeConfig, TransportError
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError, ApiError
from elasticsearch.helpers import streaming_bulk, scan
from tqdm import tqdm
from yarl import URL

logger = logging.getLogger(__name__)


class MyRequestsHttpNode(RequestsHttpNode):
    proxies = {}

    def __init__(self, config: NodeConfig):
        super(MyRequestsHttpNode, self).__init__(config=config)

        self.session.proxies = self.proxies.copy()
        self.session.trust_env = False

    @classmethod
    def get_proxified_class(cls, proxies: dict) -> Type["MyRequestsHttpNode"]:
        cls.proxies = proxies
        return cls


class ElasticWrapper(object):
    """Wrapper for Elasticsearch object"""

    ELASTICSEARCH_TIMEOUT = 120
    DEFAULT_QUERY_SIZE = 10000
    DEFAULT_QUERY_CHUNK_SIZE = 5000

    def __init__(self, conn_conf: Box):
        """ElasticWrapper

        :param conn_conf: Box instance with connection info
        """
        self._proxies = conn_conf.proxies
        self._connection = self._get_connection(conn_conf)
        logger.info("ElasticWrapper initialized")

    @classmethod
    def get_client(cls, conn_conf: Box):
        return cls(conn_conf=conn_conf)

    def __repr__(self):
        return f"<ElasticWrapper(connection={self._connection}, " f"proxies: {self._proxies})>"

    def __del__(self):
        """Close Elasticsearch connections when destroy"""
        if self._connection:
            self._connection.close()

    def _get_connection(self, conn_conf: Box) -> Elasticsearch:
        if conn_conf.apikey_secret:
            elastic_url = URL(f"{conn_conf.scheme}://{conn_conf.node}:{conn_conf.port}")
            api_key = (conn_conf.apikey_id, conn_conf.apikey_secret)
        else:
            elastic_url = (
                URL(f"{conn_conf.scheme}://{conn_conf.node}:{conn_conf.port}")
                .with_user(conn_conf.user)
                .with_password(conn_conf.password)
            )
            api_key = None

        if self._proxies:
            es = Elasticsearch(
                [str(elastic_url)],
                api_key=api_key,
                node_class=MyRequestsHttpNode.get_proxified_class(proxies=self._proxies),
                request_timeout=self.ELASTICSEARCH_TIMEOUT,
            )
        else:
            es = Elasticsearch(
                [str(elastic_url)],
                api_key=api_key,
                request_timeout=self.ELASTICSEARCH_TIMEOUT,
            )
        return es

    def delete_index(self, index: str) -> bool:
        """deletes a index

        :param index: index to be deleted
        """
        try:
            self._connection.indices.delete(index=index)
        except NotFoundError as nf:
            logger.warning(f"Index to delete {index} not found.")
            return False
        except (ApiError, TransportError) as e:
            logger.error(f"Exception while deleting index {index}: {e.args}")
            return False
        logger.info(f"Index {index} was deleted.")
        return True

    def scan(
        self,
        index: str,
        query: dict = {"match_all": {}},
        chunk_size: int = DEFAULT_QUERY_CHUNK_SIZE,
        sort_by: str = None,
        order: Literal["desc", "asc"] = "desc",
    ) -> Generator[dict, None, None]:
        """
        Retorna todos los registros del indice "index"

        :param index: Indice o alias sobre el que se va a realizar la query
        :param chunk_size: número de registros por cada petición a servidor
        :param sort_by: Field used to sort
        :param order: sort order "asc" or "desc"
        :returns: Resultado de la query (None en caso de error)
        """
        body = {"query": query}
        if sort_by:
            body["sort"] = [{sort_by: {"order": order}}]

        es_generator = scan(
            self._connection, index=index, query=body, size=chunk_size, preserve_order=True
        )
        return es_generator

    # ********
    # * BULK *
    # ********

    @staticmethod
    def _generate_actions(dataset):
        return (element for element in dataset)
        # for element in dataset:
        #     yield element

    def bulk_dataset(self, data_iterator: Iterator[dict], index: str) -> int:
        """
        Función: bulk_dataset
        Descripción: Ingesta Dataset en formato array de objetos Json en elasticsearch

        :param data_iterator: Array de documentos ha realizar bulk en elasticsearch
        (Formato: [{..},{..},...])
        :param index: indice sobre el que se van a ingestar los datos
        :returns: num docs indexed
        """
        logger.info(f"Connection to Elasticsearch : {self._connection}")
        progress = tqdm(unit="docs")
        successes = fails = 0
        action = None
        try:
            for ok, action in streaming_bulk(
                client=self._connection,
                index=index,
                actions=data_iterator,
                raise_on_exception=True,
                raise_on_error=True,
                chunk_size=1000,
                yield_ok=True,
            ):
                if ok:
                    successes += 1
                else:
                    fails += 1

                progress.update(1)
        except (ApiError, TransportError) as ee:
            logger.error(f"Action: {ee.args}, {action if action else None}")
        progress.close()
        logger.info("Documentos indexados: %d", successes)
        logger.warning(f"Documents not indexed: {fails}")
        return successes

    @staticmethod
    def _result_from_generator(es_generator: Iterator) -> dict:
        hits = []
        tick = time.perf_counter_ns()
        for element in es_generator:
            hits.append(element)

        tock = time.perf_counter_ns()
        res = {
            "took": tock - tick,
            "hits": {"hits": hits, "total": {"value": len(hits), "relation": "eq"}},
        }
        return res
