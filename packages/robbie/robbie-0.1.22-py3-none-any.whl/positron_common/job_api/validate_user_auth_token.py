import requests
from ..env_config import env
from ..cli.logging_config import logger

def is_auth_token_valid() -> bool:
    Headers = {"PositronAuthToken": env.USER_AUTH_TOKEN}
    url = f'{env.API_BASE}/validate-user-auth-token'
    
    logger.debug(f'Calling: {url}')
    response = requests.get(url, headers=Headers)
    
    logger.debug(response)
    if response.status_code == 200:
        return True
    else:
        return False
