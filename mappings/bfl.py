"""BFL (Black Forest Labs - Flux) endpoint mappings."""

MAPPINGS = {
    r'^/proxy/bfl/flux-2-pro/generate$': {
        'provider': 'bfl',
        'url_template': 'https://api.bfl.ml/v1/flux-2-pro',
        'auth_fn': lambda key: {'x-key': key},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/bfl/flux-kontext-max/generate$': {
        'provider': 'bfl',
        'url_template': 'https://api.bfl.ml/v1/flux-kontext-max',
        'auth_fn': lambda key: {'x-key': key},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/bfl/flux-kontext-pro/generate$': {
        'provider': 'bfl',
        'url_template': 'https://api.bfl.ml/v1/flux-kontext-pro',
        'auth_fn': lambda key: {'x-key': key},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/bfl/flux-pro-1.0-expand/generate$': {
        'provider': 'bfl',
        'url_template': 'https://api.bfl.ml/v1/flux-pro-1.0-expand',
        'auth_fn': lambda key: {'x-key': key},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/bfl/flux-pro-1.0-fill/generate$': {
        'provider': 'bfl',
        'url_template': 'https://api.bfl.ml/v1/flux-pro-1.0-fill',
        'auth_fn': lambda key: {'x-key': key},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/bfl/flux-pro-1.1-ultra/generate$': {
        'provider': 'bfl',
        'url_template': 'https://api.bfl.ml/v1/flux-pro-1.1-ultra',
        'auth_fn': lambda key: {'x-key': key},
        'request_transform': None,
        'response_transform': None,
    },
}
