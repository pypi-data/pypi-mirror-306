import os
import typer
import copy
from typing_extensions import Annotated
from typing import Optional
from positron_common.deploy import command_runner_deploy
from positron_common.config import parse_job_config, PositronJob
from positron_common.cli_args import args
from positron_common.cli.console import console, ROBBIE_DEFAULT, ROBBIE_BLUE
from positron_common.constants import JOB_CONF_YAML_PATH
from positron_common.image_name import get_auto_image_name_and_cluster
from positron_common.cli.interactive import prompt_and_build_positron_job_config
from positron_common.cli.logging_config import logger
from positron_common.enums import JobRunType
from positron_cli.download import filename_is_valid
from positron_common.job_api.funding_envs_images import *
from positron_common.job_api.validate_user_auth_token import is_auth_token_valid
from positron_common.user_config import user_config
from positron_cli.login import login
from pipreqs.pipreqs import init
from prompt_toolkit import prompt
from prompt_toolkit.styles import Style



def run(
  # the following options control the job configuration
  name_arg: Annotated[str, typer.Option("--name", help="Name of the run")] = None,
  funding_arg: Annotated[str, typer.Option("--funding_group_id", help="Specify the team to run the job on.")] = None,
  environment_arg: Annotated[str, typer.Option("--environment_id", help="Specify the hardware to run the job on.")] = None,
  image_arg: Annotated[str, typer.Option("--image", help="Specify the image to run the job on or 'auto-select'.")] = None,
  commands_arg: Annotated[Optional[str], typer.Argument(help='String of shell commands, a .py file, or a .ipynb file.')] = None,
  auto_capture_deps: Annotated[bool, typer.Option("--auto-dep", help='(EXPERIMENTAL) Automatically resolve Python dependencies.')] = None,
  # the following options control how the job is run
  tail: Annotated[bool, typer.Option("--tail", help='Tail the run\'s stdout back to your CLI.')] = False,
  status: Annotated[bool, typer.Option("--s", help='Monitor run status in your CLI.')] = False,
  skip_prompts: Annotated[bool, typer.Option("--y", help='Bypass the prompts and execute the run immediately.')] = False,
  interactive: Annotated[bool, typer.Option("--i", help="Interactively choose your run configuration.")] = False,
  download: Annotated[str, typer.Option("--download", help="Download a results <file> to your local machine. Specify 'all' for the complete list.")] = None,
  path: Annotated[str, typer.Option("--path", help="Local directory where the downloaded files will be stored.")] = None,
  create_only: Annotated[bool, typer.Option("--create-only", help="Only create the run, do not execute it. [Robbie internal use only]")] = False,
) -> None:
    """
    Run shell commands as a batch job in Robbie

    There are three possible scenarios:
    1. User types: robbie run - commands are run from the job_config.yaml file
    2. User types: robbie run "command" - commands override the job_config.yaml file
    3. User types: robbie run --i - interactive mode, user is prompted for all the options and a job_config.yaml file is created/overwritten

    In scenerio 1 and 2, user's can pass in funding groups and enviroments as arguments to override the job_config.yaml file.

    """

    logger.debug("================= run() =====================")
    logger.debug(f"name_arg: {name_arg}")
    logger.debug(f"funding_arg: {funding_arg}")
    logger.debug(f"environment_arg: {environment_arg}")
    logger.debug(f"image_arg: {image_arg}")
    logger.debug(f"commands_arg: {commands_arg}")
    logger.debug(f"auto_capture_deps: {auto_capture_deps}")
    logger.debug(f"tail: {tail}")
    logger.debug(f"status: {status}")
    logger.debug(f"skip_prompts: {skip_prompts}")
    logger.debug(f"interactive: {interactive}")
    logger.debug(f"download: {download}")
    logger.debug(f"path: {path}")
    logger.debug(f"create_only: {create_only}")
    logger.debug(f"=============================================")


    # This check eliminates a extra step if the user happens to run robbie run and the API key is not valid
    if not user_config.user_auth_token or not is_auth_token_valid():
        # there is no auth token set in .robbie/config.yaml or the token is invalid/expired in the backend
        console.print('[red]Sorry, your API is invalid, please login.')
        login()

    # we can either stream or monitor status but not both at the same time
    if tail and status:
        console.print('[red]Error: Choose either the -logs and -s option.')
        return
    
    if (download and not (tail or status)):    
        console.print('[red]Error: The --download option can only be used with the --tail or --s option.')
        return
    
    if download and not filename_is_valid(download):
        console.print('[red]Error: Please specify a valid file name or "all" to download all files.')
        return
    
    if path and not download:
        console.print('[red]Error: The --path option can only be used with the --download option.')
        return
    
    if path and not os.path.exists(path):
        console.print('[red]Error: The path you specified is not valid.')
        return

    # initialize the argument singleton
    args.init(
        name=name_arg,
        stream_stdout=tail,
        skip_prompts=skip_prompts,
        monitor_status=status,
        commands_to_run=commands_arg,
        interactive=interactive,
        create_only=create_only,
        download=download,
        local_path=path,
        auto_capture_deps=auto_capture_deps
    )

    # first-level sanity checks
    if commands_arg and interactive:
        console.print("[red]Sorry: Please specify command line or use the interactive mode.")
        return
    
    if interactive and (funding_arg or environment_arg or image_arg):
        console.print("[red]Sorry: You can't specify funding, environments, or images in interactive mode.")
        return

    # Read in the job_config.yaml file if it exists
    yaml_job_config = None
    if os.path.exists(JOB_CONF_YAML_PATH) and os.path.getsize(JOB_CONF_YAML_PATH) != 0:
        console.print(f'Found run and reading configuration file: {JOB_CONF_YAML_PATH}')
        yaml_job_config = parse_job_config(JOB_CONF_YAML_PATH)
        if yaml_job_config:
            if yaml_job_config.funding_group_id:
                yaml_job_config.funding_selection = "From job_config.yaml"
            if yaml_job_config.environment_id:
                yaml_job_config.environment_selection = "From job_config.yaml"
            if yaml_job_config.image:
                yaml_job_config.image_selection = "From job_config.yaml"
        else:
            console.print('[red]Error parsing job_config.yaml file. Disregarding it.')
            

    """
    There are three possible scenarios:
    1. User types: robbie run - commands are run from the job_config.yaml file
    2. User types: robbie run "command" - commands override the job_config.yaml file
    3. User types: robbie run --i - interactive mode, user is prompted for all the options and a job_config.yaml file is created

    There are three important variables in the code:
    - yaml_job_config - this is the PositronJob object created from the job_config.yaml file
    - job_config_to_run - this is the PositronJob object that will be passed to deploy to run the job
    - add_args_to_run_job_config - this is a flag that is set for scenerio 1 and 2 to merge the passed arguments into to the job_config_to_run object
    """
    add_args_to_run_job_config = False
    # 
    # Scenerio 1: User types: "robbie run" - commands are run from the job_config.yaml file
    #
    if not commands_arg and not interactive:
        logger.debug("@@@@@@@@@@@   Scenerio 1: User types: robbie run")
        if not yaml_job_config:
            console.print('[red]Error: No job_config.yaml file found. Please specify commands to run.')
            return
        if not yaml_job_config.commands:
            console.print('[red]Error: No commands found in job_config.yaml file.')
            return
        job_config_to_run = yaml_job_config
        add_args_to_run_job_config = True

    # 
    # Scenerio 2. User types: robbie run "command" - commands override the job_config.yaml file if it exists
    #
    if commands_arg:
        logger.debug("@@@@@@@@@@ Scenerio 2: User types: robbie run 'command'")
        # Is there a job_config.yaml file?
        if yaml_job_config:
            if yaml_job_config.commands:
                console.print('[yellow]Overriding commands in existing job_config.yaml file.')
            job_config_to_run = yaml_job_config
        else:
            console.print('No job_config.yaml file found, using defaults.')
            job_config_to_run = PositronJob()
        
        # Add the commands to the job_config
        job_config_to_run.commands = []
        job_config_to_run.commands.append(commands_arg)

        add_args_to_run_job_config = True
        
    # now lets deal with the arguments for the first two scenarios
    if add_args_to_run_job_config:
        logger.debug("Adding arguments to job_config")
        job_config_to_run = _merge_from_yaml_and_args(job_config_to_run, funding_arg, environment_arg)
        if not job_config_to_run:
            logger.debug('[red]Error: Unable to merge yaml and arguments.')
            return
        
        # now lets sort out the image
        if job_config_to_run.image:
            # there is one in the job_config.yaml file
            if image_arg:
                logger.debug(f'[yellow] Notice: overriding image job_config.yaml image: {job_config_to_run.image}, setting image to: {image_arg}')
                job_config_to_run.image = image_arg
                job_config_to_run.image_selection = "Overriden by argument"
            else:
                logger.debug(f'Using the image: {job_config_to_run.image} found in job_config.yaml. To override, please use the --image option.')
                job_config_to_run.image_selection = "From job_config.yaml"
    
            if job_config_to_run.image == "auto-select":
                # auto select the image and cluster
                job_config_to_run.image, job_config_to_run.cluster = get_auto_image_name_and_cluster(job_config_to_run.funding_group_id, job_config_to_run.environment_id)
                job_config_to_run.image_selection = "Automatically Selected"
    # 
    # Scenerio 3. User types: robbie run --i - interactive mode, user is prompted for all the options and a job_config.yaml file is created or modified
    #
    if interactive:
        logger.debug("@@@@@@@@@ Scenerio 3: User types: robbie run --i")
        preserve = False
        if yaml_job_config and yaml_job_config.commands:
            response = prompt('You are about to override your job_config.yaml, do you want preserve the enviroment variables and commands [[y]/n]:', style=Style.from_dict({'prompt': 'yellow'}))
            if response in ["y", "yes", "Yes", "Y", ""]:
                preserve = True        
                       
        # lets prompt the user 
        console.print(f"Please follow the prompts to configure your run ([{ROBBIE_DEFAULT}][] = default[/{ROBBIE_DEFAULT}], <tab> for options)")
        captured_job_config = prompt_and_build_positron_job_config(preserve)
        logger.debug("Interactive cfg: ", captured_job_config)
        if captured_job_config == None:
            console.print(f"[red]Sorry, failed to create a file {JOB_CONF_YAML_PATH}")
            return
        
        # keeping the previous commands and envs from the job_config.yaml file
        if preserve:
            if yaml_job_config.env:
                # this prevents a null env from being copied over
                captured_job_config.python_job.env = yaml_job_config.env
            
            captured_job_config.python_job.commands = yaml_job_config.commands

        if captured_job_config.python_job.commands == None:
            console.print("[red]Error: You did not specify any commands to run.")
            return
        captured_job_config.write_to_file(filename=JOB_CONF_YAML_PATH)
        job_config_to_run = captured_job_config.python_job

    # Handle auto capturing dependencies for non-Conda environments
    # this comes in two forms:
    # 1. User types: robbie run --auto-dep
    # 2. job_config.yaml file has dependencies: auto-capture
    overwrite_reqs = False
    if auto_capture_deps or (yaml_job_config and yaml_job_config.dependencies == "auto-capture"):
        logger.debug("Auto-capturing dependencies")
        if os.path.exists("./requirements.txt"):
            if args.skip_prompts == False:
                overwrite_reqs = prompt('A requirement.txt file already exist, do you want to overwrite it? [y/N]:', style=Style.from_dict({'prompt': 'yellow'}))
                if overwrite_reqs in ["no", "n", "No", "N", ""]:
                    console.print("[yellow]See you soon![/yellow]")
                    return
            else:
                overwrite_reqs = True
            
        # arguments for pipreqs package - https://github.com/bndr/pipreqs
        pipreq_args = {
            "<path>": ".",
            "--print": False,
            "--savepath": None,
            "--pypi-server": None,
            "--proxy": None,
            "--use-local": False,
            "--diff": None,
            "--clean": None,
            "--mode": None,
            "--scan-notebooks": True,
            "--force": False
        }
        if overwrite_reqs:
            pipreq_args["--force"] = True

        console.print("Analyzing Python (.py) and Notebook (.ipynb) files for dependencies...", style=ROBBIE_BLUE)
        init(pipreq_args) # this is the pipreqs call    
        console.print("[green]✔[/green] Dependency analysis complete, requirements.txt file created.")
        job_config_to_run.dependencies = "./requirements.txt"
        # hack to remove robbie from the generated requirements.txt file
        _remove_package_from_requirements('robbie')

    job_config_to_run.job_type = JobRunType.BASH_COMMAND_RUNNER
    logger.debug("Calling command_runner_deploy")
    command_runner_deploy(job_config_to_run)


