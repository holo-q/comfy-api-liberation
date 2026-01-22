"""
Endpoint mapping registry.
Maps ComfyUI proxy paths to direct vendor APIs.
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


# Global registry: regex pattern → mapping
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
    """Load all provider mapping modules."""
    from . import (
        google,
        openai,
        stability,
        bfl,
        ideogram,
        recraft,
        luma,
        runway,
        kling,
        minimax,
        pika,
        tripo,
        rodin,
        topaz,
        byteplus,
        pixverse,
        vidu,
        moonvalley,
        ltx,
        wan,
    )

    providers = [
        google, openai, stability, bfl, ideogram, recraft,
        luma, runway, kling, minimax, pika, tripo, rodin,
        topaz, byteplus, pixverse, vidu, moonvalley, ltx, wan,
    ]

    for provider in providers:
        try:
            register_provider_module(provider)
        except Exception as e:
            log.warning(f"Failed to load provider {provider.__name__}: {e}")

    log.info(f"Loaded {len(ENDPOINT_MAP)} endpoint mappings")


# Load on import
_load_all_providers()
