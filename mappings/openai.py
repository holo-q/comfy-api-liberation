"""OpenAI (GPT, DALL-E, Sora) endpoint mappings."""

MAPPINGS = {
    # Responses API (GPT, etc)
    r'^/proxy/openai/v1/responses$': {
        'provider': 'openai',
        'url_template': 'https://api.openai.com/v1/responses',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/openai/v1/responses/(.+)$': {
        'provider': 'openai',
        'url_template': 'https://api.openai.com/v1/responses/{0}',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    # Image generation (DALL-E)
    r'^/proxy/openai/images/generations$': {
        'provider': 'openai',
        'url_template': 'https://api.openai.com/v1/images/generations',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/openai/images/edits$': {
        'provider': 'openai',
        'url_template': 'https://api.openai.com/v1/images/edits',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    # Sora video
    r'^/proxy/openai/v1/videos$': {
        'provider': 'openai',
        'url_template': 'https://api.openai.com/v1/videos',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/openai/v1/videos/([^/]+)$': {
        'provider': 'openai',
        'url_template': 'https://api.openai.com/v1/videos/{0}',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/openai/v1/videos/([^/]+)/content$': {
        'provider': 'openai',
        'url_template': 'https://api.openai.com/v1/videos/{0}/content',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
}
