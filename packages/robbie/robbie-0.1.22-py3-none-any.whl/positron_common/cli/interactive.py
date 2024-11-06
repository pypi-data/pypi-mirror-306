
import os
from positron_common.job_api.funding_envs_images import *
from positron_common.cli.console import console, ROBBIE_BLUE, ROBBIE_DEFAULT
from prompt_toolkit import prompt
from prompt_toolkit.styles import Style
from prompt_toolkit.validation import Validator
from prompt_toolkit.completion import WordCompleter, PathCompleter
from positron_common.config import PositronJob
from positron_common.config import PositronJobConfig
from positron_common.enums import JobRunType
from positron_common.image_name import get_auto_image_name_and_cluster


# Prompts the user for FGs, environmetns, etc.
# Queries the backend for the FundingSources and Environments.
def prompt_and_build_positron_job_config(preserve: bool = False
) -> PositronJobConfig:

    try:
        pj = PositronJob()

        style = Style.from_dict({
            'completion-menu.completion': 'bg:#008888 #ffffff',
            'completion-menu.completion.current': 'bg:#00aaaa #000000',
        })
        # user can enter a name

        message = [
            (ROBBIE_BLUE, "Please enter a custom run name ["),
            (ROBBIE_DEFAULT, "let Robbie choose"),
            (ROBBIE_BLUE, "]:" ),
        ]
        name_choice = prompt(message=message, style=style)
        if len(name_choice):
            pj.name = name_choice

        # fetch the names and ids
        fs = FundingSources.load()

        # validate the user input
        def is_fs_valid(text):
            return text == "" or text in fs.menu_items()
        fs_validator = Validator.from_callable(is_fs_valid, error_message='Please select a valid funding source.')

        message = [ 
            (ROBBIE_BLUE, "Select how to bill your job ["),
            (ROBBIE_DEFAULT, "Personal tokens"),
            (ROBBIE_BLUE, "]:" ),
        ]
        fs_choice = prompt(message=message, completer=WordCompleter(fs.menu_items()), style=style, validator=fs_validator)

        if len(fs_choice):
            fs_id = fs.id_from_menu_item(fs_choice)
            pj.funding_selection = "User Selected"
        else:
            fs_id = fs.default_funding_source_id()
            pj.funding_selection = "User Selected - Default"
            
        pj.funding_group_id = fs_id

        #
        # Envrionments
        #
        # are there any environments in this funding source?
        envs = Environments.load(pj.funding_group_id)

        # validate the user input
        def is_env_valid(text):
            return text == "" or text in envs.menu_items()
        env_validator = Validator.from_callable(is_env_valid, error_message='Please enter a valid environment.')

        if envs:
            message = [ 
                (ROBBIE_BLUE, "Select your preferred hardware ["),
                (ROBBIE_DEFAULT, "None" if not fs.default_env_name_from_fs_id(fs_id) else fs.default_env_name_from_fs_id(fs_id)), # this is null for personal
                (ROBBIE_BLUE, "]:" ),
            ]
            env_choice = prompt(message=message, completer=WordCompleter(envs.menu_items()), style=style, validator=env_validator)
        else:
            # no environments for the user oh well
            console.print(f"[red]Error your funding sources: {fs_choice} has no approved hardware, please contact 'support@robbie.run'")
            return None

        if len(env_choice):
            pj.environment_id = envs.id_from_menu_item(env_choice)
            pj.environment_selection = "User Selected"
        else:
            # choose the default, if available
            if fs.default_env_id_from_fs_id(fs_id) == None:
                console.print(f"[red] Error funding source: {fs_choice} has no default hardware and you didn't specify any.")
                return None
            else:
                pj.environment_id = fs.default_env_id_from_fs_id(fs_id)
                pj.environment_selection = "User Selected - Default"

        #
        # Images
        #
        images = Images.load(pj.funding_group_id, pj.environment_id)

        def is_image_valid(text):
            return text == "" or text in images.menu_items()
        
        image_validator = Validator.from_callable(is_image_valid, error_message='Please choose a valid image.')

        if images:
            message = [ 
                    (ROBBIE_BLUE, "Select your preferred image["),
                    (ROBBIE_DEFAULT, "auto-select"),
                    (ROBBIE_BLUE, "]:" ),
                ]
            image_choice = prompt(message=message, completer=WordCompleter(images.menu_items()), style=style, validator=image_validator)

            if len(image_choice):
                # the user hit tab and selected an image
                pj.image = images.name_from_menu_item(image_choice)
                # we just get the cluster type from the environment
                pj.cluster = envs.cluster_type_from_env_id(pj.environment_id)
                pj.image_selection = "User Selected"
            else:
                # the user just hit <return>, so auto-select
                pj.image, pj.cluster = get_auto_image_name_and_cluster(pj.funding_group_id, pj.environment_id)
                console.print('Auto-selecting image:', style=ROBBIE_BLUE, end="")
                console.print(f'{pj.image} on cluster {pj.cluster}')
                pj.image_selection = "Automatically Selected"
        else:
            # no environments for the user oh well
            console.print(f"[red]Failed to get images, please contact 'support@robbie.run'")
            return None
        #
        # Dependencies
        #
        def is_dependency_valid(text):
            return text == "" or text in ["auto-capture", "./requirements.txt"]
        
        dependency_validator = Validator.from_callable(is_dependency_valid, error_message='Please choose a valid selection.')
        message = [ 
                (ROBBIE_BLUE, "Dependencies["),
                (ROBBIE_DEFAULT, "none"),
                (ROBBIE_BLUE, "]:" ),
            ]
        deps = prompt(message=message, completer=WordCompleter(["auto-capture", "./requirements.txt" ]), style=style, validator=dependency_validator)
        if len(deps):
            pj.dependencies = deps


        # 
        # Max tokens
        #
        
        def is_max_token_valid(text):
            return text == "" or (text.isdigit() and int(text) >=1 and int(text) < 10000)
        
        max_token_validator = Validator.from_callable(is_max_token_valid, error_message='Please enter a number between 1 and 10000.')
        

        message = [ 
                (ROBBIE_BLUE, "Maximum tokens to consume ["),
                (ROBBIE_DEFAULT, "none"),
                (ROBBIE_BLUE, "]:" ),
            ]
        text = prompt(message=message, style=style, validator=max_token_validator)
        if len(text):
            pj.max_tokens = int(text)
        

        # 
        # Max duration
        #
        def is_max_duration_valid(text):
            return text == "" or (text.isdigit() and int(text) >=1 and int(text) < 1000)
        duration_validator = Validator.from_callable(is_max_duration_valid, error_message='Please enter a valid duration between 1 and 1000.')


        message = [ 
                (ROBBIE_BLUE, "Max duration in minutes ["),
                (ROBBIE_DEFAULT, "none"),
                (ROBBIE_BLUE, "]:" ),
            ]
        text = prompt(message=message,style=style, validator=duration_validator)
        if len(text):
            pj.max_time = int(text)

        message = [ 
                (ROBBIE_BLUE, "Specify the directory contents to send to the remote machine ["),
                (ROBBIE_DEFAULT, os.getcwd()),
                (ROBBIE_BLUE, "]:" ),
            ]
        text = prompt(message=message, style=style)
        if len(text):
            pj.workspace_dir = text
        else:
            pj.workspace_dir = os.getcwd()

        # 
        # Environment variables
        #
        if not preserve:
            first_pass = True
            while True:
                var_name = prompt('Environment variable name (Enter a <blank> line to go to the next step):',style=Style.from_dict({'prompt': ROBBIE_BLUE}))
                if not var_name:
                    break
                var_value = prompt(f'Value for {var_name} (hint= Enter a <blank> line to use local machine value):', style=style)
                if first_pass:
                    pj.env = {}
                    first_pass = False
                pj.env[var_name] = var_value
        # 
        # Commands - loop through and capture the commands
        #
        if not preserve:
            first_pass = True
            while True:
                cmd = prompt('Enter command to run (Enter a <blank> line when you are done entering commands):', style=Style.from_dict({'prompt': ROBBIE_BLUE}))
                if not cmd:
                    break
                if first_pass:
                    pj.commands = []
                    first_pass = False
                pj.commands.append(cmd)

        pj.job_type = JobRunType.BASH_COMMAND_RUNNER

        return PositronJobConfig(version="1.0", python_job=pj)
    
    except Exception as e:
       print(f"Error: {e}")
       return None


