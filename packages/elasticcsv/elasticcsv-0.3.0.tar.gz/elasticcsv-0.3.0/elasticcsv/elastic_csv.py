import csv
import logging
import math
import re
from datetime import datetime, date
from enum import Enum
from typing import Iterator, List, Dict, Generator, Any

import pandas as pd
import pytz
from box import Box
from pandas import DataFrame
from toolz import pipe, curry, identity
from tqdm import tqdm

from elasticcsv.elastic_wrapper import ElasticWrapper

logger = logging.getLogger(__name__)

DEFAULT_CSV_WRITE_CHUNK_SIZE = 50000


class FileMode(str, Enum):
    a = "a"
    w = "w"


def download_csv(
    config: Box, csv_file_name: str, index: str, delimiter: str, file_mode: FileMode = FileMode.a
) -> int:
    """Main process to load csv to elastic

    :param file_mode: Open mode for CSV file (a: append, w: write), write mode resets file before write
    :param config: Dictionary with elasctic connection data
    :param csv_file_name: csv file path
    :param index: index name (_index)
    :param delimiter: csv delimiter
    """
    e_wrapper = ElasticWrapper(config.elastic_connection)
    es_iterator = e_wrapper.scan(index=index)
    regs: int = _write_csv(
        es_iterator, csv_file_name=csv_file_name, delimiter=delimiter, file_mode=file_mode
    )
    return regs


def load_csv(
    config: Box,
    csv_file_name: str,
    index: str,
    delimiter: str,
    csv_date_format: str = None,
    logic_date: date = date.today(),
    csv_offset: int = 0,
    dict_columns: List[str] = None,
):
    """Main process to load csv to elastic
    :param csv_offset:
    :param dict_columns:
    :param config: Dictionary with elasctic connection data
    :param csv_file_name: csv file path
    :param index: index name (_index)
    :param delimiter: csv delimiter
    :param csv_date_format: date format spec as '%Y-%m-%d'
    :param logic_date:
    """
    parent_data: bool = config.elastic_index.data_format.parent_data_object
    csv_iterator = _csv_reader(
        filepath=csv_file_name,
        delimiter=delimiter,
        logic_date=logic_date,
        transform_to_data=parent_data,
        count_lines=True,
        csv_date_format=csv_date_format,
        csv_offset=csv_offset,
        dict_columns=dict_columns,
    )
    e_wrapper = ElasticWrapper(config.elastic_connection)
    return e_wrapper.bulk_dataset(data_iterator=csv_iterator, index=index)


def delete_index(config: Box, index: str) -> bool:
    e_wrapper = ElasticWrapper(config.elastic_connection)
    return e_wrapper.delete_index(index=index)


def _csv_reader(
    filepath: str,
    delimiter: str = None,
    chunk_size: int = 10000,
    logic_date: date = date.today(),
    transform_to_data: bool = True,
    count_lines: bool = False,
    csv_date_format: str = None,
    csv_offset: int = 0,
    dict_columns: List[str] = None,
) -> Generator[dict, None, None]:
    """Returns an iterator of dicts

    :param filepath:
    :param delimiter:
    :param chunk_size:
    :param logic_date:
    :param transform_to_data:
    :param count_lines: file line count before iteration process
    :return:
    """
    logger.debug(f"Loading generator for filename: {filepath}")
    tz = pytz.timezone("Europe/Madrid")
    ts = tz.localize(datetime.now(tz=tz)).isoformat()
    date_str = tz.localize(datetime.combine(logic_date, datetime.min.time())).isoformat()

    total_chunks = _count_chunks(chunk_size, csv_offset, filepath) if count_lines else None

    skip = range(1, csv_offset + 1) if csv_offset != 0 else None
    df_chunks = pd.read_csv(
        filepath_or_buffer=filepath,
        delimiter=delimiter,
        names=None,
        header=0,
        chunksize=chunk_size,
        iterator=True,
        encoding="utf-8",
        skiprows=skip,
    )

    for chunk in tqdm(df_chunks, unit=f" ({chunk_size} lines group)", total=total_chunks):
        if "" in chunk.columns:
            chunk.drop([""], axis=1, inplace=True)
        chunk.dropna(axis=1, how="all", inplace=True)
        chunk.fillna("", inplace=True)
        chunk["@timestamp"] = ts
        chunk["date"] = date_str
        chunk = chunk.astype(str)

        if csv_date_format:
            _format_date_columns(chunk, csv_date_format)
        if dict_columns:
            _eval_dict_columns(chunk, dict_columns)

        for d in chunk.to_dict("records"):
            if transform_to_data:
                d = {
                    k: value
                    for k, value in d.items()
                    if isinstance(value, str) or isinstance(value, dict)
                }
                yield _transform_to_data_struct(d)
            else:
                yield d


