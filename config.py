"""
API key configuration management.
All keys stored in JSON config file, managed via UI.
No environment variables - clean, simple, user-controlled.
"""
import json
import logging
from pathlib import Path
from threading import Lock

log = logging.getLogger("comfy-api-liberation")

_CONFIG_PATH = Path(__file__).parent / "api_keys.json"
_keys_cache: dict[str, str] = {}
_cache_lock = Lock()
_loaded = False

# All supported providers
PROVIDERS = [
    'google',
    'openai',
    'stability',
    'bfl',
    'ideogram',
    'recraft',
    'luma',
    'runway',
    'kling',
    'minimax',
    'pika',
    'tripo',
    'rodin',
    'topaz',
    'byteplus',
    'pixverse',
    'vidu',
    'moonvalley',
    'ltx',
    'wan',
]


def _load_config():
    """Load config from JSON file if not already loaded."""
    global _loaded
    with _cache_lock:
        if _loaded:
            return
        if _CONFIG_PATH.exists():
            try:
                data = json.loads(_CONFIG_PATH.read_text())
                _keys_cache.update(data)
                log.info(f"Loaded {len(data)} API keys from config")
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
    """Get API key for a provider from config."""
    _load_config()
    with _cache_lock:
        return _keys_cache.get(provider)


def set_api_key(provider: str, key: str):
    """Set API key for a provider (persists to config file)."""
    _load_config()
    with _cache_lock:
        _keys_cache[provider] = key
    _save_config()
    log.info(f"API key set for {provider}")


def delete_api_key(provider: str):
    """Delete API key for a provider."""
    _load_config()
    with _cache_lock:
        _keys_cache.pop(provider, None)
    _save_config()
    log.info(f"API key deleted for {provider}")


def get_all_key_status() -> dict[str, dict]:
    """
    Get status of all providers (configured or not).
    Returns dict like: {"google": {"configured": True, "source": "config-file"}, ...}
    """
    _load_config()
    result = {}

    for provider in PROVIDERS:
        with _cache_lock:
            has_key = bool(_keys_cache.get(provider))
        result[provider] = {
            "configured": has_key,
            "source": "config-file" if has_key else None,
        }

    return result
