"""
Monkey patches for ComfyUI's API client.

Goals:
1) Rewrite `/proxy/*` API-node requests to direct vendor URLs with vendor auth.
2) Eliminate the Comfy account dependency for asset uploads by virtualizing
   `/customers/storage` and capturing uploads into a local asset vault.
"""

from __future__ import annotations

import logging
from functools import wraps
from typing import Any, Optional
from urllib.parse import urlparse

log = logging.getLogger("comfy-api-liberation")

_patched = False
_original_request_base = None
_original_validate_or_raise = None
_original_upload_file = None


_NODE_MODULE_TO_PROVIDER: dict[str, str] = {
    "comfy_api_nodes.nodes_gemini": "google",
    "comfy_api_nodes.nodes_veo2": "google",
    "comfy_api_nodes.nodes_openai": "openai",
    "comfy_api_nodes.nodes_sora": "openai",
    "comfy_api_nodes.nodes_stability": "stability",
    "comfy_api_nodes.nodes_bfl": "bfl",
    "comfy_api_nodes.nodes_ideogram": "ideogram",
    "comfy_api_nodes.nodes_recraft": "recraft",
    "comfy_api_nodes.nodes_luma": "luma",
    "comfy_api_nodes.nodes_runway": "runway",
    "comfy_api_nodes.nodes_kling": "kling",
    "comfy_api_nodes.nodes_minimax": "minimax",
    "comfy_api_nodes.nodes_tripo": "tripo",
    "comfy_api_nodes.nodes_rodin": "rodin",
    "comfy_api_nodes.nodes_topaz": "topaz",
    # Comfy file is named `nodes_bytedance.py`, but provider config is `byteplus`.
    "comfy_api_nodes.nodes_bytedance": "byteplus",
    "comfy_api_nodes.nodes_pixverse": "pixverse",
    "comfy_api_nodes.nodes_vidu": "vidu",
    "comfy_api_nodes.nodes_moonvalley": "moonvalley",
    # Comfy file is named `nodes_ltxv.py`, but provider config is `ltx`.
    "comfy_api_nodes.nodes_ltxv": "ltx",
    "comfy_api_nodes.nodes_wan": "wan",
}


def _infer_provider(node_cls: Any) -> Optional[str]:
    mod = getattr(node_cls, "__module__", "") or ""
    return _NODE_MODULE_TO_PROVIDER.get(mod)


def is_patched() -> bool:
    return _patched


