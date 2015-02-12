#!/usr/bin/python3

"""
   Copyright 2014 Tomáš Vician, Štefan Uram

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import sys
import subprocess
import getpass
import json
import urllib.request
import os
import threading
import urllib.parse
from os import system as x
startupinfo = None
#import logging    
#logging.basicConfig(level=logging.DEBUG)

sys.path.append("./lib")
from sleekxmpp import ClientXMPP

try:
    urllib.request.urlopen("http://62.168.125.40/", timeout=10)
    pass
except urllib.request.URLError:
    print ("Internet connection does not exist.")
    volba = input()
    if volba == "continue":
        pass
    else:
        os._exit(1)

if os.name == "nt":
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    
    road = 'C:/Program Files (x86)/VideoLAN/VLC/vlc.exe'
    if (os.path.isfile(road)):
        pass
    else:
        road = 'C:/Program Files/VideoLAN/VLC/vlc.exe'
        if (os.path.isfile(road)):
            pass
        else:
            print ("Application require VLC Media Player. \
Messages will not be readed.")
    
    def player():
        return "\"" + road + "\" --play-and-exit --intf dummy "

else:
    while True:
        try:
            subprocess.call("mplayer", stdout=subprocess.PIPE)
            def player():
                return "mplayer -really-quiet -noconsolecontrols -nolirc "
            break
        except OSError:
            if os.path.isfile("/usr/bin/vlc"):
                def player():
                    return "vlc --play-and-exit --intf dummy "
                break
            else:
                print ("Application require: \n\
mplayer or VLC media player.\n\
Please install it and continue by press Enter.")
                input ()


#### APP
class Config: # UNDER CONSTRUCTION
    import configparser
    file = "config.ini"
    config = configparser.ConfigParser()
    if (os.path.isfile(file)):
        config_exists = True
        print ("Config file with saved settings found.\n\
Do you want to load theese settings? If not, application will load \
default settings\n\
(You can access menu by typing menu while application is running)")
        volba = input ("Y/n: ")
        if volba in ["Y", "y", '']:
            config.read(file)
        else:
            config["SETTINGS"] = {"lang": "en", "read_name": "True",
            "whitelist": "True", "user": ""}
            config["NAMES"] = {}
            config_exists = "true" #menu()
    else:
        config_exists = False
        config["SETTINGS"] = {"lang": "en", "read_name": "True",
        "whitelist": "True", "user": ""}
        config["NAMES"] = {}
    
    class File:
        def read(file):
            with open(file, 'r') as f:
                Config.config.read(f)
        def write(file):
            with open(file, 'w') as f:
                Config.config.write(f)
    
    def rd(variable, category="SETTINGS"):
        if variable != "":
            data = Config.config[category][variable]
        else:
            data = Config.config[category]
        
        if data in ("True", "False"):
            if data == "True":
                data = True
            else: 
                data = False
        return data
    
    def wt(variable, data, category="SETTINGS"):
        if data != "":
            data = str(data)
            Config.config[category][variable] = data
        else:
            Config.config[category] = variable
        
    def save():
        Config.File.write(Config.file)

class Dynamic:
    read_running = False


class Loading:
    """Loading"""
    from time import sleep
    loading_state = True
    text = None

    try:
        import loadanim
        loadingAnimation = loadanim.genAnim()
        lines = loadanim.lines + 2
        speeded = loadanim.speed
        width = loadanim.width
    except:
        loadingAnimation = ["|", "/", "-", "\\"]
        lines = 0 + 2
        speeded = 0.1
        width = 1

    def start():
        threading.Thread(target=Loading.loading).start()

    def loading(loanim = loadingAnimation, speed = speeded):
        a = 0
        if not (Loading.text == None):
            Loading.lines = Loading.lines + 1
        if not (os.name == "nt"):
            for i in range(1, Loading.lines):
                print()
        Loading.loading_state = True
        while Loading.loading_state:
            if os.name == "nt":
                cls()
            else:
                print("\u001B[" + str(Loading.lines) + "A\u001B[1C")
            if not (Loading.text == None):
                print (Loading.text)
            print(loanim[a])
            a = a + 1
            if a >= len(loanim):
                a = 0
            Loading.sleep(speed)
        Loading.loading_state = True
        
    def stop():
        if Loading.loading_state:
            Loading.loading_state = False
            while Loading.loading_state == False:
                pass
            if os.name == "nt":
                cls()
            else:
                print("\u001B[" + str(Loading.lines) + "A\u001B[1C")
                for i in range(1, Loading.lines):
                    print(" " * Loading.width)
                print("\u001B[" + str(Loading.lines) + "A\u001B[1C")
            Loading.loading_state = False


if os.name == "nt":
    Loading.text = "Loading..."


def cls():
    if os.name == "nt":
        x("cls")
    else:
        x("clear")


def session_start(event):
    fbtts.send_presence()
    Loading.stop()
    print("Connected..")
    fbtts.get_roster()


def startup_q():
    if Config.config_exists == False:
        print ("Do you want to launch application with default settings?\n\
(You can access menu by typing menu while application is running)")
        volba = input ("Y/n: ")
        if volba in ["Y", "y", '']:
            return
        else:
            menu()
    elif Config.config_exists == "true": 
        menu()


def menu():
    cls()
    
    if len(list(Config.rd("", "NAMES").keys())) == 0:
        i_names = "all"
    else:
        i_names = len(list(Config.rd("", "NAMES").keys()))
    
    print ("""Menu:
