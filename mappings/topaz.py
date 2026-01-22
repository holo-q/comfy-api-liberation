"""Topaz Labs endpoint mappings."""

MAPPINGS = {
    r'^/proxy/topaz/image/v1/enhance-gen/async$': {
        'provider': 'topaz',
        'url_template': 'https://api.topazlabs.com/image/v1/enhance-gen/async',
        'auth_fn': lambda key: {'X-API-Key': key},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/topaz/image/v1/status/([^/]+)$': {
        'provider': 'topaz',
        'url_template': 'https://api.topazlabs.com/image/v1/status/{0}',
        'auth_fn': lambda key: {'X-API-Key': key},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/topaz/image/v1/download/([^/]+)$': {
        'provider': 'topaz',
        'url_template': 'https://api.topazlabs.com/image/v1/download/{0}',
        'auth_fn': lambda key: {'X-API-Key': key},
        'request_transform': None,
        'response_transform': None,
    },
    # Video endpoints
    r'^/proxy/topaz/video/$': {
        'provider': 'topaz',
        'url_template': 'https://api.topazlabs.com/video/',
        'auth_fn': lambda key: {'X-API-Key': key},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/topaz/video/([^/]+)/accept$': {
        'provider': 'topaz',
        'url_template': 'https://api.topazlabs.com/video/{0}/accept',
        'auth_fn': lambda key: {'X-API-Key': key},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/topaz/video/([^/]+)/complete-upload$': {
        'provider': 'topaz',
        'url_template': 'https://api.topazlabs.com/video/{0}/complete-upload',
        'auth_fn': lambda key: {'X-API-Key': key},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/topaz/video/([^/]+)/status$': {
        'provider': 'topaz',
        'url_template': 'https://api.topazlabs.com/video/{0}/status',
        'auth_fn': lambda key: {'X-API-Key': key},
        'request_transform': None,
        'response_transform': None,
    },
}
