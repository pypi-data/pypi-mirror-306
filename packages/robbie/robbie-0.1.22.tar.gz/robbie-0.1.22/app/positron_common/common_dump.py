import sys
import os
import subprocess
from positron_common.cli.console import console
from positron_common.build_env import build_env
from positron_common.utils import get_version
from positron_common.env_defaults import current
from positron_common.env_config import env
from positron_common.user_config import user_config
from positron_common.cli_args import args

def common_dump():
    console.print(f"====================BEGIN=======================")
    console.print(f"==========[bold]Python executable (sys.executable)[/bold]=========")
    console.print(sys.executable)
    console.print(f"==========[bold]Python executable (os.__file__)[/bold]==========")   
    console.print(os.__file__)
    console.print(f"==========[bold]importlib.metadata.version('robbie')[/bold]==========")
    console.print(get_version())
    console.print(f"==========[bold]pip show robbie[/bold]==========")
    result = subprocess.run(["pip", "show", "robbie"], capture_output=True, text=True)
    console.print(result.stdout)
    console.print(f"==========[bold]build_env[/bold]=========")
    console.print(build_env)
    console.print(f'==========[bold]env[/bold]============')
    env.dump()
    console.print(f"==========[bold]current[/bold]==========")
    current.dump()
    console.print(f"==========[bold]user_config[/bold]==========")
    user_config.dump()
    console.print(f"==========[bold]args[/bold]==========")
    args.dump()
    console.print(f"====================END=======================")
