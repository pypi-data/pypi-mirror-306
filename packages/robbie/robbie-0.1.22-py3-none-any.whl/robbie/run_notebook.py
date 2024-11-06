import io
import os
import subprocess
import signal
import sys
import tempfile
import time
import ipywidgets as widgets
from ipywidgets import HBox, Layout
from nbformat import read, NO_CONVERT
from IPython import get_ipython
from IPython.display import display
from rich.jupyter import print
from positron_common.cli.logging_config import logger
from positron_common.cli.console import console, ROBBIE_DEFAULT, ROBBIE_BLUE
from positron_cli.run import run
from positron_common.job_api.funding_envs_images import *
from positron_common.cli.logging_config import set_log_level

RUN_NAME_HELPER_TEXT = '(Optional customized run name)'
COMING_SOON_MENU_ITEM = 'Customize...(coming soon)'

# Each notebook platform is unique in terms of how to derive the notebook name and how to convert its cells to a python file.
# We support three notebook types:
# 1. Visual Studio Code
# 2. Generic Jupyter Notebook
# 3. Google Colab


def _convert_notebook_to_py_based_on_platform():
    ip = get_ipython()
    if '__vsc_ipynb_file__' in ip.user_ns:
        console.print("[green]✔[/green] Visual Studio Code detected!") 
        return _convert_generic_notebook_to_py(ip.user_ns['__vsc_ipynb_file__'])
    elif 'JPY_SESSION_NAME' in os.environ:
        console.print("[green]✔[/green] Generic Jupyter Notebook detected!")
        return _convert_generic_notebook_to_py(os.getenv('JPY_SESSION_NAME'))
    elif 'google.colab' in str(ip):
        console.print("[green]✔[/green] Google Colab detected!")
        path = "/content/notebook.ipynb"
        _convert_colab_notebook_to_py(path)
    else:
        console.print("[red] Unanble to determine current notebook file name")
        return None