# Class and singleton builds a list of tuples from the DB results
class FundingSources: 
    is_init: bool = False
    my_fs: dict

    def __init__(self, fs_arg: dict):
        if self.is_init:
            raise ValueError('FundingSources.load() already initialized')
        else:
            self.init = True
            self.my_fs= fs_arg

    @staticmethod
    def load():
        fs = list_funding_sources()
        if len(fs) == 0:
            return None
        # Loop through and add a custom "menu" item to each dict 
        for key, val in fs.items(): 
                val[FS_MENU] = f'{val[FS_NAME]} ({val[FS_TOKENS]} tokens available)'
        return FundingSources(fs)
        
    # Prompt toolkit needs a list of strings to display in the menu 
    def menu_items(self) -> list: 
        ret_list: list = []
        for key, val in self.my_fs.items():
            # just show names
            ret_list.append(val[FS_MENU])
        return ret_list

    # Return 'funding_group_id' using the val returned from session.prompt() 
    def id_from_menu_item(self, menu_item: str) -> str:
        for key, val in self.my_fs.items():
            if (val[FS_MENU] == menu_item):
                return val.get(FS_ID)
        return None

    def default_env_id_from_menu_item(self, menu_item: str) -> str:
        for key, val in self.my_fs.items():
            if (val[FS_MENU] == menu_item):
                return val.get(FS_DEF_ENV_ID)
        return None
    
    def default_env_name_from_menu_item(self, menu_item: str) -> str:
        for key, val in self.my_fs.items():
            if (val[FS_MENU] == menu_item):
                return val.get(FS_DEF_ENV_NAME)
        return None
    
    def default_env_name_from_fs_id(self, id: str) -> str:
        for key, val in self.my_fs.items():
                if (val[FS_ID] == id):
                    return val.get(FS_DEF_ENV_NAME)
        return None
    
    def default_env_id_from_fs_id(self, id: str) -> str:
        for key, val in self.my_fs.items():
                if (val[FS_ID] == id):
                    return val.get(FS_DEF_ENV_ID)
        return None
    
    def default_env_id(self) -> str:
        for key, val in self.my_fs.items():
            if (val[FS_TYPE] == FS_PERSONAL_TYPE):
                return val.get(FS_DEF_ENV_ID)
        return None
    
    def default_funding_source_id(self) -> str: 
        for key, val in self.my_fs.items():
            if (val[FS_TYPE] == FS_PERSONAL_TYPE):
                return val.get(FS_ID)
        return None
    
    def default_image_name(self, id: str) -> str:
        for key, val in self.my_fs.items():
            if (val[FS_ID] == id):
                return val.get(FS_DEFAULT_IMAGE_NAME)
        return None
    
    def default_image_id(self, id: str) -> str:
        for key, val in self.my_fs.items():
            if (val[FS_ID] == id):
                return val.get(FS_DEFAULT_IMAGE_ID)
        return None
    


