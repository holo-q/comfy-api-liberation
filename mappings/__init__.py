"""
Endpoint mapping registry — single source of truth for all provider metadata.

Every provider is declared once in PROVIDER_REGISTRY. All other parts of the
system (config.py, patches.py, frontend, routes) derive from this registry
rather than maintaining their own hardcoded lists.

Each entry maps a provider key (e.g. "google") to:
  - node_modules:    ComfyUI node module paths (for monkey-patch error handling)
  - key_url:         Where the user can get an API key
  - mapping_module:  Name of the submodule in this package with MAPPINGS dict
                     (defaults to provider key if omitted)
"""
import logging
from typing import Callable, TypedDict

log = logging.getLogger("comfy-api-liberation")


class ProviderMapping(TypedDict, total=False):
    provider: str                              # Key name in config (e.g., "google")
    url_template: str                          # Vendor URL with {0}, {1} placeholders
    auth_fn: Callable[[str], dict[str, str]]   # Returns auth headers given API key
    request_transform: Callable | None         # Optional request body transform
    response_transform: Callable | None        # Optional response body transform


# =============================================================================
# Single source of truth — add new providers HERE, everything else derives
# =============================================================================

PROVIDER_REGISTRY: dict[str, dict] = {
    "google": {
        "node_modules": ["comfy_api_nodes.nodes_gemini", "comfy_api_nodes.nodes_veo2"],
        "key_url": "https://aistudio.google.com/app/apikey",
    },
    "openai": {
        "node_modules": ["comfy_api_nodes.nodes_openai", "comfy_api_nodes.nodes_sora"],
        "key_url": "https://platform.openai.com/api-keys",
    },
    "grok": {
        "node_modules": ["comfy_api_nodes.nodes_grok"],
        "key_url": "https://console.x.ai/",
    },
    "stability": {
        "node_modules": ["comfy_api_nodes.nodes_stability"],
        "key_url": "https://platform.stability.ai/account/keys",
    },
    "bfl": {
        "node_modules": ["comfy_api_nodes.nodes_bfl"],
        "key_url": "https://api.bfl.ml",
    },
    "ideogram": {
        "node_modules": ["comfy_api_nodes.nodes_ideogram"],
        "key_url": "https://ideogram.ai/manage-api",
    },
    "recraft": {
        "node_modules": ["comfy_api_nodes.nodes_recraft"],
        "key_url": "https://www.recraft.ai/docs/api-reference/getting-started",
    },
    "luma": {
        "node_modules": ["comfy_api_nodes.nodes_luma"],
        "key_url": "https://lumalabs.ai/dream-machine/api/keys",
    },
    "runway": {
        "node_modules": ["comfy_api_nodes.nodes_runway"],
        "key_url": "https://dev.runwayml.com",
    },
    "kling": {
        "node_modules": ["comfy_api_nodes.nodes_kling"],
        "key_url": "https://app.klingai.com/global/dev/api-key",
    },
    "minimax": {
        "node_modules": ["comfy_api_nodes.nodes_minimax"],
        "key_url": "https://platform.minimax.io",
    },
    "pika": {
        "node_modules": ["comfy_api_nodes.nodes_pika"],
        "key_url": "https://pika.art/api",
    },
    "tripo": {
        "node_modules": ["comfy_api_nodes.nodes_tripo"],
        "key_url": "https://platform.tripo3d.ai",
    },
    "rodin": {
        "node_modules": ["comfy_api_nodes.nodes_rodin"],
        "key_url": "https://hyperhuman.deemos.com/api-dashboard",
    },
    "topaz": {
        "node_modules": ["comfy_api_nodes.nodes_topaz"],
        "key_url": "https://www.topazlabs.com/api",
    },
    "byteplus": {
        # Comfy file is named nodes_bytedance.py, but provider config is byteplus
        "node_modules": ["comfy_api_nodes.nodes_bytedance"],
        "key_url": "https://console.byteplus.com",
    },
    "pixverse": {
        "node_modules": ["comfy_api_nodes.nodes_pixverse"],
        "key_url": "https://platform.pixverse.ai",
    },
    "vidu": {
        "node_modules": ["comfy_api_nodes.nodes_vidu"],
        "key_url": "https://platform.vidu.com",
    },
    "moonvalley": {
        "node_modules": ["comfy_api_nodes.nodes_moonvalley"],
        "key_url": "https://www.moonvalley.com",
    },
    "ltx": {
        # Comfy file is named nodes_ltxv.py, but provider config is ltx
        "node_modules": ["comfy_api_nodes.nodes_ltxv"],
        "key_url": "https://ltx.io/model/api",
    },
    "wan": {
        "node_modules": ["comfy_api_nodes.nodes_wan"],
        "key_url": "https://www.alibabacloud.com/help/en/model-studio/get-api-key",
    },
}


# =============================================================================
# Derived views — used by config.py, patches.py, routes.py, and frontend
# =============================================================================

PROVIDERS: list[str] = list(PROVIDER_REGISTRY.keys())
"""All supported provider names, in registry order."""

NODE_MODULE_MAP: dict[str, str] = {
    mod: name
    for name, info in PROVIDER_REGISTRY.items()
    for mod in info.get("node_modules", [])
}
"""Maps ComfyUI node module paths → provider names (for patches.py error handling)."""

KEY_URLS: dict[str, str] = {
    name: info["key_url"]
    for name, info in PROVIDER_REGISTRY.items()
    if "key_url" in info
}
"""Maps provider names → API key signup URLs (for frontend key management UI)."""


# =============================================================================
# Endpoint mapping registry (regex pattern → routing config)
# =============================================================================

ENDPOINT_MAP: dict[str, ProviderMapping] = {}


def register(pattern: str, mapping: ProviderMapping):
    """Register a new endpoint mapping."""
    ENDPOINT_MAP[pattern] = mapping
    log.debug(f"Registered mapping: {pattern} → {mapping['provider']}")


def register_provider_module(module):
    """Auto-register all mappings from a provider module that has MAPPINGS dict."""
    if hasattr(module, 'MAPPINGS'):
        for pattern, mapping in module.MAPPINGS.items():
            register(pattern, mapping)


def _load_all_providers():
    """Import and register all provider mapping modules from the registry."""
    import importlib
    for provider_name in PROVIDER_REGISTRY:
        module_name = PROVIDER_REGISTRY[provider_name].get("mapping_module", provider_name)
        try:
            mod = importlib.import_module(f".{module_name}", package=__name__)
            register_provider_module(mod)
        except Exception as e:
            log.warning(f"Failed to load provider mapping '{module_name}': {e}")

    log.info(f"Loaded {len(ENDPOINT_MAP)} endpoint mappings from {len(PROVIDER_REGISTRY)} providers")


# Load on import
_load_all_providers()
