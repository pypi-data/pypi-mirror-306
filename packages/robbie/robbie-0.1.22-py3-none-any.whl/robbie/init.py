from positron_cli.login import login
from positron_common.job_api.validate_user_auth_token import is_auth_token_valid
from positron_common.user_config import user_config
from robbie.run_notebook import run_notebook

def init(loglevel: str = None):
    if not user_config.user_auth_token or not is_auth_token_valid():
        # there is no auth token set in .robbie/config.yaml or the token is invalid/expired in the backend
        login()
    run_notebook(loglevel)
