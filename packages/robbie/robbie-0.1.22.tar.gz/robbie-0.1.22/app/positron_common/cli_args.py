from pydantic import BaseModel
from typing import List, Optional
from positron_common.cli.console import console

class PositronCLIArgs(BaseModel):
    """
    Positron CLI command line arguments.
    """
    is_init: bool = False
    name: Optional[str] = None
    local: bool = False
    deploy: bool = False
    stream_stdout: bool = False
    job_args: Optional[List[str]] = None
    skip_prompts: bool = False
    monitor_status: bool = False
    commands_to_run: Optional[str] = None
    interactive: bool = False
    create_only: bool = False
    results_from_job_id: str = ""
    download: Optional[str] = None
    local_path: Optional[str] = None
    auto_capture_deps: bool = False


    def init(self,
        name: Optional[str] = None,
        local: bool = False,
        deploy: bool = False,
        stream_stdout: bool = False,
        job_args: Optional[List[str]] = None,
        skip_prompts: bool = False,
        monitor_status: bool = False,
        commands_to_run: Optional[str] = None,
        interactive: bool = False,
        create_only: bool = False,
        results_from_job_id: str = "",
        download: Optional[str] = None,
        local_path: Optional[str] = None,
        auto_capture_deps: bool = False
    ):
        if self.is_init:
            raise ValueError('CLI Args already initialized')
        
        self.name = name
        self.local = local
        self.deploy = deploy
        self.stream_stdout = stream_stdout
        self.job_args = job_args
        self.is_init = True
        self.skip_prompts=skip_prompts
        self.monitor_status=monitor_status
        self.commands_to_run = commands_to_run
        self.interactive = interactive
        self.create_only = create_only
        self.results_from_job_id = results_from_job_id
        self.download = download
        self.local_path = local_path
        self.auto_capture_deps = auto_capture_deps

    def dump(self):
        console.print(f'[bold]CLI Arguments[/bold]')
        console.print(f'name: {self.name}')
        console.print(f'local: {self.local}')
        console.print(f'deploy: {self.deploy}')
        console.print(f'stream_stdout: {self.stream_stdout}')
        console.print(f'job_args: {self.job_args}')
        console.print(f'skip_prompts: {self.skip_prompts}')
        console.print(f'monitor_status: {self.monitor_status}')
        console.print(f'commands_to_run: {self.commands_to_run}')
        console.print(f'interactive: {self.interactive}')
        console.print(f'create_only: {self.create_only}')
        console.print(f'results_from_job_id: {self.results_from_job_id}')
        console.print(f'download: {self.download}')
        console.print(f'local_path: {self.local_path}')
        console.print(f'auto_capture_deps: {self.auto_capture_deps}')
        console.print(f'is_init: {self.is_init}')
        


#
# Export global (singleton)
#
args = PositronCLIArgs()
"""
Global CLI arguments singleton, make sure you call init() before using it.
"""
