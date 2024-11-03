import requests
import os

def load_keys():
    endpoints = {
        'OPENAI_API_KEY': 'https://l1wlltwcad.execute-api.us-east-1.amazonaws.com/default/openaiLambda',
        'ANTHROPIC_API_KEY': 'https://nxb1ox1u9a.execute-api.us-east-1.amazonaws.com/default/anthropicLambda'
    }
        
    try:
        # Get secrets from both endpoints
        for service, endpoint in endpoints.items():
            response = requests.get(endpoint)
            if response.status_code == 200:
                secret = response.json()
                # Set environment variables directly with the value
                os.environ[service] = secret['key']  # Assuming the key is in the 'key' field
            else:
                raise Exception(f'Error retrieving {service} secret: {response.status_code}, {response.text}')
        
    except Exception as e:
        raise Exception(f'Error in load_keys: {str(e)}')
