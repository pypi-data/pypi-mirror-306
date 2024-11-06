import select
import subprocess
import requests
import time
import threading
from datetime import datetime, timezone
from positron_common.exceptions import RobbieException
from positron_common.enums import JobRunType
from positron_job_runner.runner_env import runner_env
from positron_job_runner.cloud_logger import logger
from positron_job_runner.remote_function import RemoteFunction
from positron_job_runner.workspace import unpack_workspace_from_s3, upload_results_to_s3

'''_______________________________________________________________________________________
    
    INITIALIZING CONFIGURATION AND CONSTANTS
    ______________________________________________________________________________________
'''

# Define API endpoints
API_BASE = runner_env.API_ENDPOINT
API_GET_JOB = f'{API_BASE}/get-job'
API_UPDATE_JOB = f'{API_BASE}/update-job'
API_JOB_LIFECYCLE = f'{API_BASE}/check-lifecycle'

# Define cross component enums
job_statuses = dict(
    pending="pending",
    uploading="uploading",
    in_queue="in_queue",
    launching="launching_pod",
    pulling_image="pulling_image",
    pulled_image="pulled_image",
    starting_container="starting_container",
    started_container="started_container",
    initializing="initializing",
    computing="computing",
    storing="storing",
    complete="complete",
    failed="failed",
    execution_error="execution_error",
    terminate="terminate_job",
    terminated="terminated"
)

# Job management
running_job = None
final_status = job_statuses['complete']

# Request header
headers = {
    "PositronJobId": runner_env.JOB_ID,
    "SystemAuthenticationKey": runner_env.SYSTEM_AUTHENTICATION_KEY,
}

'''_______________________________________________________________________________________
    
    SUB MODULES
    ______________________________________________________________________________________
'''
# Get Job -----------------------------------------------------------
def get_job():
    logger.info('Fetching job details')
    resp = try_request(requests.get, API_GET_JOB, headers=headers)
    job = resp.json()
    return job

# Run Job -----------------------------------------------------------
def run_job(job: dict):
    logger.info('Starting job')
    update_job(status=job_statuses["computing"])
    
    job_type_str = job.get('entryPoint')
    logger.debug(f"Running job with type: {job_type_str}")
    job_type = JobRunType[job_type_str]
    if job_type == JobRunType.BASH_COMMAND_RUNNER:
        run_commands(job)
        return
    if job_type == JobRunType.REMOTE_FUNCTION_CALL:
        run_remote_function_job(job)
        return
    if job_type == None:
        raise RobbieException(f"Job type was not set. This could be a compatibility issue with the robbie library.")
    raise RobbieException(f"Unknown job type of: '{job_type}'!")


def run_commands(job: dict):
    command: str = job.get('commands')
    logger.debug(f'Found commands to execute:\n{command}')
    command_prefix = 'cd .. && python -m venv venv && . venv/bin/activate && cd job-execution'
    full_command = f"{command_prefix} && {command}"
    logger.debug(f"Full command: {full_command}")
    start_and_monitor_job(full_command)


def run_remote_function_job(job: dict):
    # Determine which cli to install
    robbie_local_cli_cmd = f"[ -d \"{runner_env.ROBBIE_CLI_PATH}\" ] && echo 'Installing local robbie cli...' && pip install {runner_env.ROBBIE_CLI_PATH}"
    robbie_env_cli_cmd = "echo 'Installing robbie' && pip install robbie"
    if (runner_env.POSITRON_CLI_ENV == "development"):
        robbie_env_cli_cmd = "echo 'Installing robbie:dev' && pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ --pre robbie"
    if (runner_env.POSITRON_CLI_ENV == "test"):
        robbie_env_cli_cmd = "echo 'Installing robbie:test' && pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ robbie"
    install_robbie_cmd = f"{robbie_local_cli_cmd} || {robbie_env_cli_cmd}"

    enter_env = "python -m venv venv && . venv/bin/activate"
    install_requirements = "[ -f requirements.txt ] && pip install -r requirements.txt || echo 'No requirements to install'"

    # Construct the command
    # By putting the install_robbie_cmd at the end, we ensure the latest version of robbie is installed,
    # overriding any version in the requirements.txt
    command_base = " && ".join([
        enter_env,
        install_requirements,
        install_robbie_cmd,
    ])

    logger.info('Downloading function and arguments')
    rm = RemoteFunction()
    rm.setup()

    meta = job.get('meta', {})
    job_arguments = meta.get('jobArguments', [])

    # Join job arguments with spaces
    arguments_string = ' '.join(job_arguments)

    # Construct the execution command
    execution_command = f"{rm.run_cmd} {arguments_string}"

    # Log the execution command
    logger.info(f"Installing Dependencies and running: {execution_command}")

    # Combine the base command with the execution command
    full_command = f"{command_base} && {execution_command}"
    logger.debug(f"Full command: {full_command}")
    start_and_monitor_job(full_command)


