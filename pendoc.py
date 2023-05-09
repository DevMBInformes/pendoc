#!/bin/python

#-----------------------------------
#Pendoc .01v                        
#author: devmb
#
#info: dev.manuel.barros@gmail.com
#----------------------------------

##
#Imports
#
##
import sys
import os
import pyperclip
import logging
import shutil
from enum import Enum
from colorlog import ColoredFormatter


path_captures{YOUR PATH CAPTURES}
##
#Config format log.
#
##
LOG_LEVEL = logging.DEBUG
LOGFORMAT = "  [%(log_color)s%(levelname)-8s%(reset)s] | %(log_color)s%(message)s%(reset)s"
logging.root.setLevel(LOG_LEVEL)
formatter = ColoredFormatter(LOGFORMAT)
stream = logging.StreamHandler()
stream.setLevel(LOG_LEVEL)
stream.setFormatter(formatter)
log = logging.getLogger('pythonConfig')
log.setLevel(LOG_LEVEL)
log.addHandler(stream)


##
#Config colors
#
##
class bcolors:
    VIOLET = '\033[90m'
    RED = '\033[91m'
    GREEN = '\033[92m' 
    YELLOW = '\033[93m' 
    BLUE = '\033[94m' 
    LILA = '\033[95m' 
    CYAN = '\033[96m' 
    GRAY = '\033[97m' 
    WHITE = '\033[98m'
    BOLD = '\x1B[1m'
    ITALIC = '\x1B[3m'
    B_I = '\x1B[1;3m'
    RESET_S = '\x1B[0m'
    RESET_C = '\033[0m' 
    RESET_A = RESET_S + RESET_C



##
# Define global variables
#
##
config_path={YOU CONFIG PATH}
config_file=config_path + "data.conf"
session_file=config_path + "session.dat"
notes_file = "/notes.txt"


###
#
#GROUP OF ENUMS
#
##

class e_target(Enum):
    #target
    name_machine="#name_machine#:"
    os="#O.S#:"
    ip="#ip#:"
    open_ports_type="#open_ports_type#:"
        

class e_face(Enum):
    face="#face#:"

class e_machine(Enum):
    #machine
    name_machine_="#name_machine#:"
    osys_="#O.S#:"
    ip_actual_="#ip_actual#:"
    open_ports_type_="#open_ports_type#:"

class e_types(Enum):
    action="@)"
    permanet="$-)"

class e_action(Enum):
    #action
    cmd = "#cmd#:"
    note = "#note#:"
    output = "#output#:"
    image="#image#:"


class e_password(Enum):
    #data context
    context="#context#:"
    user="#user#:"
    password="#password#:"


class e_vuln(Enum):
    #Data vuln
    vuln="#vuln#:"
    service="#service#:"
    description="#description#:"
    url="#url_info#:"
    exploit="#exploit#:"


items_v=f"{bcolors.VIOLET}[{bcolors.RESET_A}*{bcolors.VIOLET}]{bcolors.GREEN} " 



###
#
#Functions workings whit session
#
###
def open_session_file()->str:
    content = open(session_file, mode="r")
    result = content.read()
    content.close()
    return result.strip()
    
def name_session():
    print(open_session_file().split('/')[-1])


def write_session_file(session:str):
    write_file(session_file, session)
    session = session.split('/')[-1]
    log.debug(f"Make a new session: [{session}]")

def clear_session_file():
    write_file(session_file,"")
    log.debug(f"Delete session")

def path_session()->str:
    path = open_session_file() + notes_file
    if os.path.exists(path):
        return path
    else:
        log.error("The path no exists, please first make a session")
        return "Error"


def create_session():
    select_list(list_paths, create_enviroment, "number type session")

def open_session():
    select_list(list_session_exist, write_session_file,"number session")

##
#
#Function workings whit files and path
#
##
def write_file(path:str, content:str)->bool:
    file = open(path, mode="w")
    file.write(content)
    file.close()
    return True

def append_file(path:str, text:str):
    file= open(path, "a")
    file.write(text+"\n")


def read_paths()->list:
    content = open(config_file)
    result = content.readlines()
    content.close()
    return result


def list_paths()->tuple:
    paths = read_paths()
    for i, item in enumerate(paths):
        name = item.split(':')
        paths[i] = name[0]
        print(f"index: {i} name: {name[1].strip()}")
    return len(paths), paths
    

###
#
#
#
###

def create_enviroment(path):
    session_name = input("Plase, input name of session: ")
    new_path = path +session_name
    write_session_file(new_path)
    if (os.path.isdir(new_path)):
        log.warning("The session exists, open session")
    else:
        os.mkdir(new_path)
        os.mkdir(new_path+"/nmap")
        os.mkdir(new_path+"/exploits")
        os.mkdir(new_path+"/scripts")
        os.mkdir(new_path+"/images")
        open(new_path+notes_file, "w").close()
        log.info("Directory created.. you can work...")


###
#
#Generic Funtions
#
###
def print_path():
    path = open_session_file()
    pyperclip.copy(path)
    log.info(f"The path: {path} is in clipboard")

def error_select():
    log.error("No valid option")
    print_help()