def _write_csv(
    es_iterator: Iterator[dict],
    csv_file_name: str,
    delimiter: str,
    file_mode: FileMode,
    chunk_size: int = DEFAULT_CSV_WRITE_CHUNK_SIZE,
    encoding: str = "utf-8",
) -> int:
    """

    :param es_iterator: elastic iterator returning hits
    :param csv_file_name: file to append hits as csv rows
    :param file_mode: File open mode (a, w)
    :param encoding:
    :param chunk_size:

    :return: Total registers
    """
    total_registers = 0
    data = True
    first_chunk = True
    while data:
        dicts: List[dict] = []
        i = 0
        for i, hit in tqdm(
            enumerate(es_iterator),
            desc=f"Download chunk of hits ({DEFAULT_CSV_WRITE_CHUNK_SIZE})",
            unit=" hit",
        ):
            # ! hit.get("_source")
            dicts.append(hit.get("_source"))
            if i >= chunk_size:
                break
            i += 1
        if i < chunk_size:
            data = False

        if not dicts:
            logger.debug(f"Nothing to write to csv_filename: {csv_file_name}")
        else:
            # flatten dict values (only one level) as key1.key11: value11
            if any([isinstance(value, dict) for value in list(dicts[0].values())]):
                dicts = list(map(_flatten_dict, dicts))

            with open(csv_file_name, file_mode, encoding=encoding, newline="") as f:
                headers = list((dicts[0].keys()))
                writer = csv.DictWriter(
                    f, fieldnames=headers, delimiter=delimiter, extrasaction="ignore"
                )
                if first_chunk:
                    writer.writeheader()
                writer.writerows(dicts)
                total_registers += len(dicts)
            first_chunk = False
            # * Second chunk has to be append, avoiding "w" config
            file_mode = "a"
    return total_registers


def _pipe_csv_reader(
    filepath: str,
    delimiter: str = None,
    chunk_size: int = 10000,
    logic_date: date = date.today(),
    transform_to_data: bool = True,
    count_lines: bool = False,
    csv_date_format: str = None,
    csv_offset: int = 0,
    dict_columns: List[str] = None,
) -> Generator[dict, None, None]:
    """Returns an iterator of dicts

    :param filepath: filepath to csv
    :param delimiter: delimiter of csv columns
    :param chunk_size: chunk size for reading csv
    :param logic_date: date of logic
    :param transform_to_data: whether transform to data struct or not
    :param count_lines: wether to count file line or not (default False)
    :param csv_date_format: date format for csv columns
    :param csv_offset: offset of csv

    :return:
    """
    logger.debug(f"Loading generator for filename: {filepath}")

    total_chunks = _count_chunks(chunk_size, csv_offset, filepath) if count_lines else None

    skip = range(1, csv_offset + 1) if csv_offset != 0 else None
    # * Read csv by dataframe chunks
    df_chunks = pd.read_csv(
        filepath_or_buffer=filepath,
        delimiter=delimiter,
        names=None,
        header=0,
        chunksize=chunk_size,
        iterator=True,
        encoding="utf-8",
        skiprows=skip,
    )
    tz = pytz.timezone("Europe/Madrid")
    ts = tz.localize(datetime.now(tz=tz)).isoformat()
    date_str = tz.localize(datetime.combine(logic_date, datetime.min.time())).isoformat()
    # * curried functions pipeline construction
    # * df_chunks > _prepare_chunks | _format_chunk_date_columns |
    # * _eval_chunk_dict_columns | _df_chunk_to_dict_list
    # * Return generator as result of last function of pipe line
    return pipe(
        df_chunks,  # data in
        [  # four functions
            curry(_prepare_chunks)(ts=ts, date_str=date_str),
            curry(_format_chunk_date_columns)(csv_date_format=csv_date_format)
            if csv_date_format
            else identity,
            curry(_eval_chunk_dict_columns)(dict_columns=dict_columns)
            if dict_columns
            else identity,
            curry(_df_chunk_to_dict_list)(
                transform_to_data=transform_to_data, total_chunks=total_chunks
            ),
        ],
    )


