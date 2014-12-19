#!/usr/bin/python3

import sys
import subprocess
import getpass
import json
import urllib.request
import os
import threading
from os import system as x
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
    print ("Aplikácia momentálne neumožňuje prehrávanie zvuku pre Windows. Správy nebudú prečítané nahlas.")
    #exit()
else:
    while True:
        try:
            subprocess.call("mplayer", stdout=subprocess.PIPE)
            break
        except OSError:
            print ("Pre používanie je potrebné mať nainštalovaný mplayer.\nProsím, doinštalujte ho a pokračujte stlačením klávesy Enter.")
            input ()


#### APP
d_jazyk = "sk"
d_mena = []
d_citaj_meno = True
whitelist = True

def cls():
    if os.name == "nt":
        x("cls")
    else:
        x("clear")

def session_start(event):
    fbtts.send_presence()
    print("Connected.")
    fbtts.get_roster()


def startup_q():
    print ("Prajete si spustiť program so základnými nastaveniami?\n(v slovenskom jazyku číta správy od všetkých používateľov.\nKu menu sa dá počas spojenia prisúpiť zadaním príkazu menu)")
    volba = input ("Y/n: ")
    if volba in ["Y", "y", '']:
        return
    else:
        cls()
        menu(d_jazyk, d_mena, d_citaj_meno)




def menu(jazyk, mena, citaj_meno):
    #cls()
    
    #global jazyk, mena, citaj_meno
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
        menu(jazyk, mena, citaj_meno)
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

    menu(jazyk, mena, citaj_meno)



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
    x ("mplayer -ao alsa -really-quiet -noconsolecontrols -nolirc \"http://translate.google.com/translate_tts?tl="+jazyk+"&q="+toread+"&ie=UTF8\"")


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
        cls()
        menu()
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
    global jid, password
    jid = input("Username: ")
    if not check_username(jid):
        print ("Zadajte správne prihlasovacie meno.")
        get_info()
        return
    jid += "@chat.facebook.com"
    password = getpass.getpass("Password: ")



def main():
    startup_q()
    
    get_info()
    server = ("chat.facebook.com", 5222)

    print ("Connecting... (môže trvať niekľko minút)")
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