def run_notebook(loglevel: str = None):
    """ 
    Run a notebook as a job on Robbie 
    
    This function will display a UI that allows the user to select the hardware to run the notebook on.
    
    """
    if loglevel:
        set_log_level(loglevel)
    #
    # Left Column
    #
    left_column_title = widgets.HTML(
        value="<b>Robbie can run your notebook as a job!</b>",
    )

    # logo
    file = open(os.path.join(os.path.dirname(__file__), 'img', 'dog.png'), "rb")
    image = file.read()

    logo = widgets.Image(
        value=image,
        format='png',
        width=200,
        height=200,
    )

    style = {'description_width': 'initial'}

    #
    # Middle Column
    #
    middle_column_title = widgets.HTML(
        value="<b>Just choose your hardware!</b>",
    )
     # Environment Drop down
    _drop_dict = _load_envs_for_dropdown()
    if _drop_dict is None:
        console.print("[red] Error loading environments")
        return
    _drop_dict.update({COMING_SOON_MENU_ITEM: None})
    
    hardware_dropdown = widgets.Dropdown(
        options = _drop_dict,
        # value=_drop_dict[1],
        description='Hardware Options:',
        style=style,
        layout={'width': 'max-content'}
    )

    _or_ = widgets.HTML(
        value="           - or - ",
    )

    # robbie does it for you
    auto_checkbox = widgets.Checkbox(
        value=False,
        description='Let Robbie choose the best resources for you',
        disabled=False,
        indent=False
    )

    # goes back to simple mode
    take_me_back_button = widgets.Button(
        description='Take me back',
        disabled=False,
        # button_style='info', # 'success', 'info', 'warning', 'danger' or ''
        tooltip='Go back to simple options',
        style = style
    )

    #
    # Right Column
    #
    right_column_title = widgets.HTML(
        value="<b>And get the ball rolling!</b>",
    )

    # optional name
    optional_name = widgets.Text(
        value=RUN_NAME_HELPER_TEXT,
        # description='Enter a name:',
        disabled=False,
        style=style
    )
    
    # "Run" button
    run_button = widgets.Button(
        description='Run',
        disabled=False,
        button_style='success', # 'success', 'info', 'warning', 'danger' or ''
        tooltip='Your notebook will be run as a job on Robbie',
        icon='play',
        style = style
    )

    # make sure the notebooke is saved
    saved_text = widgets.HTML(
        value="\n\nPlease ensure your notebook is saved before hitting to <b>Run</b> button",
    )

    # save help
    file = open(os.path.join(os.path.dirname(__file__), 'img', 'mac_save.png'), "rb")
    image = file.read()

    mac_short_cut_image = widgets.Image(
        value=image,
        format='png',
        width=30,
        height=21,
    )

    mac_shortcut_text = widgets.HTML(
        value=" on a Mac",
    )
    mac_save = HBox([mac_short_cut_image, mac_shortcut_text])
    # dont' stretch the image
    mac_save.layout.align_items = 'center'

    file = open(os.path.join(os.path.dirname(__file__), 'img', 'windows_save.png'), "rb")
    image = file.read()

    windows_shortcut_image = widgets.Image(
        value=image,
        format='png',
        width=49,
        height=18,
    )
    windows_shortcut_text = widgets.HTML(
        value=" on Windows",
    )

    coming_soon_text = widgets.HTML(
        value="Coming soon!",
    )

    # robbie does it for you
    tail_checkbox = widgets.Checkbox(
        value=False,
        description='Tail the remote machine stdout.',
        disabled=False,
        indent=False,
        style=style
    )
    windows_save = HBox([windows_shortcut_image, windows_shortcut_text])
    # dont' stretch the image
    windows_save.layout.align_items = 'center'

    save_hints = widgets.HBox([mac_save, windows_save])

    # layout
    left_column = widgets.VBox([left_column_title, logo])
    middle_column = widgets.VBox([middle_column_title, hardware_dropdown, _or_, auto_checkbox],layout=Layout(margin = '0 20px 0 20px'))
    right_column = widgets.VBox([right_column_title, optional_name, run_button, saved_text, save_hints, tail_checkbox], layout=Layout(margin = '0 20px 0 20px'))
    ui = widgets.HBox([left_column, middle_column, right_column])

    out = widgets.Output()
    # display everything
    display(ui, out)

 
    def on_take_me_back_button_clicked(change):
        """ When we display the full list of option (all disabled) this button gets gets us back to the simple mode"""
        with out:
            # print("on_take_me_back_clicked() - change:", change)
            middle_column.children = [middle_column_title, hardware_dropdown, _or_, auto_checkbox]
    
    take_me_back_button.on_click(on_take_me_back_button_clicked)
    

    # this is the hardware dropdown to change to customization mode
    def on_hw_dropdown_changed(change):
        """ This is experimental now to show users what is coming"""
        with out:
            # print("on_checkbox_clicked() - change:", change)
            if change.get('type') == 'change' and change.get('name') == 'value' and change.get('new') == COMING_SOON_MENU_ITEM:
                gpu_dropdown = widgets.Dropdown(
                    options=['Nvidia A10 (24GB)', 'Nvidia A100 (40GB)', 'Nvidia H100 (40GB)', 'CPU only'],
                    value='Nvidia A100 (40GB)',
                    description='GPU model:',
                    style=style,
                    layout={'width': 'max-content'},
                    disabled=True
                )
                cpu_slider=widgets.IntSlider(description='vCPU cores', min=1, max=64, step=1, value=4, style=style, disabled=True);
                memory_slider=widgets.IntSlider(description='System Memory (GB)', min=16, max=128, step=16, value=32, style=style, disabled=True);
                disksize_slider=widgets.IntSlider(description='Disk Size (GB)', min=16, max=128, step=16, value=32, style=style, disabled=True);
                middle_column.children = [middle_column_title, coming_soon_text, gpu_dropdown, cpu_slider, memory_slider, disksize_slider, take_me_back_button]

    hardware_dropdown.observe(on_hw_dropdown_changed)

    # this is the robbie does it for you checkbox
    def on_checkbox_clicked(change):
        """ This is experimental now to show users what is coming"""
        with out:
            # print("on_checkbox_clicked() - change:", change)
            if change.get('type') == 'change' and change.get('name') == 'value' and change.get('new') == True:
                # print("Checkbox is checked")
                # gpu_dropdown.disabled = True 
                # cpu_slider.disabled = True
                # memory_slider.disabled = True
                hardware_dropdown.disabled = True
                # disksize_slider.disabled = True
            elif change.get('type') == 'change' and change.get('name') == 'value' and change.get('new') == False:
                # print("Checkbox is unchecked")
                # gpu_dropdown.disabled = False
                # cpu_slider.disabled = False
                # memory_slider.disabled = False
                hardware_dropdown.disabled = False
                # disksize_slider.disabled = False

    # register the event handler
    auto_checkbox.observe(on_checkbox_clicked)


    def on_button_clicked(b):
        """ The user clicked the run button """
        with out:
            logger.debug(f"Hardware dropdown value: {hardware_dropdown.value}")  
            if hardware_dropdown.value == None:
                console.print("[red] Please choose a hardware option, before running.")
                return
            
            py_path = _convert_notebook_to_py_based_on_platform()
            if py_path:
                console.print("[green]✔[/green] Converting notebook to Python..Success!")
            else:
                console.print("[red]Comverting notebook to Python..failed!")
                return
            
            console.print('Sending run to Robbie...')

            # this was the old way of doing things
            # kept here for reference
            '''
            run_cmd = f'robbie run "pip install uv && uv pip install -r ./requirements.txt && python {py_path}" --environment_id {hardware_dropdown.value} --y --auto-dep'
            if (optional_name.value and optional_name.value != RUN_NAME_HELPER_TEXT):
                run_cmd += f' --name "{optional_name.value}"'
            if tail_checkbox.value:
                run_cmd += ' --tail'
  
            # check if they enter a name
            rc = bash(run_cmd, print_stdout=True, print_stderr=True)
            if(rc != 0):
                console.print("[red] Job submission to Robbie..failed! Return code:", rc)
            '''
            run(name_arg=optional_name.value,
                funding_arg=None,
                environment_arg=hardware_dropdown.value,
                image_arg=None,
                commands_arg=f"pip install uv && uv pip install -r ./requirements.txt && python {py_path}",
                auto_capture_deps=True,
                tail=tail_checkbox.value,
                status=False,
                skip_prompts=True,
                interactive=False,
                download=False,
                create_only=False)
        
    # register the event handler
    run_button.on_click(on_button_clicked)

