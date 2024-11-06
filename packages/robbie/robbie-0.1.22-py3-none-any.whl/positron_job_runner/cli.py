import typer
from typing import Annotated
from .run_job import run
from .runner_env import runner_env
from .cloud_logger import logger

app = typer.Typer(help="Runs your job from the Positron Cloud environment.")

@app.command()
def hello():
    """
    Describes what you can do with the Positron Job Runner
    """
    logger.info('Hello, I am the Positron Job Runner')
    logger.info('Here is a list of thing I can help you with:')
    logger.info('- Run a job in the Positron Cloud')

@app.command()
def run_job(
    rerun: Annotated[bool, typer.Option(help='Enables rerunning a job')] = False,
):
    """
    Run the job from inside a Positron container.

    Example usage:
    $ positron_job_runner run_job
    """
    # @TODO: Validate that all necessary env variables are correctly set (JOB_ID...)

    logger.info('Running job in the Positron Cloud')
    logger.info(f'Job ID: {runner_env.JOB_ID}')
    runner_env.rerun = rerun

    logger.debug(f"Wrapper env: {runner_env}")

    try:
        run()
    except Exception as e:
        logger.exception(e)
        exit(0)


if __name__ == "__main__":
    app()
