"""Recraft endpoint mappings."""

MAPPINGS = {
    r'^/proxy/recraft/image_generation$': {
        'provider': 'recraft',
        'url_template': 'https://external.api.recraft.ai/v1/images/generations',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/recraft/images/imageToImage$': {
        'provider': 'recraft',
        'url_template': 'https://external.api.recraft.ai/v1/images/imageToImage',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/recraft/images/inpaint$': {
        'provider': 'recraft',
        'url_template': 'https://external.api.recraft.ai/v1/images/inpaint',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/recraft/images/removeBackground$': {
        'provider': 'recraft',
        'url_template': 'https://external.api.recraft.ai/v1/images/removeBackground',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/recraft/images/replaceBackground$': {
        'provider': 'recraft',
        'url_template': 'https://external.api.recraft.ai/v1/images/replaceBackground',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/recraft/images/vectorize$': {
        'provider': 'recraft',
        'url_template': 'https://external.api.recraft.ai/v1/images/vectorize',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/recraft/images/creativeUpscale$': {
        'provider': 'recraft',
        'url_template': 'https://external.api.recraft.ai/v1/images/creativeUpscale',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/recraft/images/crispUpscale$': {
        'provider': 'recraft',
        'url_template': 'https://external.api.recraft.ai/v1/images/crispUpscale',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
}
