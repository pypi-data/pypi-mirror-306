import asyncio
import socketio
import nest_asyncio
import json
import time
from positron_common.env_config import env
from positron_common.exceptions import RobbieException
from ..cli.console import console, ROBBIE_BLUE
from ..cli.logging_config import logger

sio = socketio.AsyncClient()
nest_asyncio.apply() # enabled nested event loops

@sio.event(namespace='/stdout-stream')
async def connect():
    console.print("Connected to your run's log stream!")

@sio.event(namespace='/stdout-stream')
async def message(message: str):
    try:
        log: dict = json.loads(message)
        level_name = log.get('log_level')
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S:%MS", time.gmtime(log.get('timestamp') / 1000))
        message = log.get('message')
        level_string = level_name.ljust(8)
        logger_name = log.get('app_name')

        if level_name == "INFO":
            level_string = f"[green]{level_name}[/green]"
        elif level_name == "DEBUG":
            level_string = f"[blue]{level_name}[/blue]"
        elif level_name == "ERROR":
            level_string = f"[red]{level_name}[/red]"
        elif level_name == "WARNING":
            level_string = f"[yellow]{level_name}[/yellow]"

        formatted_log = f"{logger_name}: {timestamp} {level_string}: {message}"
        console.print(formatted_log)
    except:
        console.print(log['message'], style=ROBBIE_BLUE)

@sio.event(namespace='/stdout-stream')
async def disconnect():
    console.print('Disconnected from stdout stream')

@sio.event(namespace='/stdout-stream')
async def error(err):
    console.print('An error occurred in the streaming process')
    logger.error(err)

async def start_stream(job_id: str):
    custom_headers = {
        "PositronAuthToken": env.USER_AUTH_TOKEN,
        "PositronJobId": job_id
    }
    await sio.connect(env.SOCKET_IO_DOMAIN, headers=custom_headers, socketio_path=env.SOCKET_IO_PATH)
    # TODO: I don't think we want to actually do this long term.
    await sio.wait()

def start_stdout_stream(job_id: str):
    try:
        # Start the stream
        asyncio.get_event_loop().run_until_complete(start_stream(job_id))
    except Exception as error:
        raise RobbieException(error)


