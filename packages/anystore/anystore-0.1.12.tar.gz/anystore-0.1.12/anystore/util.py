from io import BytesIO
import hashlib
from pathlib import Path
from typing import Any, BinaryIO
from urllib.parse import urljoin, urlparse, urlsplit, urlunsplit

from banal import clean_dict as _clean_dict
from banal import is_mapping


DEFAULT_HASH_ALGORITHM = "sha1"


def _clean(val: Any) -> Any:
    if val is False:
        return False
    return val or None


def clean_dict(data: Any) -> dict[str, Any]:
    """
    strip out defaultdict and ensure str keys (for serialization)
    """
    if not is_mapping(data):
        return {}
    return _clean_dict(
        {
            str(k): clean_dict(dict(v)) or None if is_mapping(v) else _clean(v)
            for k, v in data.items()
        }
    )


def ensure_uri(uri: Any) -> str:
    if not uri:
        raise ValueError(f"Invalid uri: `{uri}`")
    if uri == "-":  # stdin/stout
        return uri
    if isinstance(uri, Path):
        return uri.absolute().as_uri()
    if isinstance(uri, str) and not uri.strip():
        raise ValueError(f"Invalid uri: `{uri}`")
    uri = str(uri)
    parsed = urlparse(uri)
    if parsed.scheme:
        return uri
    return Path(uri).absolute().as_uri()


def join_uri(uri: Any, path: str) -> str:
    # FIXME wtf
    uri = ensure_uri(uri)
    if not uri or uri == "-":
        raise ValueError(f"Invalid uri: `{uri}`")
    uri += "/"
    scheme, *parts = urlsplit(uri)
    _, *parts = urlsplit(urljoin(urlunsplit(["", *parts]), path))
    return urlunsplit([scheme, *parts])


def join_relpaths(*parts: str) -> str:
    return "/".join((p.strip("/") for p in parts if p)).strip("/")


def make_checksum(io: BinaryIO, algorithm: str = DEFAULT_HASH_ALGORITHM) -> str:
    hash_ = getattr(hashlib, algorithm)()
    for chunk in iter(lambda: io.read(128 * hash_.block_size), b""):
        hash_.update(chunk)
    return hash_.hexdigest()


def make_data_checksum(data: Any, algorithm: str = DEFAULT_HASH_ALGORITHM) -> str:
    data = repr(data).encode()
    return make_checksum(BytesIO(data), algorithm)


def make_signature_key(*args, **kwargs) -> str:
    return make_data_checksum((args, kwargs))