def start_and_monitor_job(command: str):
    sub_env = runner_env.env_without_runner_env()
    logger.debug(f'Running client job with job environment: {sub_env}')

    # Start job
    global running_job
    if (runner_env.JOB_USER != 'job_user'):
        logger.debug('Running job as current user')
        running_job = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,                # allows running on any os
            universal_newlines=True,   # otherwise stdout and stderr will be bytes
            cwd=runner_env.JOB_CWD,
        )
    else:
        logger.debug('Running job as protected user')
        running_job = subprocess.Popen(
            ["su", "-c", command, "-s", "/bin/bash", runner_env.JOB_USER],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            # requires elevated permissions which is not allowed in the runtime environment.
            # shell=True,
            cwd=runner_env.JOB_CWD,
            env=sub_env,
        )

    logger.debug(f"Job started with PID: {running_job.pid}")

    # Start parallel threads
    stop_event = threading.Event()
    log_stop_event = threading.Event()
    logger.debug("Starting threads...")
    termination_thread = start_termination_thread(stop_event)
    charge_thread = start_charging_thread(stop_event)
    stdout_thread = threading.Thread(target=logging_thread, args=(running_job.stdout, "stdout", log_stop_event)); stdout_thread.start()
    stderr_thread = threading.Thread(target=logging_thread, args=(running_job.stderr, "stderr", log_stop_event)); stderr_thread.start()

    logger.info("Waiting for job to complete")
    running_job.wait()
    return_code = running_job.returncode
    stop_event.set()
    if return_code == -9:
        # Force stop
        log_stop_event.set()
        logger.warn("Job process terminated. Shutting down open threads...")
        logger.warn("Some of your logs will be lost.")
    else:
        logger.info(f"Job completed with code: {return_code}. Waiting for threads to finish processing...")
        # Note: Streaming stdout will take much longer to process than the actual process itself.
        stdout_thread.join()
        stderr_thread.join()

    # Wait for charging and termination thread to finish.
    charge_thread.join()
    termination_thread.join()
    logger.debug("Job run completed.")

    global final_status
    return_code = running_job.returncode
    if final_status != job_statuses['terminated'] and return_code > 0: final_status = job_statuses["execution_error"]

def decode_if_bytes(line):
    return line.decode('utf-8') if isinstance(line, bytes) else line

# Finish Job --------------------------------------------------------
def finish_job(job: dict):
    logger.info("Finishing job")
    out_str = '\n'.join(decode_if_bytes(line) for line in logger.stdout)
    err_str = '\n'.join(decode_if_bytes(line) for line in logger.stderr)

    tokens_used = job['tokensUsed']

    if tokens_used:
        tokens_used_msg = f'Total tokens used for processing job: {tokens_used}'
        logger.info(tokens_used_msg)
        out_str += f'\n{tokens_used_msg}'

    logger.debug(f"Updating job with logs: output log size: {len(out_str)}, error log size: {len(err_str)}")

    update_job(status=final_status, end_date=datetime.now(timezone.utc), output_log=out_str, error_log=err_str)
    
    # Shared backend checks for this signal to terminate socket connection
    logger.info("Job successfully completed.")
    logger.end_of_logs_signal()


'''_______________________________________________________________________________________
    
    UTILS
    ______________________________________________________________________________________
'''
# Check for termination ---------------------------------------------
def is_job_active():
    if (runner_env.rerun):
        return True

    resp = try_request(requests.get, API_GET_JOB, headers=headers)
    db_job = resp.json()
    inactive_statuses = [
        job_statuses["complete"],
        job_statuses["failed"],
        job_statuses["execution_error"],
        job_statuses["terminate"],
        job_statuses["terminated"],
    ]

    if db_job['status'] not in inactive_statuses:
        return True

    global final_status
    if db_job['status'] == job_statuses["terminate"]:
        final_status = job_statuses["terminated"]
        logger.info("The job has been terminated by the user.")
    else:
        final_status = db_job['status']
        logger.info(f"The job is not active anymore (status: {db_job['status']})")

    return False


# Update Job --------------------------------------------------------
def update_job(status, start_date=None, end_date=None, output_log=None, error_log=None):
    logger.debug(f'Updating status: {status}')
    body={
        "status": status,
        "startDate": start_date.isoformat() if start_date is not None else None,
        "endDate": end_date.isoformat() if end_date is not None else None,
        "outputLog": output_log,
        "errorLog": error_log
    }
    # filter out the items where the value is None
    body = {key:value for key, value in body.items() if value is not None}
    try_request(requests.post, API_UPDATE_JOB, headers=headers, json_data=body)

