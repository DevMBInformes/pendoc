#!/bin/python


#########################################################################################
#
#                       IMPORTS
#########################################################################################
import os
import pyperclip
import shutil
import click
import json
import time
import re
import datetime
#import base64
from pwn import log

#########################################################################################
#
#                       FUNCTIONS CHECKS DICTS
#########################################################################################

def cmp_path_check(string:str)->bool:
    # Verificar si la cadena tiene un largo mayor a 10 caracteres
    if len(string) > 20:
        p.status("Max 20 characters")
        return False

    # Verificar si la cadena contiene caracteres no permitidos
    if not re.match(r'^[\w\-]+$', string):
        p.status("Characters no accepts in your string")
        return False

    # Verificar si la cadena tiene dos palabras
    if len(string.split()) != 1:
        p.status("Only one word")
        return False

    return True



#########################################################################################
#
#                       WORK WITH DICTS
#########################################################################################
def list_simple_dict(dictonary:dict, value_filter='', output=True)->tuple:
    counter = 0
    paths = []
    for key, value in dictonary.items():
        tmp_string = ""
        counter +=1
        for inner_key, inner_value in value.items():
            if value_filter != '':
                if inner_key == value_filter:
                    paths.append(inner_value)
            tmp_string += f" - {inner_value}"
        string = f"[{key}]{tmp_string}"
        if output == True:
            print(string)
    return counter, paths
       

#########################################################################################
#
#                       GLOBAL VARIABLES
#########################################################################################

user_name='{YOUR_USER_NAME}'
file_data="data.conf"
file_session="session.dat"
notes_file = "notes.txt"

config_path = os.path.join("/home",user_name, ".config","pendoc")
config_file = os.path.join(config_path, file_data)
session_file = os.path.join(config_path, file_session)
path_captures=os.path.join("/home", user_name, "images", "captures")
path_image = 'images'
dirs_create = ['nmap', path_image, 'scripts', 'others']
p = log.progress('Pendoc 0.2v')
pentes_path=os.path.join("/home", user_name, "pentesting")
format_time = "%Y-%d-%m-%H-%M-%S"



#########################################################################################
#
#                       STRUCT OF CONFIG
#########################################################################################
config = {}

path = {
        'name' : ["Input name of new path", "input", ''],
        'path' : ["Input the new path", "input", ''],
        }
session = {
        'name' : ["Input nade of session", 'input', cmp_path_check]
        }
#########################################################################################
#
#                       STRUCT OF NOTES
#########################################################################################

'''
dict of notes, content description
of attack
'''
notes = {
    'targets': {},
    'actions_prompt': {},
    'actions_application' : {},
    'users' : {},
    'vuln' : {},
    'comments': {},
    'scripts' : {},
}

'''
dict of ports
'''
ports = {
    'date' : ["", "time"],
    'port': ["Input the port number", "input", ''],
    'type_port': ["Input TCP or UDP", "input", ''],
    'service': ["Input the service of the port", "input", ''],
    'version': ["Input the version of the service", "input", ''],
}

'''
dict of target
'''
target = {
    'date' : ["", "time"],
    'name_machine': ["Input the machine name", "input", ''],
    'os': ["Input the operating system", "input", ''],
    'ip': ["Input the actual IP", "input", ''],
    'domain': ["Input the domain", "input", ''],
    'subdomain': ["Input the subdomain", "input", ''],
    'url': ["Input the URL", "input", ''],
    'ports': {},
}

'''
dict of actions prompt
'''
actions_prompt = {
    'date' : ["", "time"],
    'cmd': ["Input the prompt", "input", ''],
    'note': ["Insert comments", "input", ''],
    'output': ["Copy to clipboard and press enter here...", "copy_clipboard"],
    'image': ["Copy the latest image from clipboard, press Y/n: ", "copy_image"],
}

'''
dict of action applications
'''
actions_application = {
    'date' : ["", "time"],
    'application': ["Input the name of the application", "input", ''],
    'action': ["Write the action", "input", ''],
    'note': ["Insert comments", "input", ''],
    'image': ["Copy the latest image from clipboard, press Y/n", "copy_image"],
}

'''
dict of user and password
'''
user = {
    'date' : ["", "time"],
    'context': ["Insert the context", "input", ''],
    'user': ["Input the user", "input", ''],
    'password': ["Input the password", "input", ''],
    'target' : ['Insert number target', "input", ''],
}

