"""PixVerse endpoint mappings."""

MAPPINGS = {
    r'^/proxy/pixverse/image/upload$': {
        'provider': 'pixverse',
        'url_template': 'https://api.pixverse.ai/v1/image/upload',
        'auth_fn': lambda key: {'API-Key': key},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/pixverse/video/img/generate$': {
        'provider': 'pixverse',
        'url_template': 'https://api.pixverse.ai/v1/video/img/generate',
        'auth_fn': lambda key: {'API-Key': key},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/pixverse/video/text/generate$': {
        'provider': 'pixverse',
        'url_template': 'https://api.pixverse.ai/v1/video/text/generate',
        'auth_fn': lambda key: {'API-Key': key},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/pixverse/video/transition/generate$': {
        'provider': 'pixverse',
        'url_template': 'https://api.pixverse.ai/v1/video/transition/generate',
        'auth_fn': lambda key: {'API-Key': key},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/pixverse/video/result/([^/]+)$': {
        'provider': 'pixverse',
        'url_template': 'https://api.pixverse.ai/v1/video/result/{0}',
        'auth_fn': lambda key: {'API-Key': key},
        'request_transform': None,
        'response_transform': None,
    },
}
