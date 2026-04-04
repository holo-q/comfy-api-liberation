"""
API key configuration management.

Providers can resolve credentials from either:
1. A locally stored key value managed by the liberation UI.
2. A `pass` entry path whose secret is maintained outside ComfyUI via CLI.
"""
import json
import logging
import shutil
import subprocess
from pathlib import Path
from threading import Lock
from typing import Literal, TypedDict

log = logging.getLogger("comfy-api-liberation")

_CONFIG_PATH = Path(__file__).parent / "api_keys.json"
_cache_lock = Lock()
_loaded = False


class KeyEntry(TypedDict):
    source: Literal["local", "pass"]
    value: str


_keys_cache: dict[str, KeyEntry] = {}

# All supported providers — derived from the single source of truth
# in mappings.PROVIDER_REGISTRY. Do NOT hardcode providers here.
from .mappings import PROVIDERS


def _normalize_entry(value) -> KeyEntry | None:
    """
    Normalize on-disk config values.

    Older liberation versions stored raw strings directly. We transparently
    upgrade those to the structured local-source format on load.
    """
    if isinstance(value, str):
        return {"source": "local", "value": value}

    if not isinstance(value, dict):
        return None

    source = value.get("source")
    stored_value = value.get("value")
    if source not in {"local", "pass"} or not isinstance(stored_value, str) or not stored_value.strip():
        return None

    return {"source": source, "value": stored_value.strip()}


def is_pass_available() -> bool:
    return shutil.which("pass") is not None


def _resolve_pass_key(pass_path: str) -> str | None:
    if not is_pass_available():
        log.warning("`pass` is not available while resolving %s", pass_path)
        return None

    try:
        result = subprocess.run(
            ["pass", "show", pass_path],
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        )
    except Exception as e:
        log.warning("Failed to run `pass show %s`: %s", pass_path, e)
        return None

    if result.returncode != 0:
        stderr = (result.stderr or "").strip()
        log.warning("`pass show %s` failed: %s", pass_path, stderr or f"exit {result.returncode}")
        return None

    first_line = next((line.strip() for line in result.stdout.splitlines() if line.strip()), "")
    return first_line or None


def _load_config():
    """Load config from JSON file if not already loaded."""
    global _loaded
    with _cache_lock:
        if _loaded:
            return
        if _CONFIG_PATH.exists():
            try:
                data = json.loads(_CONFIG_PATH.read_text())
                if isinstance(data, dict):
                    for provider, raw_value in data.items():
                        entry = _normalize_entry(raw_value)
                        if entry:
                            _keys_cache[provider] = entry
                log.info(f"Loaded {len(_keys_cache)} API key entries from config")
            except Exception as e:
                log.warning(f"Failed to load config: {e}")
        _loaded = True


def _save_config():
    """Save current keys cache to JSON file."""
    with _cache_lock:
        try:
            _CONFIG_PATH.write_text(json.dumps(_keys_cache, indent=2))
        except Exception as e:
            log.error(f"Failed to save config: {e}")


def get_api_key(provider: str) -> str | None:
    """Resolve the actual API key for a provider."""
    _load_config()
    with _cache_lock:
        entry = _keys_cache.get(provider)

    if not entry:
        return None
    if entry["source"] == "pass":
        return _resolve_pass_key(entry["value"])
    return entry["value"]


def set_api_key(provider: str, key: str):
    """Store a local API key for a provider."""
    _load_config()
    normalized_key = key.strip()
    with _cache_lock:
        _keys_cache[provider] = {"source": "local", "value": normalized_key}
    _save_config()
    log.info("Local API key set for %s", provider)


def set_pass_path(provider: str, pass_path: str):
    """Store a `pass` entry path for a provider."""
    _load_config()
    normalized_path = pass_path.strip()
    with _cache_lock:
        _keys_cache[provider] = {"source": "pass", "value": normalized_path}
    _save_config()
    log.info("Pass path set for %s: %s", provider, normalized_path)


def delete_api_key(provider: str):
    """Delete API key for a provider."""
    _load_config()
    with _cache_lock:
        _keys_cache.pop(provider, None)
    _save_config()
    log.info(f"API key deleted for {provider}")


def get_key_entry(provider: str) -> KeyEntry | None:
    """Return the stored key source metadata without exposing local secrets."""
    _load_config()
    with _cache_lock:
        entry = _keys_cache.get(provider)
        if not entry:
            return None
        return dict(entry)


def get_all_key_status() -> dict[str, dict]:
    """
    Get status of all providers (configured or not).
    Returns UI-safe source metadata without exposing local secrets.
    """
    _load_config()
    result = {}

    for provider in PROVIDERS:
        entry = get_key_entry(provider)
        if not entry:
            result[provider] = {
                "configured": False,
                "source": None,
                "pass_path": None,
            }
            continue

        result[provider] = {
            "configured": True,
            "source": entry["source"],
            "pass_path": entry["value"] if entry["source"] == "pass" else None,
        }

    return result
