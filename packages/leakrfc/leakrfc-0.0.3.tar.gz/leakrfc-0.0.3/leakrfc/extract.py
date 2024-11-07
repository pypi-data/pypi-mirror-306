"""
Extract source packages during archiving (crawl or make stage)
using ingest-file
"""

from pathlib import Path
from anystore.util import get_extension
from nomenklatura.entity import CE
from importlib.metadata import entry_points
from ingestors.exc import ProcessingException
from pantomime.mime import normalize_mimetype

from leakrfc.logging import get_logger
from leakrfc.util import guess_mimetype, make_file_proxy

log = get_logger(__name__)


EXTRACTORS = {
    e.name: e.load()
    for e in entry_points(group="ingestors")
    if e.value.startswith("ingestors.packages")
}

EXTENSIONS = [i for e in EXTRACTORS.values() for i in e.EXTENSIONS]
MIME_TYPES = [i for e in EXTRACTORS.values() for i in e.MIME_TYPES]


def auction_extractor(fp: Path, proxy: CE | None = None):
    best_score, best_cls = 0, None
    entity = proxy or make_file_proxy(fp)
    for cls in EXTRACTORS.values():
        score = cls.match(fp, entity)
        if score > best_score:
            best_score = score
            best_cls = cls

    if best_cls is None:
        raise ProcessingException("Format not supported")
    return best_cls


def is_package(fp: str) -> bool:
    if get_extension(fp) in EXTENSIONS:
        return True
    return guess_mimetype(fp) in MIME_TYPES


def is_package_mtype(mtype: str) -> bool:
    return normalize_mimetype(mtype) in MIME_TYPES
