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
from os import system as x
startupinfo = None
#import logging    
#logging.basicConfig(level=logging.DEBUG)

sys.path.append("./lib")
from sleekxmpp import ClientXMPP

if os.name == "nt":
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    
    road = 'C:/Program Files (x86)/VideoLAN/VLC/vlc.exe'
    print(os.path.isfile(road))
    if (os.path.isfile(road)):
        pass
    else:
        road = 'C:/Program Files/VideoLAN/VLC/vlc.exe'
        if (os.path.isfile(road)):
            pass
        else:
            print ("Application require VLC Media Player. Messages will not be readed.")
    
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
class Settings:
    lang = "en"
    names = []
    read_name = True
    whitelist = True


class Loading:
    """Loading"""
    from time import sleep
    loading_state = True
    
    def start():
        threading.Thread(target=Loading.loading).start()

    def loading(loanim = ["|", "/", "-", "\\"], speed = 0.1):
        a = 0
        print()
        while Loading.loading_state:
            print("\u001B[2A\u001B[1C")
            print (loanim[a])
            a = a + 1
            if a >= len(loanim):
                a = 0
            Loading.sleep(speed)
        Loading.loading_state = True
        
    def stop():
        Loading.loading_state = False
        while Loading.loading_state == False:
            pass
        print("\u001B[2A\u001B[1C")


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
    print ("Do you want to launch application with default settings?\n\
(You can access menu by typing menu while application is running)")
    volba = input ("Y/n: ")
    if volba in ["Y", "y", '']:
        return
    else:
        menu()


def menu():
    cls()
    
    if len(Settings.names) == 0:
        i_names = "all"
    else:
        i_names = len(Settings.names)
    
    print ("""Menu:
1 -> Set language (set: {0})
2 -> Userlist settings (count: {1})
3 -> Read name: {2}

0 -> Run

q -> exit()
""".format(Settings.lang, i_names, Settings.read_name))
    
    choice = input("Enter your choice: ")
    
    if choice == "":
        cls()
        return
    elif choice in ("q", "exit"):
        os._exit(1)
    try:
        choice = int(volba)
    except:
        cls()
        print("Error! Not a valid choice.")
        menu()
        return
    
    if choice == 0:
        return
    if choice == 1:
        Settings.lang = input("Type language code (for example. sk, en, de): ")
        cls()
    elif choice == 2:
        cls()
        set_users()
    elif choice == 3:
        Settings.read_name = not Settings.read_name
        cls()
    else:
        cls()
        print("Error! You have entered wrong number.")

    menu()


def set_users():
    cls()
    if len(Settings.names) == 0:
        i_names = "all"
    else:
        i_names = Settings.names
    if (Settings.whitelist):
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
            if name in Settings.names: 
                print("!> The user is already in list")
            else:
                Settings.names.append(name)
                break
        elif command == "del":
            if name in Settings.names: 
                del Settings.names [Settings.names.index(name)]
                break
            else:
                print ("!> This user not on the list.")
        elif command == "clear":
            Settings.names = []
            break
        elif command == "wb":
            Settings.whitelist = not Settings.whitelist
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
    if Settings.read_name:
        toread = name + " wrote: " + text
    else:
        toread = text
    print ("Reading: " + name + " wrote: " + text)
    uurrll = "\"http://translate.google.com/translate_tts?tl="+Settings.lang+"\
&q="+toread+"&ie=UTF8\""
    if os.name=="nt":
        subprocess.call(player()+uurrll, startupinfo=startupinfo)
    else:
        x(player()+uurrll+" &> /dev/null")


def message(msg):
    if msg["type"] in ("chat","normal"):
        rmsg = msg["body"]
        
        froms = str(msg["from"])
        idecko = froms[froms.find("-")+1:froms.find("@")]
        name = id_to_name(idecko)
        
        if len(Settings.names) == 0:
            read (name, rmsg)
        else:
            if (name in Settings.names) == Settings.whitelist:
                read (name, rmsg)
            else:
                print(name + " wrote: " + rmsg)


def kwit():
    inpul = input()
    if inpul == "exit":
        print ("Exitting...")
        os._exit(1)
    elif inpul == "menu":
        menu()
    kwit()


def check_username(usrn):
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