'''
dict of vulnerability
'''
vuln = {
    'date' : ["", "time"],
    'vuln': ["Input the vulnerability with the format CVE-", "input", ''],
    'service': ["Input the compromised service", "input", ''],
    'description': ["Write a brief description", "input", ''],
    'url': ["Copy the URL to clipboard and press enter here...", "copy_clipboard"],
}

comments = {
    'date' : ["", "time"],
    'comment': ["Input the comment", "input", ''],
    'image': ["Copy the latest image from clipboard, press Y/n", "copy_image", ''],
}

scripts = {
        'date' : ["", "time"],
        'comment' : ["Input comment about script", "input", ""],
        'file' : ["Name of file", "input", ""]
        }
#########################################################################################
#
#                       ACTION OF FILES
#########################################################################################
def open_config_data()->dict:
    """
    Open de config file

    Returns (dict),if any error return empty dict, or 
    returns notes with format.
    """
    config_data, status = open_file(config_file)
    if status:
        return config_data
    else:
        tmp_content = convert_dict_to_json(config)
        status = write_file(tmp_content, config_file)
        if status:
            p.success('Create config file and default values')
        else:
            p.status('Try created, but something errors')
        return config 


def get_path_notes()->str:
    """
    Get path of notes.txt

    Returns (str) path of notes.txt
    """
    return os.path.join(get_path(copy=False), notes_file)

def open_notes()->tuple:
    """
    Get content of notes.txt

    return (tuple->dict,bool). dict : struct notes, and bool return
    the status of opertation.
    """
    session = get_path_notes()
    notes = open_file(session)
    return notes

def get_paths_enviroments(output=True):
    """
    Return 
    """
    paths = open_config_data()
    result = list_simple_dict(paths, 'path', output)
    return result
    

def get_session_folder(paths:list, output=True):
    paths_sessions = []
    counter = 0
    for folder in paths:
        array_sessions = os.listdir(folder)
        for session in array_sessions:
            paths_sessions.append(os.path.join(folder, session))
            if output == True:
                log.info(f"[{counter}] - {session} ({os.path.join(folder, session)})")
            counter +=1
    return counter, paths_sessions


def get_path_sessions(output=True):
    paths = get_paths_enviroments(output=False)[1]
    result = get_session_folder(paths, output)
    return result


def set_session(session_name):
    print(session_name)
    write_file(session_name, session_file)

def create_enviroment(path):
    enviroment = make_input(session)
    path = os.path.join(path, enviroment['name'])
    set_session(path)
    if (os.path.isdir(path)):
        p.status("The session exists, open session")
    else:
        create_working_dirs(path)
        json_notes = convert_dict_to_json(notes)
        write_file(json_notes, os.path.join(path, notes_file))
        log.info('Create file notes')
        p.success("Directory created.. you can work...")

    
def get_path(copy=True)->str:
    path = open_file_plane(session_file)
    if path:
        if copy:
            log.info(f" the session active path is: {path[0]}")
            pyperclip.copy(path[0])
    else:
        path.append('')
        p.status("No active session")
    return path[0]
    
    
def open_file_plane(file:str)->list:
    f = open(file, "r")
    result = f.readlines()
    f.close()
    return result

def open_file(file: str)->tuple:
    """
    Opens a file and parses its content as a dictionary.
    
    Args:
        file (str): The path to the file to open.
        
    Returns:
        tuple: (dict , status)
        
    Raises:
        IOError: If there's an error opening or reading the file.
        ValueError: If the file content is not valid JSON.
    """
    try:
        with open(file, 'r') as f:
            content = f.read()
            data = json.loads(content)
            return (data, True)
    except IOError as e:
        p.status(f"If there's an error opening or reading the file Nº: {e.errno}")
        time.sleep(1)
        return ({}, False)
    except ValueError as e:
        p.status(f"If the file content is not valid JSON Nº: {e}")
        time.sleep(1)
        return ({}, False)

def convert_dict_to_json(content: dict):
    """
    Converts a dictionary to JSON format.
    
    Args:
        content (dict): The dictionary to convert to JSON.
        
    Returns:
        str: The JSON representation of the dictionary.
        
    Raises:
        ValueError: If there's an error converting the dictionary to JSON.
    """
    try:
        json_data = json.dumps(content)
        return json_data
    except ValueError as e:
        log.error(f"Error converting dictionary to JSON: {e}")
        raise

