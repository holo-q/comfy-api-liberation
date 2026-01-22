import base64
import os
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from threading import Lock
from typing import Optional
from urllib.parse import urlparse


LIBERATION_SCHEME = "liberation"
_UPLOAD_NETLOC = "upload"
_ASSET_NETLOC = "asset"


@dataclass(frozen=True)
class AssetRecord:
    path: Path
    filename: str | None
    content_type: str | None
    size_bytes: int
    created_at: float


class AssetVault:
    """
    Local asset vault for API nodes.

    It fakes Comfy's `/customers/storage` flow by issuing an "upload URL" that is
    handled in-process (no network) and a "download URL" that is a custom URI
    scheme (`liberation://asset/<id>`). Provider-specific request transforms
    can then materialize these URIs into vendor-compatible payloads.
    """

    def __init__(self, root_dir: Path):
        self._root_dir = root_dir
        self._root_dir.mkdir(parents=True, exist_ok=True)
        self._lock = Lock()
        self._records: dict[str, AssetRecord] = {}

    def create(self, filename: str | None, content_type: str | None) -> str:
        asset_id = uuid.uuid4().hex
        safe_name = filename or f"asset_{asset_id}"
        # Avoid path traversal; keep only basename.
        safe_name = os.path.basename(safe_name)
        file_path = self._root_dir / f"{asset_id}__{safe_name}"
        record = AssetRecord(
            path=file_path,
            filename=filename,
            content_type=content_type,
            size_bytes=0,
            created_at=time.time(),
        )
        with self._lock:
            self._records[asset_id] = record
        return asset_id

    def put(self, asset_id: str, data: bytes, *, content_type: str | None = None, filename: str | None = None) -> None:
        with self._lock:
            record = self._records.get(asset_id)
        if record is None:
            raise KeyError(f"Unknown asset_id: {asset_id}")

        record.path.parent.mkdir(parents=True, exist_ok=True)
        record.path.write_bytes(data)

        new_record = AssetRecord(
            path=record.path,
            filename=filename or record.filename,
            content_type=content_type or record.content_type,
            size_bytes=len(data),
            created_at=record.created_at,
        )
        with self._lock:
            self._records[asset_id] = new_record

    def get_bytes(self, asset_id: str) -> tuple[bytes, str | None, str | None]:
        with self._lock:
            record = self._records.get(asset_id)
        if record is None:
            raise KeyError(f"Unknown asset_id: {asset_id}")
        return record.path.read_bytes(), record.content_type, record.filename

    def to_asset_uri(self, asset_id: str) -> str:
        return f"{LIBERATION_SCHEME}://{_ASSET_NETLOC}/{asset_id}"

    def to_upload_uri(self, asset_id: str) -> str:
        return f"{LIBERATION_SCHEME}://{_UPLOAD_NETLOC}/{asset_id}"

    def parse_asset_id(self, uri: str, *, netloc: str) -> Optional[str]:
        try:
            p = urlparse(uri)
        except Exception:
            return None
        if p.scheme != LIBERATION_SCHEME or p.netloc != netloc:
            return None
        asset_id = (p.path or "").lstrip("/")
        return asset_id or None

    def parse_asset_uri(self, uri: str) -> Optional[str]:
        return self.parse_asset_id(uri, netloc=_ASSET_NETLOC)

    def parse_upload_uri(self, uri: str) -> Optional[str]:
        return self.parse_asset_id(uri, netloc=_UPLOAD_NETLOC)

    def to_data_url(self, asset_id: str) -> str:
        data, content_type, _filename = self.get_bytes(asset_id)
        mime = content_type or "application/octet-stream"
        b64 = base64.b64encode(data).decode("utf-8")
        return f"data:{mime};base64,{b64}"


def _default_vault_dir() -> Path:
    # .../ComfyUI/custom_nodes/comfy-api-liberation/asset_vault.py -> .../ComfyUI
    comfy_root = Path(__file__).resolve().parents[2]
    return comfy_root / "user" / "comfy-api-liberation-assets"


vault = AssetVault(_default_vault_dir())