def print_help():
    for index, value  in switch_arg.items():
        print(f"{bcolors.GREEN}pendoc.py {bcolors.RED}{index:10} {bcolors.RESET_A}: {bcolors.GREEN}{value[1]}{bcolors.RESET_A}")


def select_list(func1, func2, string):
    number_types, paths=func1()
    while True:
        selection = input(f"Select a {string}: ")
        if selection.isdigit():
            selection = int(selection)
            if selection < 0 or selection > number_types:
                log.warning("Incorrect selection, please input a correct selection")
            else:
                func2(paths[selection])
                break
        else:
            log.error("Only number is valid")


def list_directory(dir_path:str)->list:
    return os.listdir(dir_path)


def ultimate_image()->str:
    files = list_directory(path_captures)
    date_file_more_recent = 0
    file_more_recent = ''

    # iteramos sobre la lista de archivos
    for file in files:
        date_created_file = os.path.getctime(os.path.join(path_captures, file))
    
        if date_created_file > date_file_more_recent:
            date_file_more_recent = date_created_file
            file_more_recent = file

    # imprimimos el nombre del archivo más reciente
    return file_more_recent



def copy_image()->str:
    file = ultimate_image()
    new_path = open_session_file() + "/images/" 
    new_path = new_path  + str(len(os.listdir(new_path)) + 1) +".png"
    shutil.move(path_captures+file, new_path)
    return new_path


def list_session_exist()->tuple:
    paths = read_paths()
    session = [item.split(':')[0]+x for item in paths for x in os.listdir(item.split(':')[0])]
    for index,item in enumerate(session):
        name = str(set_color(bcolors.RED, item.split('/')[-1]))
        index = bcolors.LILA + "[" + set_color(bcolors.RED, str(index)) + bcolors.LILA + "]" + bcolors.RESET_A
        print(f"{index} {bcolors.LILA} name: {name:25} {bcolors.LILA} path: {bcolors.RESET_A} {item}")
    return len(session), session


def set_color(color, text):
       return color + text + bcolors.RESET_A


def make_input(delimiter:str, msg:str, clipboard=False, c_image=False):
    if clipboard:
        if c_image:
            print(f"Copy image {msg}...")
            return delimiter + msg
        else:
            input(f"{delimiter}{bcolors.GREEN}Copy {msg} to clipboard and press enter here...{bcolors.RESET_A}")
            return delimiter + pyperclip.paste()
    else:
        return delimiter + input(items_v + msg + f":{bcolors.RED} ") + bcolors.RESET_A

def list_append(reg:list, mark:e_types):
    session = path_session()
    append_file(session, mark.value)
    for item in reg:
        append_file(session, item)



###
#
#SETS
#
##


def input_face():
    list_dat = []
    list_dat.append(make_input(e_face.face.value, "Input the name of face"))
    print(e_face.face.value)
    list_append(list_dat, e_types.action)


def input_action():
    list_dat = []
    list_dat.append(make_input(e_action.cmd.value,"Input command"))
    list_dat.append(make_input(e_action.note.value,"Input comments"))
    #input(f"{items_v}Copy to clipboard and press enter here... ")
    #new_output = output + pyperclip.paste()
    list_dat.append(make_input(e_action.output.value, "data", clipboard=True))
    confirm = input("Copy ultimate image of clipboard, press Y/n: ")
    if confirm == "y" or confirm == "Y":
        list_dat.append(make_input(e_action.image.value, copy_image(), clipboard=True, c_image=True))
    list_append(list_dat, e_types.action)

def set_password():
    list_dat = []
    list_dat.append(make_input(e_password.context.value, "Input the context"))
    list_dat.append(make_input(e_password.user.value, "Input the user"))
    list_dat.append(make_input(e_password.password.value, "Input the password"))
    list_append(list_dat, e_types.action)



def set_vuln():
    list_dat = []
    list_dat.append(make_input(e_vuln.vuln.value,"Input number vuln with format CVE-"))
    list_dat.append(make_input(e_vuln.service.value, "Service or context of vuln"))
    list_dat.append(make_input(e_vuln.description.value, "Describe"))
    list_dat.append(make_input(e_vuln.url.value, "URL", clipboard=True))
    list_dat.append(make_input(e_vuln.exploit.value, "Intro name of exploit"))
    list_append(list_dat, e_types.action)



def set_machine():
    pass

def set_target_name():
    pass

def set_target_os():
    pass

def set_target_ip():
    pass


def set_target_ports():
    pass



###
#
#INIT
#
###


switch_arg = {
         "new" : (create_session, "Create a new session"),
         "list" : (list_session_exist, "List session exists"),
         "open" : (open_session, "Open a session"),
         "clear" : (clear_session_file, "Clear session"),
         "session" : (name_session,"Get name of session"),
         "face" : (input_face, "Insert faces"),
         "action" : (input_action, "Insert actions"),
         "path"  : (print_path,"Get path the actual session to clipboard"),
         "pass" : (set_password, "Insert a user, password and context"),
         "vuln" : (set_vuln, "Inser a vulnerability"),
         "help" : (print_help, "Show this menu"),
         "password" : (set_password, "Set user and password"),
         }
if len(sys.argv) > 1:
    valor = switch_arg.get(sys.argv[1])
    if valor:
        valor[0]()
    else:
        error_select()
else:
    log.error("Need arguments... pendoc <arg>")
    print_help()