def write_file(content: str, file: str) -> bool:
    """
    Writes content to a file.
    
    Args:
        content (str): The content to write.
        file (str): The path to the file to write.
        
    Returns:
        bool: True if the file was successfully written, False otherwise.
        
    Raises:
        IOError: If there's an error opening or writing to the file.
    """
    try:
        with open(file, 'w') as f:
            f.write(content)
        return True
    except IOError as e:
        log.error(f"Error writing to file: {e}")
        return False

def read_file(file: str) -> str:
    """
    Reads the content of a file.
    
    Args:
        file (str): The path to the file to read.
        
    Returns:
        str: The content of the file.
        
    Raises:
        IOError: If there's an error opening or reading the file.
    """
    try:
        with open(file, 'r') as f:
            content = f.read()
            return content
    except IOError as e:
        log.error(f"Error opening file: {e}")
        raise

def add_dict_auto_index(main_dict:dict, sub_dict:dict):
    index = len(main_dict)
    main_dict[index] = sub_dict

def check_value_exists(check_dict, key, value):
    for i, tmp_value in check_dict.items():
        for key_subdict, value_subdict in tmp_value.items(): 
            if key_subdict == key:
                p.status(f'Exists the key, please select another, key row {i}')
                log.info(f'Input other key {key_subdict} exists') 
                return False
            if value_subdict == value:
                p.status(f'The value exists, please select another, value row {i}')
                log.info(f'Input other value {value_subdict} exists') 
                return False
    return True
#########################################################################################
#
#                       FUNCTIONS OS
#########################################################################################

def list_directory(dir_path:str)->list:
    return os.listdir(dir_path)

def ultimate_image()->str:
    """

    """
    files = list_directory(path_captures)
    date_file_more_recent = 0
    file_more_recent = ''
    for file in files:
        date_created_file = os.path.getctime(os.path.join(path_captures, file)) 
        if date_created_file > date_file_more_recent:
            date_file_more_recent = date_created_file
            file_more_recent = file
    return file_more_recent


def copy_image()->str:
    """
    Search the last image saved in directorio path_image
    then rename and copy into folder image in diretory actual

    Returns (str) path the new image move.
    """
    file = ultimate_image()
    new_path_image = os.path.join(get_path(copy=False), path_image)
    name_file_image = str(len(os.listdir(new_path_image)) +  1) + ".png"
    new_path_image = os.path.join(new_path_image, name_file_image)
    shutil.move(os.path.join(path_captures, file), new_path_image)
    return new_path_image


def dir_exist(path:str, create=True)->bool:
    """
    Check if a directory exists at the given path.
    Args:
        path (str): The path of the directory to check.
        create (bool): If True, create the directory if it doesn't exist. 
                       Default is True.
    
    Returns:
        bool: True if the directory exists or was successfully created,
              False otherwise.
    """
    if os.path.isdir(path):  # Check if directory exists
        return True
    elif create:
        try:
            os.makedirs(path)# Create directory recursively
            p.status(f'The directory not exists, created... {path}')
            return True
        except OSError:
            # Failed to create directory
            log.error(f'Error to create directory: {path}')
            return False
    else:
        return False

def create_working_dirs(path:str):
    for new_dir in dirs_create:
        dir_exist(os.path.join(path, new_dir))
        log.info(f'Create new directory {os.path.join(path, new_dir)}')
        write_file('',os.path.join(path,notes_file))


    
#########################################################################################
#
#                       FUNCTIONS GETS AND SEARCH
#########################################################################################
SPACE_KEY=2

fields = {
        'users' : ['user', 'password', 'context', 'target'],
        'targets' : ['name_machine', 'os', 'ip'],
        'actions_prompt' : ['cmd', 'note'],
        'actions_application' : ['application', 'action', 'note'],
        'comments' : ['comment'],
        'vuln' : ['vuln', 'service', 'description'],
        'scripts' : ['comment', 'file'],
        'individual' : ['key' ,'value'],
        'ports' : ['port', 'type_port','service','version'],
        'space' : {
            'comments' : {
                'comment' : 80,
                'image' : 20,
                },
            'users' : {
                'user' :20,
                'password' : 20,
                'context' : 20,
                'target' : 20,
                },
            'actions_prompt' : {
                'cmd' : 40,
                'note': 100,
                'output' : 20,
                'image' : 20,
                },
            'actions_application' : {
                'application' : 18,
                'note' : 40,
                'action': 30 ,
            },
            'targets' : {
                'name_machine' : 15,
                'os' :15,
                'ip' :20,
                },
            'vuln': {
                'vuln' : 15,
                'service' : 20,
                'description': 40,
                },
            'scripts' : {
               'comment' : 90,
               'file' : 12,
                },
            'individual' : {
                'key' : 15,
                'value' : 180,
                },
            'ports' : {
                'port' : 6,
                'type_port' : 25,
                'service' : 15,
                'version' : 25,
                },
            },
        }



