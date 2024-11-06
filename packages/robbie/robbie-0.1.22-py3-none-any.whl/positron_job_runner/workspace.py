import zipfile
import tarfile
import os
from positron_common.compression import get_file_paths
from positron_common.constants import FILE_SIZE_THRESHOLD
from positron_job_runner.runner_env import runner_env
from positron_job_runner.cloud_storage import cloud_storage
from positron_job_runner.cloud_logger import logger

EXCLUDED_DIRECTORIES = ['venv', '.venv', '.git', '__pycache__', 'job-execution', '.robbie', '.ipynb_checkpoints', 'persistent-disk']
S3_BASE_PATH = f"{runner_env.JOB_OWNER_EMAIL}/{runner_env.JOB_ID}"
S3_RESULT_PATH = f"{S3_BASE_PATH}/result"

def unpack_workspace_from_s3():
    """Unpacks the workspace from S3"""
    s3_key = f"{S3_BASE_PATH}/workspace.tar.gz"
    try:
        local_tar_path = os.path.join(runner_env.RUNNER_CWD, 'workspace.tar.gz')
        cloud_storage.download_file(s3_key, local_tar_path)

        logger.info('Unpacking workspace')
        with tarfile.open(local_tar_path) as tar:
            tar.extractall(runner_env.JOB_CWD)
        logger.info('Workspace unpacked successfully')

    except Exception as e:
        logger.error(f"Failed to unpack workspace from S3: {e}")

def upload_results_to_s3():
    """Uploads the results to S3"""
    try:
        logger.info('Copying results to cloud storage...')

        results_dir = runner_env.JOB_CWD
        os.makedirs(results_dir, exist_ok=True)

        result_files = get_file_paths(path=results_dir, excluded_dirs=EXCLUDED_DIRECTORIES)

        # Create a tar.gz of the result directory
        results_zip_file_name = f"{results_dir}/result.zip"
        with zipfile.ZipFile(results_zip_file_name, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file in result_files:
                logger.debug(f"Adding to zip: {file.name}")
                zipf.write(file.full_path, arcname=file.name)

        file_size = os.path.getsize(results_zip_file_name)
        if (file_size >= FILE_SIZE_THRESHOLD):
            size_in_mb = round(file_size / (1024 * 1024), 2)
            logger.warn(f"Size: {size_in_mb} Mb. It might take a long time to upload it.")

        logger.debug(f"Uploading to cloud storage: {results_zip_file_name}")
        cloud_storage.upload_file(results_zip_file_name, f"{S3_RESULT_PATH}/result.zip")

        # Upload raw files to S3
        for file in result_files:
            logger.debug(f"Uploading to cloud storage: {file.name}")
            s3_key = f"{S3_RESULT_PATH}/{file.name}"
            cloud_storage.upload_file(file.full_path, s3_key)

        logger.info('Results uploaded to S3 successfully')

    except Exception as e:
        logger.error(f"Failed to upload results to S3: {e}")
