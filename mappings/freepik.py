"""Freepik endpoint mappings used by Magnific-powered image nodes."""

MAPPINGS = {
    r"^/proxy/freepik/v1/ai/image-upscaler$": {
        "provider": "freepik",
        "url_template": "https://api.freepik.com/v1/ai/image-upscaler",
        "auth_fn": lambda key: {"x-freepik-api-key": key},
        "request_transform": None,
        "response_transform": None,
    },
    r"^/proxy/freepik/v1/ai/image-upscaler/([^/]+)$": {
        "provider": "freepik",
        "url_template": "https://api.freepik.com/v1/ai/image-upscaler/{0}",
        "auth_fn": lambda key: {"x-freepik-api-key": key},
        "request_transform": None,
        "response_transform": None,
    },
    r"^/proxy/freepik/v1/ai/image-upscaler-precision-v2$": {
        "provider": "freepik",
        "url_template": "https://api.freepik.com/v1/ai/image-upscaler-precision-v2",
        "auth_fn": lambda key: {"x-freepik-api-key": key},
        "request_transform": None,
        "response_transform": None,
    },
    r"^/proxy/freepik/v1/ai/image-upscaler-precision-v2/([^/]+)$": {
        "provider": "freepik",
        "url_template": "https://api.freepik.com/v1/ai/image-upscaler-precision-v2/{0}",
        "auth_fn": lambda key: {"x-freepik-api-key": key},
        "request_transform": None,
        "response_transform": None,
    },
    r"^/proxy/freepik/v1/ai/image-style-transfer$": {
        "provider": "freepik",
        "url_template": "https://api.freepik.com/v1/ai/image-style-transfer",
        "auth_fn": lambda key: {"x-freepik-api-key": key},
        "request_transform": None,
        "response_transform": None,
    },
    r"^/proxy/freepik/v1/ai/image-style-transfer/([^/]+)$": {
        "provider": "freepik",
        "url_template": "https://api.freepik.com/v1/ai/image-style-transfer/{0}",
        "auth_fn": lambda key: {"x-freepik-api-key": key},
        "request_transform": None,
        "response_transform": None,
    },
    r"^/proxy/freepik/v1/ai/image-relight$": {
        "provider": "freepik",
        "url_template": "https://api.freepik.com/v1/ai/image-relight",
        "auth_fn": lambda key: {"x-freepik-api-key": key},
        "request_transform": None,
        "response_transform": None,
    },
    r"^/proxy/freepik/v1/ai/image-relight/([^/]+)$": {
        "provider": "freepik",
        "url_template": "https://api.freepik.com/v1/ai/image-relight/{0}",
        "auth_fn": lambda key: {"x-freepik-api-key": key},
        "request_transform": None,
        "response_transform": None,
    },
    r"^/proxy/freepik/v1/ai/skin-enhancer/([^/]+)$": {
        "provider": "freepik",
        "url_template": "https://api.freepik.com/v1/ai/skin-enhancer/{0}",
        "auth_fn": lambda key: {"x-freepik-api-key": key},
        "request_transform": None,
        "response_transform": None,
    },
}
