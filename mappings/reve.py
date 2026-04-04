"""Reve endpoint mappings."""

MAPPINGS = {
    r"^/proxy/reve/v1/image/create$": {
        "provider": "reve",
        "url_template": "https://api.reve.com/v1/image/create",
        "auth_fn": lambda key: {"Authorization": f"Bearer {key}"},
        "request_transform": None,
        "response_transform": None,
    },
    r"^/proxy/reve/v1/image/edit$": {
        "provider": "reve",
        "url_template": "https://api.reve.com/v1/image/edit",
        "auth_fn": lambda key: {"Authorization": f"Bearer {key}"},
        "request_transform": None,
        "response_transform": None,
    },
    r"^/proxy/reve/v1/image/remix$": {
        "provider": "reve",
        "url_template": "https://api.reve.com/v1/image/remix",
        "auth_fn": lambda key: {"Authorization": f"Bearer {key}"},
        "request_transform": None,
        "response_transform": None,
    },
}
