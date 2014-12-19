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
#logging.basicConfig(level=logging.ERROR)


#### check SleekXMPP
"""
while True:
    try:
        from sleekxmpp import ClientXMPP
        break
    except ImportError:
        print ("Nemáš knižnicu SleekXMPP. Chceš ju nainštalovať?")
        volba = input ("Y/n: ")
        if volba in ["Y", "y", '']:
            if os.name == "nt":
                x("cd lib/SleekXMPP-1.3.1/ && python setup.py install")
            else:
                x("cd lib/SleekXMPP-1.3.1/ && sudo python3 setup.py install")
            print ("Môžeš skúsiť znova spustiť aplikáciu")
            exit ()
        else:
            print ("Nieje možné importovať knižnicu SleekXMPP.")
            exit ()"""
sys.path.append("./lib")
from sleekxmpp import ClientXMPP

#### check mplayer
if os.name == "nt":
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    
    cesta = 'C:/Program Files (x86)/VideoLAN/VLC/vlc.exe'
    print(os.path.isfile(cesta))
    if (os.path.isfile(cesta)):
        #print ("(64bit)")
        pass
    else:
        cesta = 'C:/Program Files/VideoLAN/VLC/vlc.exe'
        if (os.path.isfile(cesta)):
            #print ("(x86)")
            pass
        else:
            print ("Aplikácia pre prehrávanie zvuku potrebuje VLC Media Player. V základných umiestneniah sa nenachádza. Správy nebudú prečítané nahlas.")
    def player():
        return "\""+cesta + "\" --play-and-exit --intf dummy "
    
    #exit()
else:
    while True:
        try:
            subprocess.call("mplayer", stdout=subprocess.PIPE)
            def player():
                return "mplayer -ao alsa -really-quiet -noconsolecontrols -nolirc "
            break
        except OSError:
            if os.path.isfile("/usr/bin/vlc"):
                def player():
                    return "vlc --play-and-exit --intf dummy "
                break
            else:
                print ("Pre používanie je potrebné mať nainštalovaný mplayer alebo VLC media player.\nProsím, doinštalujte ho a pokračujte stlačením klávesy Enter.")
                input ()


#### APP
jazyk = "sk"
mena = []
citaj_meno = True
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
    print("Connected.")
    #read("Fejsbúk","Pripojené")
    fbtts.get_roster()


def startup_q():
    print ("Prajete si spustiť program so základnými nastaveniami?\n(v slovenskom jazyku číta správy od všetkých používateľov.\nKu menu sa dá počas spojenia prisúpiť zadaním príkazu menu)")
    volba = input ("Y/n: ")
    if volba in ["Y", "y", '']:
        return
    else:
        menu()




def menu():
    cls()
    
    global jazyk, mena, citaj_meno
    if len(mena) == 0:
        i_mena = "všetci"
    else:
        i_mena = len(mena)
    
    print ("""Menu:
1 -> Nastavenie jazyka (nastavený: {0})
2 -> Nastavenie zoznamu sledovaných užívateľov (nastavených: {1})
3 -> Prečítanie mena pred správou: {2}

0 -> Spustiť

q -> exit()
""".format(jazyk, i_mena, citaj_meno))
    
    volba = input("Zdajte číslo: ")
    
    if volba == "":
        cls()
        return
    elif volba in ("q", "exit"):
        os._exit(1)
    try:
        volba = int(volba)
    except:
        cls()
        print("Chyba! Nezadali ste číslo (Integer).")
        menu()
        return
    
    if volba == 0:
        return
    if volba == 1:
        jazyk = input("Zadajte kódové označenie jazyka (napr. sk, en, de): ")
        cls()
    elif volba == 2:
        cls()
        set_users()
    elif volba == 3:
        citaj_meno = not citaj_meno
        cls()
    else:
        cls()
        print("Chyba! Zadali ste nesprávne číslo.")

    menu()