1 -> Set language (set: {0})
2 -> Userlist settings (count: {1})
3 -> Read name: {2}\n\n
s -> Save settings as default
q -> exit()
""".format(Config.rd("lang"), i_names, Config.rd("read_name")))
    
    choice = input ("Enter your choice: ")
    
    if choice == "":
        cls()
        return
    elif choice in ("q", "exit"):
        os._exit(1)
    elif choice == "s":
        Config.save()

    try:
        choice = int(choice)
    except:
        cls()
        print("Error! Not a valid choice.")
        menu()
        return
    
    if choice == 0:
        return
    if choice == 1:
        Config.wt("lang", input("Type language code (example: sk, en, de): "))
        cls()
    elif choice == 2:
        cls()
        set_users()
    elif choice == 3:
        Config.wt("read_name", not Config.rd("read_name"))
        cls()
    else:
        cls()
        print("Error! You have entered wrong number.")

    menu()


def set_users():
    cls()
    if len(list(Config.rd("", "NAMES").keys())) == 0:
        i_names = "all"
    else:
        i_names = list(Config.rd("", "NAMES").keys())
    if (Config.rd("whitelist")):
        i_wlist = "[WHITELIST] /  BLACKLIST "
        i_wlstw = "read"
    else:
        i_wlist = " WHITELIST  / [BLACKLIST]"
        i_wlstw = "don’t read"
    
    print ("!> Currently {0} users:\n    {1}".format(i_wlstw, i_names))
    print ("""!> Available commands: 
    add [user] 
    del [user]
    clear          (clear list)
    wb (change access to users) """ + i_wlist)
    
    while 1:
        command = input("?> ")
        try:
            command, name = command.split(" ", 1)
        except:
            pass
        
        if command == "add":
            if name in list(Config.rd("", "NAMES").keys()): 
                print("!> The user is already in the list")
            else:
                tmp = list(Config.rd("", "NAMES").keys())
                tmp.append(name)
                dictt = {}
                Config.wt(dictt.fromkeys(tmp, ""), "", "NAMES")
                break
        elif command == "del":
            if name in list(Config.rd("", "NAMES").keys()): 
                tmp = list(Config.rd("", "NAMES").keys())
                del tmp [tmp.index(name)]
                dictt = {}
                Config.wt(dictt.fromkeys(tmp, ""), "", "NAMES")
                break
            else:
                print ("!> The user is not in the list.")
        elif command == "clear":
            tmp = list(Config.rd("", "NAMES").keys())
            tmp = {}
            Config.wt(tmp, "", "NAMES")
            break
        elif command == "wb":
            Config.wt("whitelist", not Config.rd("whitelist"))
            cls()
            break
        elif command == "exit":
            os._exit(1)
            exit()
        elif command == "":
            cls()
            return
        else:
            print ("!> Wrond command!")

    set_users()


def id_to_name(iddie):
    url = "http://graph.facebook.com/" + iddie
    raw_data = urllib.request.urlopen(url).read()
    data = json.loads(raw_data.decode("utf8"))
    name = data["name"]
    return name


def read(name, text):
    while Dynamic.read_running:
        pass
    Dynamic.read_running = True
    if Config.rd("read_name"):
        toread = name + " wrote: " + text
    else:
        toread = text

    toread = urllib.parse.quote(toread)
    while True:
        if len(toread) > 160:
            toread_now = toread[:toread[:160].rfind("%20")]
            toread = toread[toread[:160].rfind("%20"):]
        else:
            toread_now = toread
        if toread_now == "":
            toread_now = toread
        print ("Reading: " + urllib.parse.unquote(toread_now))
        uurrll = "\"http://translate.google.com/translate_tts?tl=\
"+Config.rd("lang")+"&q="+toread_now+"&ie=UTF8\""
        if os.name=="nt":
            subprocess.call(player()+uurrll, startupinfo=startupinfo)
        else:
            x(player()+uurrll+" &> /dev/null")
        if toread == toread_now:
            break

    Dynamic.read_running = False


def message(msg):
    if msg["type"] in ("chat","normal"):
        rmsg = msg["body"]
        
        froms = str(msg["from"])
        idecko = froms[froms.find("-")+1:froms.find("@")]
        name = id_to_name(idecko)
        
        if len(list(Config.rd("", "NAMES").keys())) == 0:
            read (name, rmsg)
        else:
            if (name.lower() in list(Config.rd("", "NAMES").keys())) == Config.rd("whitelist"):
                read (name, rmsg)
            else:
                print(name + " wrote: " + rmsg)


def kwit():
    inpul = input()
    if (inpul == "exit") or (inpul == "quit"):
        print ("Exiting...")
        os._exit(1)
    elif inpul == "menu":
        Loading.stop()
        menu()
    kwit()


def check_username(usrn):
    if Config.rd("user") == usrn:
        return True
    Loading.start()
    url = "http://graph.facebook.com/" + usrn
    try:
        raw_data = urllib.request.urlopen(url).read()
        data = json.loads(raw_data.decode("utf8"))
        try:
            data["error"]
            Loading.stop()
            return False
        except:
            Loading.stop()
            Config.wt("user", usrn)
            return True
    except:
        Loading.stop()
        return False


def get_info():
    jid = input("Username: ")
    while not check_username(jid):
        print ("Type correct login name.")
        jid = input("Username: ")
    jid += "@chat.facebook.com"
    password = getpass.getpass("Password: ")
    return jid, password


def main():
    startup_q()
    
    jid,password = get_info()
    server = ("chat.facebook.com", 5222)

    print ("Connecting... (it may takes some minutes)")
    Loading.start()
    threading.Thread(target=kwit).start()
    
    global fbtts
    fbtts = ClientXMPP(jid,password)
    fbtts.add_event_handler("session_start", session_start)
    fbtts.add_event_handler("message", message)
    fbtts.auto_reconnect = True
    fbtts.connect(server)
    fbtts.process(block=True)


if __name__ == "__main__":
    main()