def _pipe_write_csv(
    es_gen: Generator[dict, None, None],
    csv_file_name: str,
    delimiter: str,
    file_mode: FileMode,
    chunk_size: int = DEFAULT_CSV_WRITE_CHUNK_SIZE,
    encoding: str = "utf-8",
) -> int:
    """

    :param es_gen: elastic generator returning hits
    :param csv_file_name: file to append hits as csv rows
    :param file_mode: File open mode (a, w)
    :param encoding:
    :param chunk_size:

    :return: Total registers
    """
    # * curried functions and pipe line construction
    # * es_gen > _get_data_chunks | _flatten_data_chunks | _save_to_file_data_chunks
    pipe_funcs = [
        curry(_get_data_chunks)(chunk_size=chunk_size),
        _flatten_data_chunks,  # no need to curry
        curry(_save_to_file_data_chunks)(
            encoding=encoding, delimiter=delimiter, csv_file_name=csv_file_name, file_mode=file_mode
        ),
    ]

    # * Return result from last function of pipe line (total_registers)
    return pipe(es_gen, *pipe_funcs)


def _count_chunks(chunk_size, csv_offset, filepath):
    total_lines = _count_lines(filepath) if csv_offset == 0 else _count_lines(filepath) - csv_offset
    total_chunks = math.ceil(total_lines / chunk_size)
    return total_chunks


def _get_data_chunks(
    regs_gen: Generator[dict, None, None], chunk_size: int
) -> Generator[List[dict], None, None]:
    """Get data from dict generator in chunks of size chunk_size

    :param regs_gen:
    :param chunk_size:
    :return:
    """
    # Group dicts into chunks of size chunk_size
    chunk = []
    try:
        while True:
            for _ in range(chunk_size):
                chunk.append(next(regs_gen).get("_source"))
            yield chunk
            chunk = []
    except StopIteration:
        if chunk:
            yield chunk


def _flatten_data_chunks(
    chunk_gen: Generator[List[dict], None, None]
) -> Generator[List[dict], None, None]:
    for dicts in chunk_gen:
        if any([isinstance(value, dict) for value in list(dicts[0].values())]):
            yield list(map(_flatten_dict, dicts))
        else:
            yield dicts


def _save_to_file_data_chunks(
    chunk_gen: Generator[List[dict], None, None],
    csv_file_name: str,
    encoding: str,
    delimiter: str,
    file_mode: FileMode,
) -> int:
    """Save data from dict generator in chunks of size chunk_size

    :param chunk_gen:
    :param csv_file_name:
    :param encoding:
    :param delimiter:
    :return: Total number of registers
    """
    with open(csv_file_name, file_mode, encoding=encoding, newline="") as f:
        first_chunk = True
        total_regs = 0
        progress = tqdm(unit=" registers", desc="Saving registers to csv file")
        for dicts in chunk_gen:
            headers = list((dicts[0].keys()))
            writer = csv.DictWriter(
                f, fieldnames=headers, delimiter=delimiter, extrasaction="ignore"
            )
            if first_chunk:
                writer.writeheader()
                first_chunk = False
            writer.writerows(dicts)
            total_regs += len(dicts)
            progress.update(len(dicts))

    return total_regs


