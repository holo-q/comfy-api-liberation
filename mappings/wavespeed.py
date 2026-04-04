"""WaveSpeed endpoint mappings."""

MAPPINGS = {
    r"^/proxy/wavespeed/api/v3/wavespeed-ai/flashvsr$": {
        "provider": "wavespeed",
        "url_template": "https://api.wavespeed.ai/api/v3/wavespeed-ai/flashvsr",
        "auth_fn": lambda key: {"Authorization": f"Bearer {key}"},
        "request_transform": None,
        "response_transform": None,
    },
    r"^/proxy/wavespeed/api/v3/wavespeed-ai/(.+)$": {
        "provider": "wavespeed",
        "url_template": "https://api.wavespeed.ai/api/v3/wavespeed-ai/{0}",
        "auth_fn": lambda key: {"Authorization": f"Bearer {key}"},
        "request_transform": None,
        "response_transform": None,
    },
    r"^/proxy/wavespeed/api/v3/predictions/([^/]+)/result$": {
        "provider": "wavespeed",
        "url_template": "https://api.wavespeed.ai/api/v3/predictions/{0}/result",
        "auth_fn": lambda key: {"Authorization": f"Bearer {key}"},
        "request_transform": None,
        "response_transform": None,
    },
}
