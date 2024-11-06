from rich import print
from positron_common.cli.interactive import prompt_and_build_positron_job_config
from positron_common.constants import JOB_CONF_YAML_PATH

def configure() -> None:
    """
    Build a Robbie job configure file (job_config.yaml) interactively.

    """
    print("Please follow the prompts to build a 'job_config.yaml' in your current directory.")
    print("Values in brackets [] are default, use the <tab> key to see a menu of options.\n")
    
    cfg = prompt_and_build_positron_job_config()

    if cfg:
        cfg.write_to_file(filename=JOB_CONF_YAML_PATH)
        print(f"[green] Successfully wrote config file {JOB_CONF_YAML_PATH}'")
        print(f"[yellow]---------- Contents ----------")
        print(cfg)
        print(f"[yellow]---------- End ----------")




    
