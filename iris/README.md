### IRIS
Mass Social Engineering tool and Email and Account Extraction (Random Brute Force Discovery) and Password Brute Force through Tor.
- Automatic Random Email and Password generation.
- Load Email dumps too.
- Mass Emailer with your Malacious Attachment (no Email dump required, but can be loaded).
- Random Brute Force Discovery. Get Accounts that use Weak passwords on Instagram.
- Classic Brute Force on Instagram.

#### Why only Instagram?
People tend to use weak combinations on Instagram Alot.
And it's easier because I found a Module to Brute Force easily over Tor.

#### Brute Forcing Accounts over Tor
Every Single account brute forced by this tool is over Tor because of [Instagram-Py](https://github.com/deathsec/instagram-py).
On a successful login attempt, They will receive a notification which looks like this.

![ALERT](https://github.com/quantumcored/paradoxia/blob/master/iris/alert.png)

#### Mass Email
You can send Emails with malacious or legitimate attachments to Random emails, Or use an email list to send to.

#### Random Brute Force Discovery
Call it a Crazy idea that'll never work but,
``Random Brute Force Discovery`` is a method I've created, A different type of Brute force.
It works by generating random emails and passwords and checking if they work,
If they work, save them, if they don't, keep on working.
The random email:password is generated like this for example: \
``bob2003@gmail.com:bob12345`` \
Leave it running without quitting for long periods of time to discover accounts that use weak Passwords.

#### USAGE
Mass Emailer
```bash
$ cd IRIS
$ ./iris.py -email myemail@service.com -password myemailpassword 
```

Password Spraying
```bash
$ ./iris.py -discover-instagram true
```

Brute Force over Tor only
```bash
$ ./iris.py -bruteforce-instagram true -instagram-user < username > -instagram-list < password list > 
```