def _prepare_chunks(
    chunk_gen: Generator[DataFrame, None, None], ts: str, date_str: str
) -> Generator[DataFrame, None, None]:
    # Group dicts into chunks of size chunk_size
    for chunk in chunk_gen:
        if "" in chunk.columns:
            chunk.drop([""], axis=1, inplace=True)
        chunk.dropna(axis=1, how="all", inplace=True)
        chunk.fillna("", inplace=True)
        chunk["@timestamp"] = ts
        chunk["date"] = date_str
        chunk = chunk.astype(str)
        yield chunk


def _format_chunk_date_columns(
    chunk_gen: Generator[DataFrame, None, None], csv_date_format: str
) -> Generator[DataFrame, None, None]:
    def format_dates(d_str):
        if not d_str:
            return None
        format_d_str = datetime.strptime(d_str, csv_date_format).isoformat()
        return format_d_str

    for chunk in chunk_gen:
        date_columns = list(filter(lambda c: re.findall(f".*_date$", c), chunk.columns))
        for col in date_columns:
            chunk[col] = chunk[col].apply(format_dates)
        yield chunk


def _eval_chunk_dict_columns(
    chunk_gen: Generator[DataFrame, None, None], dict_columns: List[str]
) -> Generator[DataFrame, None, None]:
    for chunk in chunk_gen:
        for col in dict_columns:
            chunk[col] = chunk[col].apply(eval)
        yield chunk


def _df_chunk_to_dict_list(
    df_chunks: Generator[DataFrame, None, None],
    transform_to_data: bool,
    total_chunks: int = None,
) -> Generator[dict, None, None]:
    progress = tqdm(unit=" chunks", desc="loading registers chunks", total=total_chunks)

    for chunk in df_chunks:
        for d in chunk.to_dict("records"):
            if transform_to_data:
                d = {
                    k: value
                    for k, value in d.items()
                    if isinstance(value, str) or isinstance(value, dict)
                }
                yield _transform_to_data_struct(d)
            else:
                yield d
        progress.update(1)


def _flatten_dict(dct: dict) -> dict:
    new_fields = {}
    for k, v in list(dct.items()):
        if isinstance(v, dict):
            for kk, vv in list(v.items()):
                new_fields[".".join([k, kk])] = vv
        else:
            new_fields[k] = v
    return new_fields


def _transform_to_data_struct(reg: Dict[str, str]) -> Dict[str, Any]:
    data = copy_elastic_properties(reg, system=False)
    props = copy_elastic_properties(reg, system=True)
    new_reg = {"data": data}
    new_reg.update(**props)
    return new_reg


def copy_elastic_properties(registro: Dict[str, str], system: bool) -> Dict[str, str]:
    if not system:
        keys = list(
            filter(
                lambda k: k[0] not in ["_", "@"] and k not in ["date"],
                list(registro.keys()),
            )
        )
    else:
        keys = list(filter(lambda k: k[0] in ["_", "@"] or k in ["date"], list(registro.keys())))
    new_reg: Dict[str, str] = {
        k: registro[k]
        for k in keys
        if isinstance(registro[k], str)
        or isinstance(registro[k], int)
        or isinstance(registro[k], float)
        or isinstance(registro[k], dict)
    }
    return new_reg


def _count_generator(raw_reader: callable) -> Generator[bytes, None, None]:
    b = raw_reader(1024 * 1024)
    while b:
        yield b
        b = raw_reader(1024 * 1024)


def _count_lines(filepath: str) -> int:
    """count lines of `filepath` file with good performance

    :param filepath:
    :return: Number of lines
    """
    with open(filepath, mode="rb") as f:
        # noinspection PyUnresolvedReferences
        generator = _count_generator(f.raw.read)
        count = sum(buffer.count(b"\n") for buffer in generator)
        return count


def _format_date_columns(chunk: DataFrame, csv_date_format: str):
    def format_dates(d_str):
        if not d_str:
            return None
        format_d_str = datetime.strptime(d_str, csv_date_format).isoformat()
        return format_d_str

    date_columns = list(filter(lambda c: re.findall(f".*_date$", c), chunk.columns))
    for col in date_columns:
        chunk[col] = chunk[col].apply(format_dates)


def _eval_dict_columns(chunk: pd.DataFrame, dict_columns: List[str]):
    for col in dict_columns:
        chunk[col] = chunk[col].apply(eval)
