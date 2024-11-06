import time
from .config import PositronJob
from .cli.console import console, ROBBIE_ORANGE, ROBBIE_BLUE
from rich.text import Text
from rich.panel import Panel
from rich import box
from .exceptions import RemoteCallException
from .cli.logging_config import logger

def print_robbie_configuration_banner(job: dict, job_config: PositronJob):
    text = Text()

    if job_config.name:
        text.append("Run Name: ", style=ROBBIE_BLUE)
        text.append(f"{job_config.name}\n")

    text.append("Python Version: ", style=ROBBIE_BLUE)
    text.append(f"{job_config.python_version}\n")

    text.append("Robbie Python SDK Version: ", style=ROBBIE_BLUE)
    text.append(f"{job_config.robbie_sdk_version}\n")

    text.append("Dependency file: ", style=ROBBIE_BLUE)
    text.append(f"{job_config.dependencies}\n")

    text.append("Conda Environment: ", style=ROBBIE_BLUE)
    text.append(f"{job_config.conda_env}\n")
    
    text.append("Funding Source: ", style=ROBBIE_BLUE)
    if not job_config.funding_selection:
        job_config.funding_selection = "Default"
    text.append(f"{job['fundingGroupName']} ({job['fundingGroupId']}) - {job_config.funding_selection}\n")
        
    text.append("Hardware: ", style=ROBBIE_BLUE)
    if not job_config.environment_selection:
        job_config.environment_selection = "Default"
    text.append(f"{job['environmentName']} ({job['environmentId']}) - {job_config.environment_selection}\n")

    if job_config.cluster:
        text.append("Cluster: ", style=ROBBIE_BLUE)
        text.append(f"{job_config.cluster}\n")
        
    text.append("Image: ", style=ROBBIE_BLUE)
    if not job_config.image_selection:
        job_config.image_selection = "Default" 
    text.append(f"{job['imageName']} - {job_config.image_selection}\n")
        
    text.append("Workspace Directory: ", style=ROBBIE_BLUE)
    text.append(f"{job_config.workspace_dir}\n") 
    text.append("Max Token Consumption: ", style=ROBBIE_BLUE)
    if not job["maxUsableTokens"]:
        text.append("Not specified\n")
    else:
        text.append(f"{job['maxUsableTokens']}\n")

    text.append("Max Execution Time (minutes): ", style=ROBBIE_BLUE)

    if not job["maxExecutionMinutes"]:
        text.append("Not specified\n")
    else:
        text.append(f"{job['maxExecutionMinutes']}\n")
    
    text.append("Environment Variables: ", style=ROBBIE_BLUE)

    if not job_config.env:
         text.append("None specified\n")
    else:
        text.append(f"{job_config.env}\n")


    if job_config.commands:
        text.append("Shell Commands:  \n", style=ROBBIE_BLUE)
        for cmd in job_config.commands:
            text.append(f'{cmd}\n')
    
    console.print(Panel(
        text,
        box=box.ROUNDED,
        # padding=(1, 2),
        title = Text(f"Robbie Run Configuration ({job['tokenRatePerHour']} tokens/hour)", style=ROBBIE_ORANGE),
        border_style=ROBBIE_ORANGE,
    ))

def print_job_details_banner(job: dict):
    ## print job details
    text = Text()
    text.append("Run Name: ", style=ROBBIE_BLUE)
    text.append(f"{job['name']}\n")
            
    text.append("Run ID: ", style=ROBBIE_BLUE)
    text.append(f"{job['id']}\n")
        
    text.append("Start Time: ", style=ROBBIE_BLUE)
    text.append(f"{time.asctime()}")

    console.print(Panel(
        text,
        box=box.ROUNDED,
        title=Text("Run Details", style=ROBBIE_ORANGE),
        border_style=ROBBIE_ORANGE,
    ))
    
# prints a rich job completion banner
def print_job_complete_banner(job: dict, start):
    ## print job details
    text = Text()
    text.append("Job Name: ", style=ROBBIE_BLUE)
    text.append(f"{job['name']}\n")
            
    text.append("Total time: ", style=ROBBIE_BLUE)
    text.append(f"{time.perf_counter() - start:.2f} seconds.\n")
        
    text.append("Tokens consumed: ", style=ROBBIE_BLUE)
    text.append(f"{job['tokensUsed']}\n")
        
    text.append("RESULT: ")
    if(job['status'] == "complete"):
        text.append(f"Success", style="green")
    else:
        text.append(f"{job['status']}", style="red")
                
    console.print(Panel(
        text,
        box=box.ROUNDED,
        # padding=(1, 2),
        title=Text("Run Complete", style=ROBBIE_ORANGE),
        border_style=ROBBIE_ORANGE,
    ))

def print_known_error(e: RemoteCallException):
    logger.debug(e, exc_info=True)
    console.print(f"[red]An error has occurred: {e.user_friendly_message}[/red]")
    if e.additional_help:
        console.print(f"[yellow]{e.additional_help}[/yellow]")
