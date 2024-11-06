from pydantic import BaseModel
from .env_defaults import current
from .user_config import user_config
from typing import Optional
from positron_common.cli.console import console

class EnvConfig(BaseModel):
    """
    The environment configuration for the Positron CLI.
    Loaded like so: defaults <- config file <- env vars.
    """
    API_BASE: str = current.api_base
    SOCKET_IO_DOMAIN: str = current.ws_base
    AUTH0_DOMAIN: str = current.auth0_domain
    AUTH0_CLIENT_ID: str = current.auth0_client_id
    AUTH0_AUDIENCE: str =  current.auth0_audience
    COMPRESSED_WS_NAME: str = 'workspace.tar.gz'
    SOCKET_IO_PATH: str = '/api/ws/socket.io'
    USER_AUTH_TOKEN: Optional[str] = None

    def __init__(self):
        super().__init__()

        # Override app dev defaults
        if user_config.user_auth_token:
            self.USER_AUTH_TOKEN = user_config.user_auth_token
        if user_config.backend_api_base_url:
            self.API_BASE = user_config.backend_api_base_url
        if user_config.backend_ws_base_url:
            self.SOCKET_IO_DOMAIN = user_config.backend_ws_base_url

    def dump(self):
        """
        Print the "env" configuration to the console.
        """
        console.print(f'API_BASE: {self.API_BASE}')
        console.print(f'SOCKET_IO_DOMAIN: {self.SOCKET_IO_DOMAIN}')
        console.print(f'AUTH0_DOMAIN: {self.AUTH0_DOMAIN}')
        console.print(f'AUTH0_CLIENT_ID: {self.AUTH0_CLIENT_ID}')
        console.print(f'AUTH0_AUDIENCE: {self.AUTH0_AUDIENCE}')
        console.print(f'COMPRESSED_WS_NAME: {self.COMPRESSED_WS_NAME}')
        console.print(f'SOCKET_IO_PATH: {self.SOCKET_IO_PATH}')
        console.print(f'USER_AUTH_TOKEN: {self.USER_AUTH_TOKEN}')

env = EnvConfig()
"""
The environment configuration for the Positron CLI.
"""
