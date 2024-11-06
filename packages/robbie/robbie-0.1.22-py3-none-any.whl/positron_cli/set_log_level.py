import typer
from typing import Optional
from logging import _nameToLevel
from positron_common.cli.logging_config import set_log_level

def log_level(
    loglevel: Optional[str] = typer.Option(
        None, help="Set the logging level [CRITICAL,FATAL,ERROR, WARNING, INFO, DEBUG, NOTSET]"
    ),
):
    set_log_level(loglevel)