# Charging thread ---------------------------------------------------
def start_charging_thread(stop_event: threading.Event):
    logger.debug('Start charging thread')
    def charge_thread():
        while not stop_event.is_set():
            res = try_request(requests.post, API_JOB_LIFECYCLE, headers=headers)
            if res is None:
                # stop looping, job is forced to terminate by try_request
                break
            j = res.json()
            if not j['succeeded']:
                # unable to validate job lifecycle due to known reason (e.g. insufficient funds, time/token limit exceeded)
                logger.error(f"Job lifecycle error! Response message: {j['message']} ")

            # @Todo: discuss if job should be charged for every computational minute that is started, i.e. if termination occurs
            # between two charge calls, should we charge for the minute that was started but not completed?
            stop_event.wait(runner_env.POSITRON_CHARGE_INTERVAL)
        logger.debug('Charging thread stopped')
    ct = threading.Thread(target=charge_thread)
    ct.start()
    return ct


# Termination thread ------------------------------------------------
def start_termination_thread(stop_event: threading.Event):
    logger.debug('Starting termination thread')
    def termination_thread():
        while not stop_event.is_set():
            res = try_request(requests.get, API_GET_JOB, headers=headers)
            if res is None:
                # stop looping, job is forced to terminate by try_request
                break
            j = res.json()
            if j['status'] == job_statuses['terminate']:
                logger.debug(f"Job status: {job_statuses['terminate']}, terminating job...")
                terminate_running_job()
                global final_status; final_status = job_statuses["terminated"]
                break
            stop_event.wait(runner_env.POSITRON_CHECK_TERMINATION_INTERVAL)
        logger.debug('Termination thread stopped')

    tt = threading.Thread(target=termination_thread)
    tt.start()
    return tt


# Logging thread ----------------------------------------------------
def logging_thread(pipe, stream_name: str, stop_event: threading.Event):
    try:
        with pipe:
            while not stop_event.is_set():
                # Calling pipe.readline() will hang the process until a new line is available
                # however, if no new lines are available, we want to check if the thread should stop
                ready, _, _ = select.select([pipe], [], [], 0.1)
                if ready:
                    # TODO: Can I iterate over the pipe and process everything that's ready?
                    line = pipe.readline()
                    if not line:
                        break
                    if line.strip():
                        if stream_name == "stdout":
                            logger.info("job stdout: " + line.rstrip())
                        else:
                            logger.error("job stderr: " + line.rstrip())
                else:
                    time.sleep(0.01)
            # TODO: Do we need to check one more time for outstanding data in the pipe?
            logger.debug(f'Logging thread for: {stream_name} stopped')
    except Exception as e:
        logger.error(f'Logging thread for: {stream_name} stopped with exception: {e}')


# Terminate running job ---------------------------------------------
def terminate_running_job():
    global running_job
    # Signal termination
    if (running_job is not None) and (running_job.poll() is None):
        logger.warn("Forcefully terminating running job...")
        running_job.kill()
        running_job.wait()
        return_code = running_job.returncode
        logger.debug(f"Job process existed with return code: {return_code}")


# Retry API requests ------------------------------------------------
def try_request(request_func, url, retries=2, headers=None, json_data=None):
    for attempt in range(retries):
        try:
            response = request_func(url, headers=headers, json=json_data)
            response.raise_for_status()  # Raise an error for 4xx and 5xx status codes
            return response
        except requests.RequestException as e:
            logger.debug(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                logger.debug("Retrying...")
                time.sleep(2)  # Adding a delay before retrying
            else:
                logger.debug("Max retries reached, terminating job.")
                terminate_running_job()
                raise RobbieException(f"Failed to make request to {url} after {retries} attempts.")


'''_______________________________________________________________________________________
    
    RUN!
    ______________________________________________________________________________________
'''
def run():
    try:
        # 1. Get the job details
        job = get_job()

        if is_job_active():
            # 2. Update status to initializing
            update_job(status=job_statuses["initializing"], start_date=datetime.now(timezone.utc))

            # 3. Unpack workspace tar
            if is_job_active():
                unpack_workspace_from_s3()

                # 4. Run the job (including dependency install)
                if is_job_active():
                    run_job(job)

                    # 5. Update status to Storing
                    update_job(status=job_statuses['storing'])

                    # 6. Upload results
                    upload_results_to_s3()

        # 7. Get the completed job details
        job = get_job()
        # 8. Update status to success or error
        finish_job(job)

    except Exception as e:
        logger.error(f'Job stopped. An exception occurred: {str(e)}.')
        logger.end_of_logs_signal()
        raise e

        
