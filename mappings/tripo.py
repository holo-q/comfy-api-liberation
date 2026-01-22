"""Tripo3D endpoint mappings."""

MAPPINGS = {
    r'^/proxy/tripo/v2/openapi/task$': {
        'provider': 'tripo',
        'url_template': 'https://api.tripo3d.ai/v2/openapi/task',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/tripo/v2/openapi/task/([^/]+)$': {
        'provider': 'tripo',
        'url_template': 'https://api.tripo3d.ai/v2/openapi/task/{0}',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
}
