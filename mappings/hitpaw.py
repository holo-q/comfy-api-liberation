"""HitPaw endpoint mappings."""

MAPPINGS = {
    r"^/proxy/hitpaw/api/photo-enhancer$": {
        "provider": "hitpaw",
        "url_template": "https://api-base.hitpaw.com/api/photo-enhancer",
        "auth_fn": lambda key: {"APIKEY": key},
        "request_transform": None,
        "response_transform": None,
    },
    r"^/proxy/hitpaw/api/video-enhancer$": {
        "provider": "hitpaw",
        "url_template": "https://api-base.hitpaw.com/api/video-enhancer",
        "auth_fn": lambda key: {"APIKEY": key},
        "request_transform": None,
        "response_transform": None,
    },
    r"^/proxy/hitpaw/api/task-status$": {
        "provider": "hitpaw",
        "url_template": "https://api-base.hitpaw.com/api/task-status",
        "auth_fn": lambda key: {"APIKEY": key},
        "request_transform": None,
        "response_transform": None,
    },
}
