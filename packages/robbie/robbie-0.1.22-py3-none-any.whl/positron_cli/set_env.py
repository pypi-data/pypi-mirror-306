import typer
from typing_extensions import Annotated
from positron_common.user_config import user_config
from positron_common.env_defaults import env_config, EnvType
from positron_common.cli.console import console

def set_env(
  env: Annotated[str, typer.Argument(help='The environment to set.')] = 'dev',
):
    """
    Set's your robbie deploy env. ADVANCED USE ONLY.
    """
    current = env_config[EnvType(env)]
    user_config.backend_api_base_url = current.api_base
    user_config.backend_ws_base_url = current.ws_base
    user_config.write()
    console.print(f'Successfully updated config.')
    console.print(f'[bold]Env[/bold]: {env}')
    console.print(f'[bold]API[/bold]: {current.api_base}')
    console.print(f'[bold]WS [/bold]: {current.ws_base}')