def print_section(section:str)->int:
    print("\n")
    p.status(f"Print fields {section}")
    content_notes = open_notes()[0]
    count_values = format_section(content_notes[section], section)
    print("\n")
    return count_values


def print_line(character:str, space:int)->str:
    #line  = "·"*((space * size) + SPACE_KEY + 2 + size)
    total_space = (space + SPACE_KEY + 6)
    line = character * total_space
    return line


def print_chart(name_section, content:list):
    titles = "|[ID]"
    total_space = 0
    for title in fields[name_section]:
        space = fields['space'][name_section][title]
        total_space += space
        titles += f"{title:^{space}}|"
    divisor_line = print_line("_", total_space)
    divisor_inner_line = print_line("-", total_space)
    print(divisor_line)
    print(titles)
    print(divisor_line)
    for item in content:
        print(item)
        print(divisor_inner_line)


def format_section(section:dict, name_section):
    list_items = []
    for key, value in section.items():
        final_line = f"|[{key:>{SPACE_KEY}}]"
        for field in fields[name_section]:
            space = fields['space'][name_section][field]
            text = value[field][:space]
            final_line += f"{text:<{space}}|"
        list_items.append(final_line)
    print_chart(name_section, list_items)
    return len(list_items)


def print_individual_record(section:str, number_record:str, row=""):
    notes, status = open_notes()
    list_items = []
    ports = False
    if status and (number_record in notes[section]):
        regis = notes[section][number_record]
        if section == 'targets':
            ports = regis['ports']
            regis.pop('ports')
        if row == "":
            space_key = fields['space']['individual']['key']
            space_value = fields['space']['individual']['value']
            for key, value in regis.items():
                value = value.replace("\n", "")
                value = value.replace("\t", "")
                final_line = (f"|[{number_record:^{SPACE_KEY}}]|{key:{space_key}}|{value:<{space_value}}|")
                list_items.append(final_line)
    else:
        print("No hay registros")
    print_chart('individual', list_items)

    if ports:
        format_section(ports, 'ports')
    

#########################################################################################
#
#                       FUNCTIONS ACTIONS
#########################################################################################

def select_list(number_paths:tuple, func2, string: str):
    """
    Generic function for listing directories and selecting actions based on them.
    
    Args:
        number_paths (tuple): This tuple should contain number_types and paths
        func2 (function): A function that performs the action with the selected item.
        string (str):     The text string to be displayed in the selection prompt, 
                          e.g., "Select a: string".
                          
    Returns:
        None
    
    Example:
        select_list(list_paths, create_environment, "number type session")
    """
    #number_types, paths = func1()  # Retrieve the total number of items and descriptions of the items.
    number_types, paths = number_paths
    number_types -=1
    while True:
        selection = input(f"Select a {string}: ").strip()
        if selection.isdigit():  # Check if it's a digit
            selection = int(selection)  # Convert to int
            if selection < 0 or selection > number_types:  # If the selection is less than zero or greater than number_types
                log.info("Incorrect selection, please input a correct selection")
            else:
                if func2 == '':
                    break
                func2(paths[selection])  # Execute func2 with the selected number.
                break
        else:
            log.info("Only numbers are valid")
            p.status("Error, please enter number")
    return selection

