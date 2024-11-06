from functools import wraps
import argparse
import os
from positron_common.cli_args import args as cli_args
from positron_common.config import PositronJob, parse_job_config, merge_config
from positron_common.deployment.deploy import Deploy
from positron_common.deployment.stored_function import StoredFunction
from positron_common.job_api.validate_user_auth_token import is_auth_token_valid
from positron_common.user_config import user_config
from positron_common.cli.console import console
from positron_common.cli.logging_config import logger, set_log_level
from positron_common.enums import JobRunType
from positron_common.utils import _exit_by_mode
from positron_cli.login import login

def remote(**parameters):

    # Parse command line arguments
    parser = argparse.ArgumentParser(description = "A decorator to handle deploying running your function in the cloud")
    parser.add_argument('--tail', action='store_true', help='Stream the stdout from Positron Cloud back to your cli', dest='stream_stdout', default=False)
    parser.add_argument('--loglevel', help='Set the logging level [CRITICAL,FATAL,ERROR, WARNING, INFO, DEBUG, NOTSET]', dest='loglevel')
    parser.add_argument('--create-only', action='store_true', help='Create the job but do not run it.', dest='create_only')
    parser.add_argument('--results-from-job-id', help='Fetch results and return from decorated function.', dest='results_from_job_id')
    positron_args, job_args = parser.parse_known_args()

    if positron_args.loglevel:
        set_log_level(positron_args.loglevel)

    logger.debug("========positron_args========")
    logger.debug(positron_args) 
    logger.debug("========job_args========")
    logger.debug(job_args)

    # Jupyter Support - Default out the cli_args to run remote always with no prompting
    if not cli_args.is_init:
        cli_args.init(
            local=False,
            deploy=True,
            stream_stdout=positron_args.stream_stdout,
            job_args=job_args,
            create_only=positron_args.create_only,
            results_from_job_id=positron_args.results_from_job_id,
            skip_prompts=True,
        )

    # enable  and tail function parameters but remove them before passing to PositronJob config    
    if "loglevel" in parameters:
        print("Setting log level to: " + parameters["loglevel"])
        set_log_level(parameters["loglevel"])
        del parameters["loglevel"]
    if "tail" in parameters:
        cli_args.stream_stdout = parameters["tail"]
        del parameters["tail"]
    if "create_only" in parameters:
        cli_args.create_only = parameters["create_only"]
        del parameters["create_only"]

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.debug("Running decorator")

            # Check this first to ensure we don't deploy
            if os.getenv('POSITRON_CLOUD_ENVIRONMENT', False):
                logger.debug("Running function locally")
                return func(*args, **kwargs)

            # This check eliminates a extra step if the user happens to run robbie run and the API key is not valid
            if not user_config.user_auth_token or not is_auth_token_valid():
                # there is no auth token set in .robbie/config.yaml or the token is invalid/expired in the backend
                console.print('[red]Sorry, your API is invalid, please login.')
                login()

            if cli_args.results_from_job_id:
                stored_function = StoredFunction(func, args, kwargs)
                stored_function.set_job_id(cli_args.results_from_job_id)
                secret_key = user_config.user_auth_token if user_config.user_auth_token else ""
                stored_function.load_and_validate_results(hmac_key=secret_key)
                return stored_function.result

            console.print("Robbie's deploying your function!", style="bold")
            # get decorator arguments
            job_config_decorator = PositronJob(**parameters)

            # track where the parameters come from so we can display to the user later
            if job_config_decorator.funding_group_id:
                job_config_decorator.funding_selection = "Passed as argument to @remote decorator"
            if job_config_decorator.environment_id:
                job_config_decorator.environment_selection = "Passed as argument to @remote decorator"
            if job_config_decorator.image:
                job_config_decorator.image_selection = "Passed as argument to @remote decorator"
                
            logger.debug("========job_config_decorator (arguments passed into remote function)========")
            job_config_decorator.print()

            job_config = job_config_decorator
            job_config.job_type = JobRunType.REMOTE_FUNCTION_CALL

            # use job yaml as base if it exists
            job_config_yaml = parse_job_config()
            if job_config_yaml:
                logger.debug("========job_config_yaml found========")
                job_config_yaml.print()
                if job_config_yaml.funding_group_id:
                    job_config_yaml.funding_selection = "From job_config.yaml"
                if job_config_yaml.environment_id:
                    job_config_yaml.environment_selection = "From job_config.yaml"
                if job_config_yaml.image:
                    job_config_yaml.image_selection = "From job_config.yaml"

                logger.debug("========merging configs=======")
                job_config = merge_config(job_config_yaml, job_config_decorator)
            else:
                logger.debug("========no job_config.yaml found========")

            if job_config.commands:
                console.print("[red]Error: The 'commands' configuration in job_config.yaml is not supported in the remote decorator.\nPlease remove it or run with 'robbie run' to use 'commands'.[/red]")
                _exit_by_mode(1)

            logger.debug("========job_config being passed to function========")
            job_config.print()

            return Deploy.remote_function_deploy(func, args, kwargs, job_config)

        return wrapper
    return decorator