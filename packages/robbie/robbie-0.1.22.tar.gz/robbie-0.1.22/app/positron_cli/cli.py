import typer
from positron_cli.run import run
from positron_cli.login import login
from positron_cli.set_env import set_env
from positron_cli.configure import configure
from positron_cli.download import download
from positron_cli.set_log_level import log_level
from positron_cli.version import version
from positron_cli.cmd_dump import dump
from positron_common.cli.console import console
import pyfiglet
  
ascii_banner = pyfiglet.figlet_format("Robbie")
console.print(ascii_banner, style='#41a7ff')
app = typer.Typer(help="A CLI tool to help you run your code in the Robbie")

app.command()(dump)
app.command()(run)
app.command()(login)
app.command()(set_env)
app.command()(configure)
app.command()(download)
app.command()(version)
app.callback()(log_level)

if __name__ == "__main__":
    app()