def make_input(struc_dict: dict) -> dict:
    """
    Creates a dictionary with user inputs based on the given structure dictionary.

    Args:
        struc_dict (dict): The structure dictionary specifying the input prompts.

    Returns:
        dict: A dictionary with user inputs based on the structure dictionary.

    Example:
        struc_dict = {
            'name': ["Enter your name", "input", ''],
            'age': ["Enter your age", "input", cmp_check_age_is_valid],
        }
        result_dict = make_input(struc_dict)
    """
    tmp_struct_dict = struc_dict.copy()
    for name, description in struc_dict.items():
        entry = False
        while not entry:
            if name == 'ports':
                break
            if description[1] == 'input':
                tmp_struct_dict[name] = str(input(f"[*] {description[0]}: "))[:-1]  #clear \n
                if description[2] != '':
                    entry = description[2](tmp_struct_dict[name])
                else:
                    entry = True
            elif description[1] == 'time':
                tmp_struct_dict[name] = datetime.datetime.now().strftime(format_time)
                break
            elif description[1] == 'copy_clipboard':
                input('Press enter and copy to clipboad to row...')
                #tmp_str = str(pyperclip.paste()[:-1]).encode('utf-8')
                #tmp_struct_dict[name] = str(base64.b64encode(tmp_str))
                tmp_str = pyperclip.paste()[:-1]
                tmp_struct_dict[name] = tmp_str
                break
            elif description[1] == 'copy_image':
                confirm = input("Copy ultimate image capture, press Y/n: ")[0]
                if confirm.lower() == "y":
                    tmp_struct_dict[name] = copy_image()
                else:
                    tmp_struct_dict[name] = ''
                break
            elif description[1] == 'type':
                tmp_struct_dict[name] = description[0]
                break
            else:
                p.status('Wrong selection')
                log.info('No reconoise option')
                break
    return tmp_struct_dict



def list_section(section:str,value:str, show_field, output=True):
    notes, status = open_notes()
    data = []
    counter=0
    if status:
        inner_section = notes[section]
        for k, v in inner_section.items():
            data.append(section + "|-|" + str(counter) + "|-|"+v[value] + "|-|" + value)
            if output:
                print(f"{k} --- {v[show_field]}")
            counter +=1
    return len(notes[section]), data
        



def new_target_init()->dict:
    tmp_target = target.copy()
    for key, _ in tmp_target.items():
        if key != 'ports':
            tmp_target[key] = ''
            if key == 'date':
                tmp_target[key] = datetime.datetime.now().strftime(format_time)
    return tmp_target


def rename_item(items):
    section, counter, actual_value, item = items.split("|-|")
    new_value = input(f"Input the new value for {item}, the actual value is: ({actual_value}): ")

    new_value = new_value[:-1] 
    notes, status = open_notes()
    if status:
        notes[section][counter][item] = new_value
        new_dict = convert_dict_to_json(notes)
        write_file(new_dict, get_path_notes())
        p.status(f"change value {actual_value} for {new_value}")
    else:
        p.status('No cannot open notes file')


def new_entry(base_dict:dict, section:str, create_make_input=True):
    if create_make_input:
        result = make_input(base_dict)
    else:
        result = new_target_init()
    notes, status = open_notes()
    if status:
        p.status('Open Notes')
        insert_note(section, notes, result)
        p.success(f'Create a new entry in section {section}')
    else:
        p.status('No cannot open notes file')


def change_item(section:str, value_to_change:str, show:str, show_input:str ):
    sections = list_section(section, value_to_change, show_field=show)
    if sections[0] > 1:
        select_list(sections, rename_item, show_input)
    else:
        rename_item(sections[1][0])


def insert_note(section:str, content, new_content):
    index = len(content[section])
    content[section][index] = new_content
    json_content = convert_dict_to_json(content)
    write_file(json_content, get_path_notes())


def select_list2(section, string=''):
    count_values = print_section(section) - 1
    if count_values < 0:
        print(f"No found values to {string} ")
    else:
        while True:
            selection = input(f"Select a {string}: ").strip()
            if selection.isdigit():  # Check if it's a digit
                selection = int(selection)  # Convert to int
                if selection < 0 or selection > count_values:  # If the selection is less than zero or greater han number_types
                    log.info("Incorrect selection, please input a correct selection")
                else:
                    break
            else:
                log.info("Only numbers are valid")
                p.status("Error, please enter number")
        return selection
    return count_values

def get_individual(section, index, string, reg="", copy=False):
    if index is not None:
        if reg != "":
            print_particular_reg(section, str(index), reg, copy)
        else:
            print_individual_record(section, str(index))
    else:
        selection = select_list2(section, string=string)
        if selection >= 0:
            if reg != "":
                print_particular_reg(section, str(selection), reg, copy)

            else:
                print_individual_record(section, str(selection))


def print_particular_reg(section, index:str, reg, copy=False):
    notes = open_notes()[0]
    print(notes[section][index][reg])
    if copy:
        p.status("Content in papperclip")
        pyperclip.copy(notes[section][index][reg])
#########################################################################################
#
#                       FUNCTIONS ENTRY
#########################################################################################

