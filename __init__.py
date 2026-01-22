"""
ComfyUI API Liberation Extension

Bypasses ComfyUI's credit proxy system by routing API calls directly to vendors
using your own API keys.

Features:
- Direct routing to vendor APIs (Google, OpenAI, Stability, etc.)
- Key management via UI, config file, or environment variables
- Auto-detection of new/unmapped proxy endpoints
- Graceful fallback to Comfy proxy when keys not configured
"""
import logging
import os

# Plugin logger (do not touch global logging config)
log = logging.getLogger("comfy-api-liberation")
log.setLevel(logging.DEBUG if os.environ.get("LIBERATION_DEBUG") == "1" else logging.INFO)

# Version
__version__ = "1.0.0"


def _init_extension():
    """Initialize the extension: apply patches, register routes, check coverage."""

    # 1. Apply monkey patches to intercept API calls
    log.info("Initializing comfy-api-liberation...")

    try:
        from .patches import apply_patches
        apply_patches()
    except Exception as e:
        log.error(f"Failed to apply patches: {e}")

    # 2. Register API routes for key management
    try:
        from .routes import register_routes
        register_routes()
    except Exception as e:
        log.warning(f"Failed to register routes (server may not be ready): {e}")

    # 3. Check coverage and warn about unmapped endpoints
    try:
        from .discovery import detect_unmapped_endpoints
        from .mappings import ENDPOINT_MAP

        unmapped = detect_unmapped_endpoints(ENDPOINT_MAP)
        if unmapped:
            log.warning(f"Found {len(unmapped)} unmapped proxy endpoints (will use Comfy proxy):")
            for ep in sorted(list(unmapped)[:5]):
                log.warning(f"  - {ep}")
            if len(unmapped) > 5:
                log.warning(f"  ... and {len(unmapped) - 5} more")
        else:
            log.info(f"All {len(ENDPOINT_MAP)} proxy endpoints mapped!")

    except Exception as e:
        log.debug(f"Coverage check failed: {e}")

    log.info(f"comfy-api-liberation v{__version__} loaded")


# Initialize on import
_init_extension()


# Export nodes for ComfyUI
from .nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

# Register web extension directory
WEB_DIRECTORY = "./web"

__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
    "WEB_DIRECTORY",
]