def apply_patches() -> None:
    """
    Apply monkey patches.
    Safe to call multiple times (only patches once).
    """
    global _patched, _original_request_base, _original_validate_or_raise, _original_upload_file

    if _patched:
        return

    import comfy_api_nodes.util.client as client_module
    import comfy_api_nodes.util.upload_helpers as upload_module

    from .asset_vault import vault
    from .config import get_api_key
    from .router import get_current_provider, get_pending_response_transform, rewrite_request

    _original_request_base = client_module._request_base
    _original_validate_or_raise = client_module._validate_or_raise
    _original_upload_file = upload_module.upload_file

    async def patched_upload_file(
        cls,
        upload_url: str,
        file,
        *,
        content_type: str | None = None,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        retry_backoff: float = 2.0,
        wait_label: str | None = None,
        progress_origin_ts: float | None = None,
    ) -> None:
        asset_id = vault.parse_upload_uri(upload_url)
        if not asset_id:
            return await _original_upload_file(
                cls,
                upload_url,
                file,
                content_type=content_type,
                max_retries=max_retries,
                retry_delay=retry_delay,
                retry_backoff=retry_backoff,
                wait_label=wait_label,
                progress_origin_ts=progress_origin_ts,
            )

        # Store bytes locally; no network.
        from io import BytesIO

        if isinstance(file, BytesIO):
            try:
                file.seek(0)
            except Exception:
                pass
            data = file.read()
            filename = getattr(file, "name", None)
        elif isinstance(file, str):
            with open(file, "rb") as f:
                data = f.read()
            filename = file
        else:
            raise ValueError("file must be a BytesIO or a filesystem path string")

        vault.put(asset_id, data, content_type=content_type, filename=filename)
        log.debug("[liberation] Stored asset %s (%d bytes)", asset_id, len(data))

    def patched_validate_or_raise(response_model, payload):
        response_transform = get_pending_response_transform()
        if response_transform and isinstance(payload, dict):
            try:
                payload = response_transform(payload)
            except Exception as e:
                log.debug("[liberation] Pre-validation transform error: %s", e)
        return _original_validate_or_raise(response_model, payload)

    @wraps(_original_request_base)
    async def patched_request_base(cfg, expect_binary):
        # Intercept Comfy storage allocation so nodes can "upload" without a Comfy account.
        if cfg.endpoint.path == "/customers/storage" and cfg.endpoint.method.upper() == "POST":
            provider = _infer_provider(cfg.node_cls)
            if provider and not get_api_key(provider):
                raise Exception(
                    f"LIBERATION_MISSING_KEY:{provider}:API key required for '{provider}'. "
                    f"Configure your {provider.upper()} API key to use this node directly."
                )

            req = cfg.data or {}
            filename = req.get("file_name") if isinstance(req, dict) else None
            content_type = req.get("content_type") if isinstance(req, dict) else None

            asset_id = vault.create(filename=filename, content_type=content_type)
            log.debug(
                "[liberation] Vault allocated %s (provider=%s, filename=%s, content_type=%s)",
                asset_id,
                provider or "unknown",
                filename,
                content_type,
            )
            return {
                "download_url": vault.to_asset_uri(asset_id),
                "upload_url": vault.to_upload_uri(asset_id),
            }

        # Normal path: route /proxy/* requests to vendors.
        original_path = cfg.endpoint.path
        cfg = rewrite_request(cfg)
        if cfg.endpoint.path != original_path:
            log.debug("[liberation] Rewrote: %s → %s", original_path, cfg.endpoint.path)

        try:
            return await _original_request_base(cfg, expect_binary)
        except Exception as e:
            msg = str(e)

            # If we routed to a vendor and got a 401, Comfy's client turns it into a misleading
            # "Please login" message. Re-wrap it so the frontend can prompt for a new key.
            parsed = urlparse(cfg.endpoint.path or "")
            is_absolute = bool(parsed.scheme and parsed.netloc)
            is_comfy_api = parsed.netloc.endswith("comfy.org") if parsed.netloc else False
            if is_absolute and not is_comfy_api and msg == "Unauthorized: Please login first to use this node.":
                provider = get_current_provider() or _infer_provider(cfg.node_cls) or "unknown"
                log.warning("[liberation] Vendor 401 mapped to INVALID_KEY (provider=%s, url=%s)", provider, cfg.endpoint.path)
                raise Exception(
                    f"LIBERATION_INVALID_KEY:{provider}:Vendor rejected your API key (HTTP 401). "
                    f"Update your {provider.upper()} API key and retry."
                ) from None

            raise

    # Apply patches
    upload_module.upload_file = patched_upload_file
    client_module._validate_or_raise = patched_validate_or_raise
    client_module._request_base = patched_request_base

    _patched = True
    log.info("[comfy-api-liberation] Patches applied - direct API routing + asset vault enabled")


def restore_patches() -> None:
    global _patched, _original_request_base, _original_validate_or_raise, _original_upload_file
    if not _patched:
        return

    try:
        import comfy_api_nodes.util.client as client_module
        import comfy_api_nodes.util.upload_helpers as upload_module

        if _original_request_base is not None:
            client_module._request_base = _original_request_base
        if _original_validate_or_raise is not None:
            client_module._validate_or_raise = _original_validate_or_raise
        if _original_upload_file is not None:
            upload_module.upload_file = _original_upload_file
    finally:
        _patched = False
        log.info("[comfy-api-liberation] Patches restored to original")
