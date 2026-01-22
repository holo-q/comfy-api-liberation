"""
REST API routes for key management.
Endpoints: /api/liberation/*
"""
import logging
from aiohttp import web

# Import at module level to avoid hot-reload issues with relative imports
from . import config
from . import discovery
from . import mappings
from . import patches

log = logging.getLogger("comfy-api-liberation")


def register_routes():
    """Register API routes with ComfyUI's server."""
    try:
        from server import PromptServer
        routes = PromptServer.instance.routes
    except Exception as e:
        log.warning(f"Could not get PromptServer routes: {e}")
        return

    @routes.get("/api/liberation/keys")
    async def list_keys(request):
        """List all providers and their key status (not actual keys)."""
        return web.json_response(config.get_all_key_status())

    @routes.post("/api/liberation/keys/{provider}")
    async def set_key(request):
        """Set API key for a provider."""
        provider = request.match_info['provider']

        if provider not in config.PROVIDERS:
            return web.json_response(
                {"error": f"Unknown provider: {provider}"},
                status=400
            )

        try:
            data = await request.json()
            key = data.get('key')
            if not key:
                return web.json_response({"error": "No key provided"}, status=400)

            config.set_api_key(provider, key)
            return web.json_response({"status": "ok", "provider": provider})
        except Exception as e:
            log.error(f"Error setting key: {e}")
            return web.json_response({"error": str(e)}, status=500)

    @routes.delete("/api/liberation/keys/{provider}")
    async def delete_key(request):
        """Delete API key for a provider."""
        provider = request.match_info['provider']

        if provider not in config.PROVIDERS:
            return web.json_response(
                {"error": f"Unknown provider: {provider}"},
                status=400
            )

        try:
            config.delete_api_key(provider)
            return web.json_response({"status": "ok", "provider": provider})
        except Exception as e:
            log.error(f"Error deleting key: {e}")
            return web.json_response({"error": str(e)}, status=500)

    @routes.get("/api/liberation/status")
    async def status(request):
        """Get extension status."""
        unmapped = list(discovery.detect_unmapped_endpoints(mappings.ENDPOINT_MAP))

        return web.json_response({
            "patched": patches.is_patched(),
            "mapped_patterns": len(mappings.ENDPOINT_MAP),
            "unmapped_endpoints": unmapped,
            "unmapped_count": len(unmapped),
        })

    @routes.get("/api/liberation/coverage")
    async def coverage(request):
        """Get detailed coverage report."""
        report = discovery.get_proxy_coverage_report(mappings.ENDPOINT_MAP)
        return web.json_response({"report": report})

    @routes.get("/api/liberation/providers")
    async def list_providers(request):
        """List all supported providers."""
        return web.json_response(config.PROVIDERS)

    log.info("Liberation API routes registered")
