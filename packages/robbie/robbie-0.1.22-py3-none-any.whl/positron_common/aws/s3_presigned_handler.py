import requests

from positron_common.env_config import env
from positron_common.exceptions import RemoteCallException, DecoratorException
from positron_common.constants import temp_path
from ..cli.logging_config import logger


class S3PresignedHandler():
    """This class is responsible for handling file transfer 
       to and from Amazon S3 trough presigned URLs."""

    @staticmethod
    def upload_bytes_to_job_folder(bytes, job_id, path):
        presigned_resp = S3PresignedHandler._get_upload_presigned_url(job_id, path)
        
        # we need to create a temporary file from the bytes to upload it to s3
        filename = path.split('/')[-1]

        with open(f"{temp_path}/{filename}", 'wb') as f:
            f.write(bytes)
        with open(f"{temp_path}/{filename}", 'rb') as f:
            logger.debug(f'Uploading {filename} to {presigned_resp.get("url")}')
            response = requests.post(presigned_resp.get('url'), data=presigned_resp.get('fields'), files={"file": (filename, f)}) 
            if response.status_code != 204:
                raise DecoratorException(
                    f'Upload failed with http code: {response.status_code} \n {response.text}')
            


    @staticmethod
    def upload_file_to_job_folder(file_path, job_id, path):
        presigned_resp = S3PresignedHandler._get_upload_presigned_url(job_id, path)

        with open(file_path, 'rb') as f:
            files = {'file': (path, f)}
            response = requests.post(presigned_resp.get('url'), data=presigned_resp.get('fields'), files=files)
            logger.debug(response)
            if response.status_code != 204:
                raise DecoratorException(
                    f'Upload failed with http code: {response.status_code} \n {response.text}')


    @staticmethod
    def download_file_to_bytes(job_id, s3_path):
        presigned_resp = S3PresignedHandler._get_download_presigned_url(job_id, s3_path)
        resp = requests.get(presigned_resp.get('url'))
        if resp.status_code != 200:
            return None
        else:
            return resp.content


    @staticmethod
    def _get_upload_presigned_url(job_id, filename):
        Headers = {"PositronAuthToken": env.USER_AUTH_TOKEN, "PositronJobId": job_id}
        url = f'{env.API_BASE}/generate-presigned-url?filename={filename}'
        logger.debug(f'Calling: {url}')
        response = requests.get(url, headers=Headers)
        logger.debug(response)
        if response.status_code != 200:
            raise RemoteCallException(f'Presigned url fetching failed with http code: {response.status_code} \n {response.text}')
        else:
            logger.debug(response.json())
            return response.json()

    @staticmethod
    def _get_download_presigned_url(job_id, filename):
        Headers = {"PositronAuthToken": env.USER_AUTH_TOKEN, "PositronJobId": job_id}
        url = f'{env.API_BASE}/generate-download-url?filename={filename}'
        logger.debug(f'Calling: {url}')
        response = requests.get(url, headers=Headers)
        logger.debug(response)
        if response.status_code != 200:
            raise RemoteCallException(
                f'Presigned url fetching failed with http code: {response.status_code} \n {response.text}')
        else:
            logger.debug(response.json())
            return response.json()