# singleton for Environments
class Environments: 
    is_init: bool = False
    my_envs: dict

    def __init__(self, env_arg):
         if self.is_init:
            raise ValueError('Environments.load() already initialized')
         else:
            self.my_envs = env_arg
            self.is_init = True

    @staticmethod
    def load(fs_id: str):
        envs = list_environments(fs_id)
        if len(envs) == 0:
            return None
        for key, val in envs.items():
            val[ENV_MENU_ITEM] = f"{val['environmentName']} ({val['tokensPerHour']} Tokens/Hour)" # shows in menu
        return Environments(envs)

    def menu_items(self) -> list: 
        menu_list = []
        for key, val in self.my_envs.items():
            menu_list.append(val[ENV_MENU_ITEM])
        return menu_list

    def id_from_menu_item(self, menu_item: str) -> str:
        for key, val in self.my_envs.items():
            if (val[ENV_MENU_ITEM] == menu_item):
                return val.get(ENV_ID)
        return None

    def tokens_per_hour(self, env_id: str) -> str:
        for key, val in self.my_envs.items():
            if (val[ENV_ID] == env_id):
                return val.get(ENV_TPH)
        return None
    
    def cluster_type_from_env_id(self, env_id: str) -> str:
        for key, val in self.my_envs.items():
            if (val[ENV_ID] == env_id):
                return val.get(ENV_CLUSTER_TYPE)
        return None
        


# singleton for Environments
class Images: 
    is_init: bool = False
    my_images: dict

    def __init__(self, image_arg):
         if self.is_init:
            raise ValueError('Images.load() already initialized')
         else:
            self.my_images = image_arg
            self.is_init = True

    @staticmethod
    def load(fs_id: str, env_id: str):
        images = list_images(fs_id, env_id)
        if len(images) == 0:
            return None
        for key, val in images.items():
            val[IMAGE_MENU_ITEM] = f"{val[IMAGE_NAME]}" # shows in menu
        return Images(images)

    def menu_items(self) -> list: 
        menu_list = []
        for key, val in self.my_images.items():
            if val.get(IMAGE_DELETED) == False:
                menu_list.append(val[IMAGE_MENU_ITEM])
        return menu_list

    def name_from_menu_item(self, menu_item: str) -> str:
        for key, val in self.my_images.items():
            if (val[IMAGE_MENU_ITEM] == menu_item):
                return val.get(IMAGE_NAME)
        return None
        
