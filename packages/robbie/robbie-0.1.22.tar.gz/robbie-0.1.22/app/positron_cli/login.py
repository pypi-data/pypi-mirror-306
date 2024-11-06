import webbrowser
import typer
from positron_common.user_config import user_config, DEFAULT_USER_CONFIG_PATH   
from positron_common.cli.logging_config import logger
from positron_common.cli.console import console
from positron_common.constants import APP_NAME, APP_HOME_DIR
from positron_common.auth_api.login import get_device_code_payload, get_user_auth_token, wait_for_access_token
from positron_common.env_config import env
from positron_common.exceptions import RemoteCallException

def login() -> None:
    """
    Logs you in to your Robbie account and stores API key on your local machine.
    """
    # Get device code
    try:
        console.print('Authenticating with Robbie...')
        device_code_data = get_device_code_payload()

        # Redirect to login
        console.print("1. If a browser window doesn't automatically launch, navigate to: ", device_code_data['verification_uri_complete'])
        console.print('2. Confirm the following code: ', device_code_data['user_code'])
        console.print('3. Enter your username and password!')
        console.print('')
        webbrowser.open(url=device_code_data['verification_uri_complete'], new=2, autoraise=True)

        # Wait for authentication
        access_token = wait_for_access_token(device_code_data)
        logger.debug(f'Access Token: {access_token}')

        # console.print('Requesting User Auth Token')
        user_token_response_data = get_user_auth_token(access_token)

        console.print(f'[green]Writing {APP_NAME} access token to: {DEFAULT_USER_CONFIG_PATH}')
        save_user_token(user_token_response_data['userAuthToken'])
        # ensure that "env" is updated with the new user token if it was imported previsouly
        env.USER_AUTH_TOKEN = user_config.user_auth_token
    except RemoteCallException as e:
        logger.debug(e, exc_info=True)
        console.print(f"[red]{e.user_friendly_message}")
        raise typer.Exit(code=1)
    except Exception as e:
        logger.debug(e, exc_info=True)
        console.print(f"[red]An error occurred: {e}. If the problem continues, reach out to our support team for help.\nEmail: support@robbie.run[/red]")
        raise typer.Exit(code=1)

def save_user_token(user_token):
    user_config.user_auth_token = user_token
    user_config.write()
    