@click.command(name='new-path', help='Create a new path for sessions')
def createpath():
    """
    Method that create new paths
    """
    config_data = open_config_data() #open the config file or create
    result_config_path = {} # tmp dict
    result = False # flag controller
    while not result: # is result = False
        result_config_path = make_input(path) # input
        result = check_value_exists(config_data, result_config_path['name'], result_config_path['path']) # check if exists values

    result_config_path['path'] =  os.path.join(pentes_path, result_config_path['path']) # directory path
    result = dir_exist(result_config_path['path']) # Exists?
    if result:
        add_dict_auto_index(config_data, result_config_path)
        json_config_data = convert_dict_to_json(config_data)
        write_file(json_config_data, config_file)


@click.command(name='list-paths', help='List exists paths')
def listpaths():
    get_paths_enviroments()
 


@click.command(name='new-session', help="Create a new session")
def create_session():
    paths = get_paths_enviroments()
    select_list(paths, create_enviroment, "number type session" )
    get_path()
    new_entry(target,'targets',create_make_input=False)
    


@click.command(name='list-session', help="Print a list of session exists")
def list_sessions():
    get_path_sessions()
    
    

@click.command(name='path', help="Get path session and copy to clipboard")
def get_path_session():
    get_path()


@click.command(name='open-session', help="Open a session exists")
def open_session():
    session_folders = get_path_sessions(output=True)
    select_list(session_folders, set_session, "session open" )



@click.command(name='clear', help="Delete de active session")
def clear_session():
    set_session('')
    p.success('Delete active session')




@click.command(name="new-target", help="create a new target")
def new_target():
    new_entry(target, 'targets')


@click.command(name='new-script', help="create a new link script")
def new_script():
    new_entry(scripts, 'scripts')

@click.command(name='new-actp', help="create a new action prompt")
def new_action_prompt():
    new_entry(actions_prompt, 'actions_prompt')
 

@click.command(name='new-acta', help="create a new action application")
def new_action_application():
    new_entry(actions_application, 'actions_application')


@click.command(name="new-user", help="Entry a new user" )
def new_user():
    new_entry(user, 'users')


@click.command(name='new-vuln', help="Entry a new vulneratibily")
def new_vuln():
    new_entry(vuln, 'vuln')


@click.command(name='new-comment', help="Entry a new vulneratibily")
def new_comment():
    new_entry(comments, 'comments')

####
#CHANGE-TARGET-XX AND PORT
####
@click.command(name="change-target-name",help="Chance the value NAME MACHINE in the target select")
def change_target_name():
    change_item('targets', 'name_machine', 'name_machine', 'Select target to change the name')

@click.command(name="change-target-os", help="Chance the value O.S in the target select")
def change_target_os():
    change_item('targets', 'os', 'name_machine', 'Select target to change the value of os')


@click.command(name="change-target-ip",help="Chance the value IP in the target select")
def change_target_ip():
    change_item('targets', 'ip', 'name_machine', 'Select target to change the value of IP')

@click.command(name="change-target-domain",help="Chance the value DOMAIN in the target select")
def change_target_domain():
    change_item('targets', 'domain', 'name_machine', 'Select target to change the value of DOMAIN')


@click.command(name="change-target-subdomain", help="Chance the value SUBDOMAIN in the target select")
def change_target_subdomain():
    change_item('targets', 'subdomain', 'name_machine', 'Select target to change the value of SUBDOMAIN')


@click.command(name="change-target-url" ,help="Chance the value URL in the target select")
def change_target_url():
    change_item('targets', 'url', 'name_machine', 'Select target to change the value of URL')


####
#CHANGE-ACTIONS PROMPT
####
@click.command(name="change-actp-cmd" ,help="Chance the value URL in the target select")
def change_action_prompt_cmd():
    change_item('actions_prompt', 'cmd', 'cmd', 'Select target')


@click.command(name="change-actp-note" ,help="Chance the value URL in the target select")
def change_action_prompt_note():
    change_item('actions_prompt', 'note', 'cmd', 'Select target')

@click.command(name="change-actp-output" ,help="Chance the value URL in the target select")
def change_action_prompt_output():
    change_item('actions_prompt', 'output', 'cmd', 'Select target')

@click.command(name="change-actp-image" ,help="Chance the value URL in the target select")
def change_action_prompt_image():
    change_item('actions_prompt', 'image', 'cmd', 'Select target')



####
#CHANGE-ACTIONS APPLICATION
####

@click.command(name="change-acta-name" ,help="Chance the value URL in the target select")
def change_action_application_application():
    change_item('actions_application', 'application', 'application', 'Select target')



@click.command(name="change-acta-action" ,help="Chance the value URL in the target select")
def change_action_application_action():
    change_item('actions_application', 'action', 'application', 'Select target')


