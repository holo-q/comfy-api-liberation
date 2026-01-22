"""Rodin (Deemos/Hyperhuman) endpoint mappings."""

MAPPINGS = {
    r'^/proxy/rodin/api/v2/rodin$': {
        'provider': 'rodin',
        'url_template': 'https://hyperhuman.deemos.com/api/v2/rodin',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/rodin/api/v2/status$': {
        'provider': 'rodin',
        'url_template': 'https://hyperhuman.deemos.com/api/v2/status',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/rodin/api/v2/download$': {
        'provider': 'rodin',
        'url_template': 'https://hyperhuman.deemos.com/api/v2/download',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
}