def _merge_from_yaml_and_args(input_job_config: PositronJob, funding_arg: str, environment_arg: str) -> PositronJob:
    """
    Merge the job_config.yaml file with the command line arguments for funding, and environment.
    Ensure that environment is in the funding group.

    Behavior:
    - Command line arguments take precedence over the job_config.yaml file
    - Command line arguments are not memorized in the job_config.yaml file 

    """
    if not input_job_config:
        logger.debug("No job config to merge.")
        return None
    
    logger.debug("================= Entering _merge_from_yaml_and_args() =====================")
    input_job_config.print()

    return_config = copy.deepcopy(input_job_config)
    logger.debug(f"return_config: {id(return_config)} created from input_job_config: {id(input_job_config)}")

    # Is there a funding group in the input config?
    if input_job_config.funding_group_id:
        logger.debug(f"return_config.funding_group_id: already set: {return_config.funding_group_id}")
        # ok the correct funding group is already in return_config.funding_group_id
        pass

    # Is there a funding group argument?
    if funding_arg:
        logger.debug(f"Setting or overriding return_config.funding_group_id: {return_config.funding_group_id} <-- funding_arg: {funding_arg}")
        return_config.funding_selection = "Overridden by argument"
        return_config.funding_group_id = funding_arg
        
    # pre-fetch the funding sources info and def env
    fs = list_funding_sources()
    if len(fs) == 0:
        logger.debug("No funding sources found.")
        return None

    def_env_id = None
    # Have we identified a funding group yet?
    if return_config.funding_group_id:
        # Find the default funding source (personal)
        logger.debug(f"Yes, we have a funding group: {return_config.funding_group_id}")
        if not return_config.environment_id:
            for _, val in fs.items():
                if (val[FS_ID] == return_config.funding_group_id):
                    def_env_id = val.get(FS_DEF_ENV_ID)
            if not def_env_id:
                console.print(f"[bold red]Can't get the default environment for the funding group: {return_config.funding_group_id}")
                return None   
            if not return_config.environment_id:
                logger.debug(f"setting return_config.environment_id: {return_config.environment_id} <-- def_env_id: {def_env_id}")
                return_config.environment_id = def_env_id
                return_config.environment_selection = "Default"
        else:
            if not _env_in_funding_group(return_config.environment_id, return_config.funding_group_id):
                console.print(f"[bold red] Sorry, the environment in your job_config.yaml: {return_config.environment_id} is not the funding group: {return_config.funding_group_id}")
                return None
    else: 
        # No funding group id, let's get the user's personal and defaut environment
        logger.debug("Still no funding group id, let's get the user's personal one.")
        for _, val in fs.items():
            if (val[FS_TYPE] == FS_PERSONAL_TYPE):
                return_config.funding_group_id = val.get(FS_ID)
                def_env_id = val.get(FS_DEF_ENV_ID)
                logger.debug(f"Setting return_config.funding_group_id to PERSONAL: {return_config.funding_group_id}, fetched def_env_id: {def_env_id}")
        if return_config.funding_group_id:
            return_config.funding_selection = "Default"
        else:
            console.print("[bold red]Can't get the default funding source (personal).")
            return None
        if not def_env_id:
            console.print("[bold red]Can't get the default environment for the personal funding source.")
            return None
        # the user specified an environment in the job_config.yaml file
        if return_config.environment_id:
            # just for fun, lets check if its in the funding group
            if not _env_in_funding_group(return_config.environment_id, return_config.funding_group_id):
                console.print(f"[bold red] Sorry, the environment in your job_config.yaml: {return_config.environment_id} is not the funding group: {return_config.funding_group_id}")
                return None
        else:
            logger.debug(f"setting return_config.environment_id: {return_config.environment_id} <-- def_env_id: {def_env_id}")
            return_config.environment_id = def_env_id
            return_config.environment_selection = "Default from Funding Source"
        
    # At this point we should have a funding group id and a default environment id
    if environment_arg:
        # check to make certain the environment argument is in the funding group
        if not _env_in_funding_group(environment_arg, return_config.funding_group_id):
            console.print(f"[bold red] Sorry, the environment you passed as an argument: {environment_arg} is not the funding group: {return_config.funding_group_id}")
            return None
        logger.debug(f"setting return_config.environment_id: {return_config.environment_id} <-- environment_arg: {environment_arg}")
        return_config.environment_id = environment_arg
        return_config.environment_selection = "Overridden by argument"

    logger.debug("================= Exiting _merge_from_yaml_and_args() =====================")
    return_config.print()

    return return_config

def _env_in_funding_group(env_id, funding_group_id):
    """ sanity check a environment id is in the funding group """
    envs = list_environments(funding_group_id)
    for _, val in envs.items():
        if (val[FS_ID] == env_id):
            return True
    return False

def _remove_package_from_requirements(package_name, file_path='./requirements.txt'):
    """ this is hack when the robbie package gets auto-added to the requirements.txt file in the auto-capture dependencies mode """
    # Read the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Write back all lines except the one with the package name
    with open(file_path, 'w') as file:
        for line in lines:
            if not line.strip().startswith(package_name):
                file.write(line)