def set_users():
    cls()
    global jazyk, mena, whitelist
    if len(mena) == 0:
        i_mena = "všetci"
    else:
        i_mena = mena
    if (whitelist):
        i_wlist = "[WHITELIST] /  BLACKLIST "
    else:
        i_wlist = " WHITELIST  / [BLACKLIST]"
    
    print ("!> Momentálne sledovaní užívatelia:\n    ", i_mena)
    print ("""!> Dostupné príkazy: 
    add [užívateľ] (pridá užívateľa) 
    del [užívateľ] (zmaže užívateľa)
    clear          (vyčistí zoznam)
    wb (zmení prístup k užívateľom v zozname) """ + i_wlist)
    
    while 1:
        command = input("?> ")
        try:
            command, name = command.split(" ", 1)
        except:
            pass
        
        if command == "add":
            if name in mena: 
                print("!> Meno sa už v zozname nachádza.")
            else:
                mena.append(name)
                break
        elif command == "del":
            if name in mena: 
                del mena [mena.index(name)]
                break
            else:
                print ("!> Meno sa v zozname nenachádza.")
        elif command == "clear":
            mena = []
            break
        elif command == "wb":
            whitelist = not whitelist
            cls()
            break
        elif command == "exit":
            os._exit(1)
            exit()
        elif command == "":
            cls()
            return
        else:
            print ("!> Chybný príkaz!")

    set_users()




def id_to_name(idecko):
    url = "http://graph.facebook.com/" + idecko
    raw_data = urllib.request.urlopen(url).read()
    data = json.loads(raw_data.decode("utf8"))
    name = data["name"]
    return name


def read(name, text):
    if citaj_meno:
        toread = name + " píše: " + text
    else:
        toread = text
    print ("Reading: " + name + " píše: " + text)
    uurrll = "\"http://translate.google.com/translate_tts?tl="+jazyk+"&q="+toread+"&ie=UTF8\""
    if os.name=="nt":
        subprocess.call(player()+uurrll, startupinfo=startupinfo)
    else:
        x(player()+uurrll+" &> /dev/null")

def message(msg):
    if msg["type"] in ("chat","normal"):
        rmsg = msg["body"]
        #if rmsg == "exitni":
        #    exit()
        #print (msg)
        
        froms = str(msg["from"])
        idecko = froms[froms.find("-")+1:froms.find("@")]
        name = id_to_name(idecko)
        
        if len(mena) == 0:
            read (name, rmsg)
        else:
            if (name in mena) == whitelist:
                read (name, rmsg)
            else:
                print(name + " píše: " + rmsg)
        #msg.reply('Thanks').send()


def kvit():
    inpul = input()
    if inpul == "exit":
        print ("Exitting...")
        os._exit(1)
    elif inpul == "menu":
        menu()
	#elif inpul sem dame ak napise bodku a medzeru tak..
    kvit()



def check_username(usrn):
    url = "http://graph.facebook.com/" + usrn
    try:
        raw_data = urllib.request.urlopen(url).read()
        data = json.loads(raw_data.decode("utf8"))
        try:
            data["error"]
            return False
        except:
            return True
    except:
        return False


def get_info():
    #global jid, password
    jid = input("Username: ")
    while not check_username(jid):
        print ("Zadajte správne prihlasovacie meno.")
        jid = input("Username: ")
    jid += "@chat.facebook.com"
    password = getpass.getpass("Password: ")
    return jid, password



def main():
    startup_q()
    
    jid,password = get_info()
    server = ("chat.facebook.com", 5222)

    print ("Connecting... (môže trvať niekľko minút)")
    Loading.start()
    threading.Thread(target=kvit).start()
    
    global fbtts
    fbtts = ClientXMPP(jid,password)
    fbtts.add_event_handler("session_start", session_start)
    fbtts.add_event_handler("message", message)
    fbtts.auto_reconnect = True
    fbtts.connect(server)
    fbtts.process(block=True)

if __name__ == "__main__":
    main()