class VerboseCalledProcessError(subprocess.CalledProcessError):
    def __str__(self):
        if self.returncode and self.returncode < 0:
            try:
                msg = "Command '%s' died with %r." % (
                    self.cmd, signal.Signals(-self.returncode))
            except ValueError:
                msg = "Command '%s' died with unknown signal %d." % (
                    self.cmd, -self.returncode)
        else:
            msg = "Command '%s' returned non-zero exit status %d." % (
                self.cmd, self.returncode)

        return f'{msg}\n' \
               f'Stdout:\n' \
               f'{self.output}\n' \
               f'Stderr:\n' \
               f'{self.stderr}'


def bash(cmd, print_stdout=True, print_stderr=True):
    stdoutfile = tempfile.mktemp()
    stderrfile = tempfile.mktemp()
    with io.open(stdoutfile, 'w') as stdout, io.open(stderrfile, 'w') as stderr, io.open(stdoutfile, 'r') as all_stdout, io.open(stderrfile, 'r') as all_stderr:
        proc = subprocess.Popen(cmd, stderr=stderr, stdout=stdout, shell=True, universal_newlines=True,
                        executable='/bin/bash')

        stdout_text = ''
        stderr_text = ''
        while proc.poll() is None:
            stdout_line = all_stdout.read();
            stderr_line = all_stderr.read();
            stderr_text += stderr_line
            stdout_text += stdout_line
            sys.stdout.write(stdout_line)
            sys.stderr.write(stderr_line)
            time.sleep(0.5)
        
        stdout_line = all_stdout.read();
        stderr_line = all_stderr.read();
        stderr_text += stderr_line
        stdout_text += stdout_line
        sys.stdout.write(stdout_line)
        sys.stderr.write(stderr_line)

        if proc.wait() != 0:
            raise VerboseCalledProcessError(proc.returncode, cmd, stdout_text, stderr_text)
        return proc.returncode

