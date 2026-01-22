"""
Request router - rewrites /proxy/* paths to direct vendor URLs.
"""
from contextvars import ContextVar
import re
import logging
from dataclasses import replace
from typing import Any, Callable

# Import at module level to avoid hot-reload issues with relative imports
from . import mappings
from . import config
from .asset_vault import vault
from comfy_api_nodes.util.client import ApiEndpoint

log = logging.getLogger("comfy-api-liberation")

# Optional: handle Pydantic URL types (v2 AnyUrl isn't a `str`)
try:
    from pydantic.networks import AnyUrl as _PydanticAnyUrl  # type: ignore
except Exception:  # pragma: no cover
    _PydanticAnyUrl = None

# Track unmapped endpoints we've seen (log once per unique path)
_seen_unmapped: set[str] = set()

# Store per-request state using ContextVars (safe with concurrent async requests)
_pending_response_transform: ContextVar[Callable | None] = ContextVar(
    "liberation_pending_response_transform",
    default=None,
)
_current_provider: ContextVar[str | None] = ContextVar("liberation_current_provider", default=None)


def get_pending_response_transform() -> Callable | None:
    """Get and clear the pending response transform."""
    transform = _pending_response_transform.get()
    _pending_response_transform.set(None)
    return transform


def get_current_provider() -> str | None:
    return _current_provider.get()


def _materialize_asset_uris_as_data_urls(obj: Any) -> Any:
    """
    Replace `liberation://asset/<id>` URIs with `data:<mime>;base64,...` URLs.

    This is a generic compatibility mode for providers that accept image/video/document URLs
    but can't fetch local assets. Provider-specific transforms can override this with a more
    idiomatic integration (multipart, vendor uploads, etc.).
    """
    if isinstance(obj, dict):
        for k, v in list(obj.items()):
            obj[k] = _materialize_asset_uris_as_data_urls(v)
        return obj

    if isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = _materialize_asset_uris_as_data_urls(obj[i])
        return obj

    is_pydantic_url = _PydanticAnyUrl is not None and isinstance(obj, _PydanticAnyUrl)
    if isinstance(obj, str) or is_pydantic_url:
        s = str(obj)
        asset_id = vault.parse_asset_uri(s)
        if asset_id:
            return vault.to_data_url(asset_id)
        # Ensure JSON-serializable output for AnyUrl values.
        return s if is_pydantic_url else obj

    return obj


def rewrite_request(cfg: Any) -> Any:
    """
    Rewrite request config if path matches a known proxy endpoint.

    Args:
        cfg: _RequestConfig from client.py

    Returns:
        Modified cfg with absolute vendor URL and auth headers, or original cfg
    """
    path = cfg.endpoint.path

    # Only process /proxy/* paths
    if not path.startswith("/proxy/"):
        _current_provider.set(None)
        _pending_response_transform.set(None)
        return cfg

    log.debug(f"[liberation] Intercepted: {path}")

    _pending_response_transform.set(None)  # Reset for this request
    _current_provider.set(None)

    # Try each mapping pattern
    for pattern, mapping in mappings.ENDPOINT_MAP.items():
        match = re.match(pattern, path)
        if match:
            provider = mapping['provider']
            _current_provider.set(provider)
            key = config.get_api_key(provider)

            if not key:
                # No key configured - return special error that frontend will intercept
                log.warning(f"[liberation] NO API KEY for '{provider}' - blocking request")
                # Use a structured error message the frontend can parse
                raise Exception(
                    f"LIBERATION_MISSING_KEY:{provider}:API key required for '{provider}'. "
                    f"Configure your {provider.upper()} API key to use this node directly."
                )

            # Build new absolute URL from template
            groups = match.groups()
            new_url = mapping['url_template'].format(*groups)

            # Get auth headers
            auth_headers = mapping['auth_fn'](key)

            # Apply request transform if defined
            new_data = cfg.data
            if mapping.get('request_transform'):
                try:
                    new_data = mapping['request_transform'](cfg.data)
                except Exception as e:
                    log.warning(f"Request transform failed for {provider}: {e}")

            # Generic asset materialization: convert asset URIs to data URLs.
            # Google is handled with a provider-specific inlineData transform.
            if provider != "google":
                try:
                    new_data = _materialize_asset_uris_as_data_urls(new_data)
                except Exception as e:
                    log.warning(f"Asset materialization failed for {provider}: {e}")

            # Store response transform for later application
            if mapping.get('response_transform'):
                _pending_response_transform.set(mapping['response_transform'])

            # Create new endpoint with absolute URL and merged headers
            new_headers = {**(cfg.endpoint.headers or {}), **auth_headers}

            new_endpoint = ApiEndpoint(
                path=new_url,
                method=cfg.endpoint.method,
                query_params=cfg.endpoint.query_params,
                headers=new_headers,
            )

            log.info(f"[liberation] {path} → {new_url}")
            return replace(cfg, endpoint=new_endpoint, data=new_data)

    # No mapping found - log once per unique path pattern
    if path not in _seen_unmapped:
        _seen_unmapped.add(path)
        log.debug(f"[liberation] Unmapped proxy: {path} - using Comfy proxy")

    return cfg
