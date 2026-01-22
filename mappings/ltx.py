"""LTX Studio endpoint mappings."""

MAPPINGS = {
    r'^/proxy/ltx/v1/text-to-video$': {
        'provider': 'ltx',
        'url_template': 'https://api.ltx.studio/v1/text-to-video',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/ltx/v1/image-to-video$': {
        'provider': 'ltx',
        'url_template': 'https://api.ltx.studio/v1/image-to-video',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
}