def _convert_generic_notebook_to_py(nb_full_path):
    """
    Convert a generic notebook to a python file
    - works for VScode and Jupyter notebooks
    - remove things that are not compatible with generic python
    """
    if nb_full_path:
        console.print(f"Reading notebook file: {nb_full_path}")
        with open(nb_full_path) as fp:
            notebook = read(fp, NO_CONVERT)
        cells = notebook['cells']
        code_cells = [c for c in cells if c['cell_type'] == 'code']

        write_file = f"{os.path.splitext(os.path.basename(nb_full_path))[0]}.py"
        console.print(f"Writing Python file: {write_file}")
        with open(write_file, 'w') as fp1:
            for no_cell, cell in enumerate(code_cells):
                # print(f"####### Cell {no_cell} #########")
                # each cell is a string
                my_str = cell['source']

                # split the string into lines so we can look at each one
                list_of_lines = my_str.split('\n')
                clean_list = []
                for line in list_of_lines:
                    # discard magics
                    if line.startswith('%'):
                        # print("found %")
                        continue
                    if line.startswith("%%"):
                        # print("found %%")
                        continue
                    # discard robbie imports
                    if line == "import robbie":
                        continue
                    if line == "robbie.init()":
                        continue
                    # wrap shell commands in os.system
                    if line.startswith("!"):
                        # print("found !")
                        line = line.replace(line[0], "", 1)
                        line = f"import os\nos.system('{line}')"
                    clean_list.append(line)
                my_str = '\n'.join(clean_list) 
                fp1.write(my_str)
                fp1.write("\n")
            #print("")
            return write_file
    return None
    
'''
Special way to convert a Google Colab notebook to a python file
- Google Colab notebooks have a different structure
- We need to use the Google Colab API to fetch the cells
'''
def _convert_colab_notebook_to_py(nb_full_path):
    # fetch the cells from the notebook frontend
    from google.colab import _message
    nb = _message.blocking_request('get_ipynb')
    if nb:
        cells = nb["ipynb"]['cells']
        code_cells = [c for c in cells if c['cell_type'] == 'code']

        print("nb_full_path:", nb_full_path)
        write_file = f"{os.path.splitext(os.path.basename(nb_full_path))[0]}.py"
        with open(write_file, 'w') as fp1:
            # go through the cells
            for no_cell, cell in enumerate(code_cells):
                print(f"####### Cell {no_cell} #########")
                print(cell['source'])
                # each cell is a list of strings
                list_of_lines = cell['source']
                # clean up the lines
                clean_list = []
                for line in list_of_lines:
                    # discard magics
                    if line.startswith('%'):
                        print("found %")
                        continue
                    if line.startswith("%%"):
                        print("found %%")
                        continue
                    # discard robbie imports
                    if line == "import robbie":
                        continue
                    if line == "robbie.init()":
                        continue
                    # wrap shell commands in os.system
                    if line.startswith("!"):
                        print("found !")
                        line = line.replace(line[0], "", 1)
                        line = f"import os\nos.system('{line}')"
                    clean_list.append(line)
                my_str = '\n'.join(clean_list) 
                fp1.write(my_str)
                fp1.write("\n")
            return write_file
    return None


#
# Reads the environments from the PERSONAL funding group
#

def _load_envs_for_dropdown():
    """
    Load the environments for the dropdown list in the cell output
    """
    fs = list_funding_sources()
    if len(fs) == 0:
        return None
    
    personal_fs_id = None
    for key, val in fs.items():
        if (val[FS_TYPE] == FS_PERSONAL_TYPE):
            personal_fs_id = val.get(FS_ID)
    
    if personal_fs_id is None:
        return None
    envs = list_environments(personal_fs_id)
    if len(envs) == 0:
        return None
    
    dropdown_list = {}
    for _, val in envs.items():
        dropdown_list.update({val.get(ENV_NAME) + " - " + val.get(ENV_DESCRIPTION) + f' ({val.get(ENV_TPH)} tokens/hr)' : val.get(ENV_ID)})
    return dropdown_list





    

