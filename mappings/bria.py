"""Bria endpoint mappings."""

MAPPINGS = {
    r"^/proxy/bria/v2/image/edit$": {
        "provider": "bria",
        "url_template": "https://engine.prod.bria-api.com/v2/image/edit",
        "auth_fn": lambda key: {"api_token": key},
        "request_transform": None,
        "response_transform": None,
    },
    r"^/proxy/bria/v2/status/([^/]+)$": {
        "provider": "bria",
        "url_template": "https://engine.prod.bria-api.com/v2/status/{0}",
        "auth_fn": lambda key: {"api_token": key},
        "request_transform": None,
        "response_transform": None,
    },
    r"^/proxy/bria/v2/image/edit/remove_background$": {
        "provider": "bria",
        "url_template": "https://engine.prod.bria-api.com/v2/image/edit/remove_background",
        "auth_fn": lambda key: {"api_token": key},
        "request_transform": None,
        "response_transform": None,
    },
    r"^/proxy/bria/v2/video/edit/remove_background$": {
        "provider": "bria",
        "url_template": "https://engine.prod.bria-api.com/v2/video/edit/remove_background",
        "auth_fn": lambda key: {"api_token": key},
        "request_transform": None,
        "response_transform": None,
    },
}
