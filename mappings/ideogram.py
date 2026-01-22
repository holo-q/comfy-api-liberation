"""Ideogram endpoint mappings."""

MAPPINGS = {
    r'^/proxy/ideogram/generate$': {
        'provider': 'ideogram',
        'url_template': 'https://api.ideogram.ai/generate',
        'auth_fn': lambda key: {'Api-Key': key},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/ideogram/ideogram-v3/generate$': {
        'provider': 'ideogram',
        'url_template': 'https://api.ideogram.ai/v3/generate',
        'auth_fn': lambda key: {'Api-Key': key},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/ideogram/ideogram-v3/edit$': {
        'provider': 'ideogram',
        'url_template': 'https://api.ideogram.ai/v3/edit',
        'auth_fn': lambda key: {'Api-Key': key},
        'request_transform': None,
        'response_transform': None,
    },
}
