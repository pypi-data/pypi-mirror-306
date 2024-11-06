from positron_common.utils import _current_python_version
from positron_common.constants import *
from positron_common.env_defaults import current
from positron_common.cli.logging_config import logger
from positron_common.job_api.funding_envs_images import *

# used to construct the image name
IMAGE_VERSION = '1.0.0'
BASE_NAME = "robbie"
LINUX_VERSION = "ubuntu22.04"

DEFAULT_PYTORCH_VERSION_GPU = {
    "py3.9": "2.0",
    "py3.10": "2.2",
    "py3.11": "2.4",
    "py3.12": "2.5",
}

DEFAULT_PYTORCH_VERSION_CPU = {
    "py3.9": "1.13",
    "py3.10": "2.2",
    "py3.11": "2.4",
    "py3.12": "2.5",
}

def get_auto_image_name_and_cluster(fs_id: str, env_id: str):
    """
    Constructs an image name based on the current environment, chosen cluster, and python version
    """
    logger.debug(f"get_auto_image_name_and_cluster(): {fs_id}, {env_id}")

    gpu_count, cluster_type = get_gpu_count_and_cluster_from_env(fs_id, env_id)
    # if there are GPUs in the environment, use the GPU image
    if gpu_count:
        type = "gpu"
    else:
        type = "cpu"
    logger.debug(f"type: {type}")

    # if running local use dev images
    if current.name == "localhost":
        env = "dev"
    else:
        env = current.name

    python_version = f"py{_current_python_version()}"
    logger.debug(f"Python version string: {python_version}")
    if type == "gpu" and not DEFAULT_PYTORCH_VERSION_GPU.get(python_version):
        logger.debug(f"No default PyTorch GPU version found for: {python_version}")
        return None, None
    if (type == "cpu" and not DEFAULT_PYTORCH_VERSION_CPU.get(python_version)):
        logger.debug(f"No default PyTorch CPU version found for: {python_version}")
        return None, None
    
    torch_version = DEFAULT_PYTORCH_VERSION_GPU.get(python_version) if type == "gpu" else DEFAULT_PYTORCH_VERSION_CPU.get(python_version)
    image_name = f"{BASE_NAME}:{IMAGE_VERSION}-{type}-{python_version}-torch{torch_version}-{LINUX_VERSION}-{env}"
    logger.debug(f"Automatically generated image name: {image_name}")
    return image_name, cluster_type

    
   
def get_gpu_count_and_cluster_from_env(fs_id: str, env_id: str):
    """ Gets the cluster type from the environment """
    envs = list_environments(fs_id)
    if len(envs) == 0:
        return None, None
    for _, val in envs.items():
        if(val.get(ENV_ID) == env_id):
            logger.debug(f"Environment: {val.get(ENV_NAME)}, Id: {val.get(ENV_ID)}, Cluster type: {val.get(ENV_CLUSTER_TYPE)}, GPU count: {val.get(ENV_GPU_NUMBER)}")
            return val.get(ENV_GPU_NUMBER), val.get(ENV_CLUSTER_TYPE)
    return None, None

      