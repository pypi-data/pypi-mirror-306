from positron_job_runner.runner_env import runner_env
from positron_job_runner.cloud_logger import logger
from positron_job_runner.cloud_storage import cloud_storage
from positron_common.deployment.meta_data import MetaData
from positron_common.deployment.serializer import Serializer

class RemoteFunction():
  """Fetches the function to execute from cloud storage."""

  run_cmd: str = "python -m positron_job_runner.lil_byter"
  s3_base_path = f"{runner_env.JOB_OWNER_EMAIL}/{runner_env.JOB_ID}"

  def setup(self):
    logger.info("Fetching function to execute...")

    meta_contents = cloud_storage.get_object(f"{self.s3_base_path}/function/metadata.json")
    metadata = MetaData.from_json(meta_contents)

    # TODO: use positron_common enum s3_constants
    self._get_resource('function.pkl', metadata.sha256_hash.get('func_hash'))
    self._get_resource('args.pkl', metadata.sha256_hash.get('args_hash'))
    self._get_resource('kwargs.pkl', metadata.sha256_hash.get('kwargs_hash'))

    logger.info("Function successfully retrieved and validated.")

  def _get_resource(self, resource_name: str, resource_hash: str):
    # TODO: use positron_common enum s3_constants
    contents = cloud_storage.get_object(f"{self.s3_base_path}/function/{resource_name}")
    computed_hash = Serializer.compute_hash(contents, secret_key=runner_env.REMOTE_FUNCTION_SECRET_KEY)
    if computed_hash != resource_hash:
      raise Exception(f"Integrity check for: {resource_hash} failed! Ensure your User Auth Token is up to date and no one has access to your cloud storage.")

    # Write to disk so subprocess can run it.
    with open(f"{runner_env.JOB_CWD}/{resource_name}", "wb") as f:
      f.write(contents)

    logger.info(f"Downloaded {resource_name}")


if __name__ == "__main__":
  rf = RemoteFunction()
  rf.setup()