@click.command(name="change-acta-note" ,help="Chance the value URL in the target select")
def change_action_application_note():
    change_item('actions_application', 'note', 'application', 'Select target')


@click.command(name="change-acta-image" ,help="Chance the value URL in the target select")
def change_action_application_image():
    change_item('actions_application', 'image', 'application', 'Select target')



####
#CHANGE-USER
####

@click.command(name="change-user-context" ,help="Chance the value URL in the target select")
def change_user_context():
    change_item('users', 'context', 'user', 'Select target')


@click.command(name="change-user" ,help="Chance the value URL in the target select")
def change_user():
    change_item('users', 'user', 'user', 'Select target')

@click.command(name="change-user-password" ,help="Chance the value URL in the target select")
def change_user_password():
    change_item('users', 'password', 'user', 'Select target')


@click.command(name="change-user-target" ,help="Chance the value URL in the target select")
def change_user_target():
    change_item('users', 'target', 'user', 'Select target')



@click.command(name="add-port", help="add new port")
def add_port():
    sections = list_section('targets', 'name_machine', show_field='name_machine')
    selection = str(select_list(sections, func2='', string="Select to machine a input port"))
    result = make_input(ports)
    notes, status = open_notes()
    if status:
        index = len(notes['targets'][selection]['ports'])
        notes['targets'][selection]['ports'][index] = result
        json_content = convert_dict_to_json(notes)
        write_file(json_content, get_path_notes())


####
#CHANGE-VULN
####

@click.command(name="change-vuln" ,help="Chance the value URL in the target select")
def change_vuln():
    change_item('vuln', 'vuln', 'vuln', 'Select target')


@click.command(name="change-vuln-service" ,help="Chance the value URL in the target select")
def change_vuln_service():
    change_item('vuln', 'service', 'vuln', 'Select target')



@click.command(name="change-vuln-description" ,help="Chance the value URL in the target select")
def change_vuln_description():
    change_item('vuln', 'description', 'vuln', 'Select target')


@click.command(name="change-vuln-url" ,help="Chance the value URL in the target select")
def change_vuln_url():
    change_item('vuln', 'url', 'vuln', 'Select target')


####
#CHANGE-VULN
####

@click.command(name="change-comment" ,help="Chance the value URL in the target select")
def change_comment():
    change_item('comments', 'comment', 'comment', 'Select target')



@click.command(name="change-comment-image" ,help="Chance the value URL in the target select")
def change_comment_image():
    change_item('comments', 'image', 'comment', 'Select target')



####
#CHANGE-SCRIPTS
####


@click.command(name="change-script" ,help="Chance the value URL in the target select")
def change_scripts():
    change_item('scripts', 'comment', 'file', 'Select target')


@click.command(name="change-script-file" ,help="Chance the value URL in the target select")
def change_scripts_file():
    change_item('scripts', 'file', 'file', 'Select target')


####
#List and gets
####
@click.command(name="list-notes", help="List notes")
def list_notes():
    for key, _ in notes.items():
        print_section(key)

@click.command(name="get-actp", help="List notes")
def get_actp():
    print_section('actions_prompt')

@click.command(name="get-users", help="List notes")
def get_users():
    print_section('users')

@click.command(name="get-targets", help="List notes")
def get_targets():
    print_section('targets')

@click.command(name="get-vulns", help="List Vulns")
def get_vulns():
    print_section('vulns')

@click.command(name="get-comments", help="List comments")
def get_comments():
    print_section('comments')

@click.command(name="get-acta", help="List actions application")
def get_acta():
    print_section('actions_application')

@click.command(name="get-scripts", help="List scripts")
def get_scripts():
    print_section('scripts')


@click.command(name="target", help="Get Individual target")
@click.option('-i', '--index', default=None, help="Specify index targe" )
@click.option('-r', '--reg', default="", help="Specify one field to print" )
@click.option('-c', '--copy', default=None, help="Copy if specify a reg")
def get_individual_targets(index, reg, copy):
    get_individual('targets', index, 'row target', reg, copy)



@click.command(name="actp", help="Get Individual Action Prompt")
@click.option('-i', '--index', default=None, help="Specify index action" )
@click.option('-r', '--reg', default="", help="Specify one field to print" )
@click.option('-c', '--copy', default=None, help="Copy if specify a reg")
def get_individual_actp(index, reg, copy):
    get_individual('actions_prompt', index, ' Action prompt', reg, copy)



