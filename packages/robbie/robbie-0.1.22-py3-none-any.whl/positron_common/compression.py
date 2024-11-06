import time
from dataclasses import dataclass
import os
import tarfile
from typing import List
from rich.tree import Tree
from rich.panel import Panel
from rich import box
from rich.text import Text
from positron_common.env_config import env
from positron_common.constants import temp_path
from rich.prompt import Confirm
from positron_common.cli.console import console, ROBBIE_YELLOW
from positron_common.cli.logging_config import logger
from positron_common.constants import FILE_SIZE_THRESHOLD

@dataclass
class FileEntry:
    full_path: str
    name: str
    size: int

def get_file_paths(path: str, excluded_dirs: List[str], excluded_files: List[str] = []) -> List[FileEntry]:
    """should return a list relative paths that should included in the results"""
    all_files: List[FileEntry] = []
    for root, dirs, files in os.walk(path):
        for exclude_dir in excluded_dirs:
            try:
                dirs.remove(exclude_dir)
            except ValueError:
                pass
        for file in files:
            if file in excluded_files:
                continue
            full_path = os.path.join(root, file)
            file_size = os.path.getsize(full_path)
            rel_path = os.path.relpath(full_path, path)
            all_files.append(FileEntry(name=rel_path, size=file_size, full_path=full_path))
    return all_files

def check_workspace_dir(workspace_dir: str):
    if not os.path.exists(workspace_dir):
        question_prompt = f"Directory '{workspace_dir}' does not exist. Would you like to create it?"
        if Confirm.ask(f'{question_prompt}', default=True):
            os.makedirs(workspace_dir)
            return True
        console.print("[yellow]Either update the 'workspace_dir' config or remove it to use the default of the current workspace.[/yellow]")
        return False
    return True

def create_workspace_tar(workspace_dir: str) -> int:
    tree = Tree("Local (workspace) files to copy to Remote Machine")
    path = f"{temp_path}/{env.COMPRESSED_WS_NAME}"
    last_files_compressed_count = 0

    if not os.path.exists(temp_path):
        os.makedirs(temp_path)

    excluded_dirs = ['venv', '.venv', '.git', '__pycache__', 'job-execution', ".robbie", ".ipynb_checkpoints", temp_path]
    files = get_file_paths(path=workspace_dir, excluded_dirs=excluded_dirs)

    logger.debug(f"Files to compress: {files}")
    with tarfile.open(path, 'w:gz') as tar:
        for file in files:
            if not file.name.endswith((".py", ".ipynb", ".yaml", ".csv", ".txt", ".pkl")):
                continue
            tree.add(f"[yellow]{file.name}, size: {file.size} bytes[/yellow]")
            last_files_compressed_count += 1
            tar.add(file.full_path, arcname=file.name)

    file_size = os.path.getsize(path)
    if (file_size >= FILE_SIZE_THRESHOLD):
        size_in_mb = round(file_size / (1024 * 1024), 2)
        text = Text(f"Size: {size_in_mb} Mb. It might take a long time to upload it.", style=ROBBIE_YELLOW)
        console.print(Panel(
            renderable=text,
            box=box.ROUNDED,
            title = Text("Workspace Archive Size Warning", style=ROBBIE_YELLOW),
            border_style=ROBBIE_YELLOW,
            padding=(1, 2),
        ))
        time.sleep(4)

    if last_files_compressed_count > 0:
        console.print(tree)
    return last_files_compressed_count
