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
from colorlog import ColoredFormatter



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
config_path="/home/devmb/.config/pendoc/"
config_file=config_path + "data.conf"
session_file=config_path + "session.dat"
notes_file = "/notes.txt"


##
#Delimiter strings
#
##

face = "#face#:"
cmd = "#cmd#:"
note = "#note#:"
output = "#output#:"
action = "@)"


data="$)"
context="#context#:"
user="#user#:"
password="#password#:"


vuln="#vuln#:"
service="#service#:"
description="#description#:"
url="#url_info#:"
exploit="#exploit#:"


items_v=f"{bcolors.VIOLET}[{bcolors.RESET_A}*{bcolors.VIOLET}]{bcolors.GREEN} " 

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
    

def create_enviroment(path):
    session_name = input("Plase, input name of session: ")
    new_path = path +session_name
    write_session_file(new_path)
    if (os.path.isdir(new_path)):
        log.warning("The session exists, open session")
    else:
        os.mkdir(new_path)
        os.mkdir(new_path+"/nmap")
        open(new_path+notes_file, "w").close()
        log.info("Directory created.. you can work...")


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


def list_session_exist()->tuple:
    paths = read_paths()
    session = [item.split(':')[0]+x for item in paths for x in os.listdir(item.split(':')[0])]
    for index,item in enumerate(session):
        name = str(set_color(bcolors.RED, item.split('/')[-1]))
        index = bcolors.LILA + "[" + set_color(bcolors.RED, str(index)) + bcolors.LILA + "]" + bcolors.RESET_A
        print(f"{index} {bcolors.LILA} name: {name:25} {bcolors.LILA} path: {bcolors.RESET_A} {item}")
    return len(session), session


def create_session():
    select_list(list_paths, create_enviroment, "number type session")

def open_session():
    select_list(list_session_exist, write_session_file,"number session")



def path_session():
    path = open_session_file() + notes_file
    if os.path.exists(path):
        return path
    else:
        log.error("The path no exists, please first make a session")
        exit(1)


def input_face():
    new_face = make_input(face, "Input the name of face")
    session = path_session()
    append_file(session, new_face)


def set_color(color, text):
       return color + text + bcolors.RESET_A


def make_input(delimiter:str, msg:str):
    return delimiter + input(items_v + msg + f":{bcolors.RED} ") + bcolors.RESET_A

def input_action():
    session = path_session()
    list_dat = []
    list_dat.append(make_input(cmd,"Input command"))
    list_dat.append(make_input(note,"Input comments"))
    input(f"{items_v}Copy to clipboard and press enter here... ")
    new_output = output + pyperclip.paste()
    list_dat.append(new_output)
    list_append(list_dat, session)


def list_append(reg:list, session):
    for item in reg:
        append_file(session, item)

def set_password():
    session = path_session()
    list_dat = []
    list_dat.append(make_input(context, "Input the context"))
    list_dat.append(make_input(user, "Input the user"))
    list_dat.append(make_input(password, "Input the password"))
    list_append(list_dat, session)


def set_vuln():
    pass

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
         "help" : (print_help, "Show this menu")
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