@click.command(name="acta", help="Get Individual Action application")
@click.option('-i', '--index', default=None, help="Specify index action" )
@click.option('-r', '--reg', default="", help="Specify one field to print" )
@click.option('-c', '--copy', default=None, help="Copy if specify a reg")
def get_individual_acta(index, reg, copy):
    get_individual('actions_application', index, ' Action application', reg, copy)



@click.command(name="comment", help="Get Individual comment")
@click.option('-i', '--index', default=None, help="Specify index comment" )
@click.option('-r', '--reg', default="", help="Specify one field to print" )
@click.option('-c', '--copy', default=None, help="Copy if specify a reg")
def get_individual_comment(index, reg, copy):
    get_individual('comments', index, 'Comment', reg, copy)


@click.command(name="user", help="Get Individual User")
@click.option('-i', '--index', default=None, help="Specify index user" )
@click.option('-r', '--reg', default="", help="Specify one field to print" )
@click.option('-c', '--copy', default=None, help="Copy if specify a reg")
def get_individual_user(index, reg, copy):
    get_individual('users', index, 'User', reg, copy)


@click.command(name="vuln", help="Get Individual vuln")
@click.option('-i', '--index', default=None, help="Specify index vuln" )
@click.option('-r', '--reg', default="", help="Specify one field to print" )
@click.option('-c', '--copy', default=None, help="Copy if specify a reg")
def get_individual_vuln(index, reg, copy):
    get_individual('vuln', index, 'vulnerability', reg, copy)



@click.command(name="script", help="Get Individual vuln")
@click.option('-i', '--index', default=None, help="Specify index vuln" )
@click.option('-r', '--reg', default="", help="Specify one field to print" )
@click.option('-c', '--copy', default=None, help="Copy if specify a reg")
def get_individual_script(index, reg, copy):
    get_individual('scripts', index, 'code script', reg, copy)
#########################################################################################
#
#                               INTRO
#########################################################################################

# Create a command group with Click
@click.group()
def cli():
    dir_exist(pentes_path)

#paths
cli.add_command(listpaths)      #list-paths
cli.add_command(createpath)    #create-path

#session
cli.add_command(create_session) #new
cli.add_command(list_sessions)  #list
cli.add_command(open_session)   #open
cli.add_command(clear_session)  #clear
cli.add_command(get_path_session)       #path

#notes-new
cli.add_command(new_action_prompt) #new-actp
cli.add_command(new_action_application) #new-acta
cli.add_command(new_vuln) # new-vuln
cli.add_command(new_user) # new-user
cli.add_command(new_comment) # new_comment
cli.add_command(new_target)
cli.add_command(new_script)


#change - target
cli.add_command(change_target_name)
cli.add_command(change_target_os)
cli.add_command(change_target_ip)
cli.add_command(change_target_domain)
cli.add_command(change_target_subdomain)
cli.add_command(change_target_url)
cli.add_command(add_port)


#change - Actions Prompt
cli.add_command(change_action_prompt_cmd)
cli.add_command(change_action_prompt_note)
cli.add_command(change_action_prompt_output)
cli.add_command(change_action_prompt_image)

#change - Actions applications
cli.add_command(change_action_application_note)
cli.add_command(change_action_application_application)
cli.add_command(change_action_application_action)
cli.add_command(change_action_application_image)


#change user

cli.add_command(change_user)
cli.add_command(change_user_context)
cli.add_command(change_user_password)
cli.add_command(change_user_target)


#change vulns

cli.add_command(change_vuln)
cli.add_command(change_vuln_service)
cli.add_command(change_vuln_description)
cli.add_command(change_vuln_url)

#change comment

cli.add_command(change_comment)
cli.add_command(change_comment_image)


#change scripts


cli.add_command(change_scripts)
cli.add_command(change_scripts_file)


#gets y list
cli.add_command(list_notes) # no habilitado del todo
cli.add_command(get_users)
cli.add_command(get_targets)
cli.add_command(get_actp)
cli.add_command(get_acta)
cli.add_command(get_vulns)
cli.add_command(get_scripts)
cli.add_command(get_comments)

#individual records
cli.add_command(get_individual_targets)
cli.add_command(get_individual_actp)
cli.add_command(get_individual_acta)
cli.add_command(get_individual_comment)
cli.add_command(get_individual_user)
cli.add_command(get_individual_vuln)
cli.add_command(get_individual_script)




if __name__ == '__main__':
    cli()


