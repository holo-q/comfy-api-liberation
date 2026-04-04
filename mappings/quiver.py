"""Quiver endpoint mappings."""

MAPPINGS = {
    r"^/proxy/quiver/v1/svgs/generations$": {
        "provider": "quiver",
        "url_template": "https://api.quiver.ai/v1/svgs/generations",
        "auth_fn": lambda key: {"Authorization": f"Bearer {key}"},
        "request_transform": None,
        "response_transform": None,
    },
    r"^/proxy/quiver/v1/svgs/vectorizations$": {
        "provider": "quiver",
        "url_template": "https://api.quiver.ai/v1/svgs/vectorizations",
        "auth_fn": lambda key: {"Authorization": f"Bearer {key}"},
        "request_transform": None,
        "response_transform": None,
    },
}
