# Remote Nuke It
Remote Nuke It is a software package for anyone who wants to remotely and 'securely' delete (nuke) one or more pre-defined files. It utilizes a Python script 
(optionally compiled into a standalone .exe), a 3rd party command-line secure file erase program, a very simple web server based on NodeJS, and a client via 
web browser (this makes the client platform/OS independent).

Warning - I am not a professional programmer so use at your own risk! I almost deleted the contents of one of my network drives on accident just because 
of a typo when developing this. Use with extreme caution!

You'll notice that I use the term 'securely delete' throughout this page. It is because the means to how this is all set up to delete files is through a
program called SDelete which you can configure to run multiple passes over your file(s) so that they are unrecoverable. If you weren't aware, when you
delete a file/folder in Windows, it's not actually gone. Even when you empty the Recycle Bin. I'm not going to go into the details here, but just know
that if you want something truly gone (unrecoverable), you have to 'securely delete' it/them.

## DISCLAIMER
I am not responsible for how you use this software, nor am I responsible for any files/directories you delete intentionally, or on accident! Use 
this software at your own risk! (Yes I know I already stated the whole 'use at your own risk' thing, but it's important to know that you are solely 
responsible for what happens on your computer(s) when using this software)

## Quick Overview / How it all Works
There are 3 major components to this software:
1. The Target. This is the computer that you would want to delete the file(s) from.
2. The Communication Server. This acts as a go-between for The Target and The Trigger (next)
3. The Trigger. This is FROM where you send the command to execute the remote deleting.

All communication is done via HTTP, not HTTPS, so please keep that in mind. Also keep in mind that there will be a delay between when you send the
command to execute the nuking of the files, and when it actually happens. However, this delay can be controlled in a config file (more on that later).

Here is how the flow works:

Let's say you have a computer that contains files you may want to delete files (The Target) remotely, which we'll call WorkstationA, which is located 
in your home. And you have a computer that is accessible from the Internet (maybe it's a cloud VM) called ServerA. And you have a smartphone that we'll 
call TriggerA. You're on the road and you realize that you need those files on WorkstationA securely deleted ASAP! You take your smartphone (TriggerA),
and point the phone's browser to a special URL (which is going to ServerA). That action will modify a special file on ServerA. Next time WorkstationA
checks in with ServerA, it will receive notice that it needs to delete your files, and does so immediately. Crisis averted!

Hopefully this is obvious, but in order for you to be able to remotely nuke your file(s) at any time of the day on any given day, The Target and The 
Communication Server both need to be running 24/7.

If this is something that you could use and want to set up, then read on!

## IMPORTANT - READ THIS BEFORE CONTINUING!!!
After you get your software all set up, SET UP A TEST DIRECTORY/FILES and run a nuke test with fake/test data! You need to make sure that it is working 
as you expect it to work before running on your real data! Because again, if you delete something on accident, it will NOT be recoverable! Or, if you 
*think* everything is working and the time comes to when you really need to delete your file(s), but it's not actually working...well, you get the point, 
right?

## Pre-requisites / Brief Summary
I go into more detail about all of the following items in the 'Setup / Installation Intructions' section below, so if you're not comfortable doing 
these things on your own right now, feel free to treat this section as a quick heads up on what we're going to do. 
- For The Target (the computer that has file(s) that you may want to remotely 'nuke'):
  - File(s) that you want to securely delete
  - A copy of SDELETE.EXE - https://learn.microsoft.com/en-us/sysinternals/downloads/sdelete Please read and understand the information that is presented
  on this page before proceeding.
  - This may be obvious, but you would also want your Target to be running 24/7 so that it's always available to receive the 'nuke' (delete) signal
  - Lastly, you need either:
    - If you want to use the .exe I provide here as is, then the .exe should be be sufficient, nothing else is needed. (I do not recommend this because 1.
    You will learn more if you do this the next way, and 2. You should never just download and run .exe files from random people on the Internet) **OR**
    - Python (https://www.python.org/), and the .py script that I provide here. **AND optionally (but recommended)**:
      - The pyInstaller package (`pip install pyinstaller`) if you want to turn your script into a standalone .exe
- For the Communication Server:
  - A copy of NodeJS, which can be downloaded from: https://nodejs.org/en/ (The script provided here was created with and successfully used with v18.12.1,
  although newer versions should work). Side note - I used the 'Windows Binary (.zip)' (aka Portable) version so that I didn't have to actually 'install' it
  on my system. I am running my communication server on a Windows system, but it should run on Linux too, possibly even with no changes to the .js file.'
  Here is a direct link to the one I used: https://nodejs.org/dist/v18.12.1/node-v18.12.1-win-x64.zip (Note that the link may be moved/dead in the future)
  - Your communication server needs to be accessible from anywhere on the Internet. You can run it on your home computer, but you will need to open up a
  port forward on your router to accommodate the approriate port and IP address. There are guides on how to do this at: https://portforward.com/
  - This may be obvious, but you would also want your communication server to be running 24/7 in order to access it anytime you need
- For The Trigger (the device you use to send the nuke command):
  - An Internet-connected device that can access a web page/URL. i.e. Chrome, Firefox, Edge, Safari, Brave, etc.
    - Note that you want to be careful on how easy you make this for yourself - you could theoretically bookmark the URL that way it's just a couple clicks,
    but what if you accidently click on that bookmark some day? Then it's bye bye files! What I do is use a (smartphone/tablet) app called HTTP (Request)
    Shortcuts - https://play.google.com/store/apps/details?id=ch.rmy.android.http_shortcuts&hl=en_US&gl=US&pli=1 This way I have to go into the app
    and then click on the trigger. This forces me to go into this special app (not a web browser), and then click on the shortcut. I do not place the
    shortcut directly on my phone's desktop, because once in a while I'll accidently click on an app that I didn't mean to. Hopefully you get my point.
 
## Setup / Installation Intructions
### The Target - the computer you may want to delete one or more files from
As I mentioned earier, you have 2 routes to go:
- Option A - Download the .exe provided here (stealthy), **OR**
- Option B - Download and install Python, download the Python script provided, and tweak if needed.
  - From here, you can choose to have the Python script be constantly running in a CMD window (not very stealthy) **OR**
  - Compile the Python script into an .exe to which you can have constantly be running, but invisibly (stealthy)
  
But first, create a folder on your C: drive for your stuff. You can call it 'RemoteNukeIt' for instance. The result may look like: C:\RemoteNukeIt. Now 
proceed on with Option A **OR** Option B

#### Option A - Download the .exe provided here
Again, this is not the recommended path. I recommend you use Option B instead. The reason is two-fold - you shouldn't download and run .exe files from
strangers on the Internet. It can be dangerous if you're not careful. And you'll gain some experience if you go with Option B. But if you must, here 
you go:
1. Download the `RemoteNukeItConfig.yaml` file and the `RemoteNukeIt.exe` file from this repository into the new directory you just created.
2. Assuming you don't want to manually launch the .exe everytime you start Windows, you can have the .exe start automatically with Windows. There 
are a few ways to do this, but one of the easiest ways is to press and hold the 'Windows key' on your keyboard, then press 'R'. This will pop open a window
where you want to type: "shell:startup" (without the quotes), then hit the 'Enter key' on your keyboard. In the window that pops up, create a shortcut
to your .exe file. That's it - next time you (re)-start Windows, it will run automatically for you!

Do not manually launch your `RemoteNukeIt.exe` program yet. And do not reboot your computer to test the auto-launching upon startup yet. You still need to 
configure the `RemoteNukeItConfig.yaml` file. And you can't do that until you set up the Communication Server. So continue with the instructions on this 
page right after Option B, which is the 'SDelete' section. When you finish with the 3 main sections of this tutorial, you can then do the 
'RemoteNukeItConfig.yaml' section. Once you're done with that, *then* you can either launch the `RemoteNukeIt.exe` program or reboot.

#### Option B - Download and install Python, download the Python script, and optionally compile into an .exe yourself
Again, this is the preferred route. You will gain a little experience and knowledge if you go this way. And you won't be downloading an .exe from a stranger 
and running it on your computer. ;)

If you already have Python installed on your system, you can skip to step #2.

1. Download and install Python on your system. You can download Python at the following address: https://www.python.org/ Note that during the install, I 
recommend you let the setup add a 'PATH' to your environment variables so that you can run the Python executable from any location on your hard drive.
2. Download the `RemoteNukeItConfig.yaml` and `RemoteNukeIt.pyw` files from this repository into your new directory. 
3. (Optional) Open the `RemoteNukeIt.pyw` Python script in a plain text editor (Notepad, Notepad++, Sublime, etc.), and make any changes you want to make. In 
reality, you shouldn't really need to make any changes, but feel free to.
4. If you want to run the Python script as a script, follow the following bulleted steps because what you need to do now is create a shortcut in your startup 
folder so that whenever you (re)start your computer, it runs automatically for you. The shortcut will point to your python.exe executable and you'll 
provide the path to your Python script as a parameter:
(If you would like to run it as a compiled .exe instead, which is recommended, skip the below bulleted steps and continue on to Step 5 below)
    - Press and hold the 'Windows key' on your keyboard, then press 'R'. This will pop open a window where you want to type: "shell:startup" 
    (without the quotes), then hit the 'Enter key' on your keyboard. 
    - In the window that pops up, create a shortcut to your Python executable. It will probably be something like:
        - *C:\Users\myusername\AppData\Local\Programs\Python\Python38-32\python.exe*
    - Now go ahead and edit it (right-click, choose 'properties').
    - Go the 'Shortcut' tab if not already there
    - Look in the 'Target' field. Put your cursor at the end of the entire path (after the .exe).
    - Now hit the spacebar, and now enter the full path to your Python script. (Note that if there are any spaces in the path, you will need to enclose the 
    path in quotes (""). So now the 'Target' field should look something like:
      - *C:\Users\myusername\AppData\Local\Programs\Python\Python38-32\python.exe C:\RemoteNukeIt\RemoteNukeIt.pyw*
    - Click OK
    - (Optional) Rename the shortcut (right-click, choose 'rename') to whatever you want (i.e. Run RemoteNukeIt)
    - Next you need to open up the `RemoteNukeIt.pyw` file in a text editor and provide full paths for the LOGFILE, CONFIGFILE, and EXECUTABLEFILE 
    constants. Currently they're set to relative paths. For example, for the 'LOGFILE', you would need to change it from 'RemoteNukeItLogFile.txt' to 
    'C:\RemoteNukeIt\RemoteNukeItLogFile.txt'
    - That's it - next time you (re)-start Windows (but don't do this yet - you need to finish all the way through the 'RemoteNukeItConfig.yaml' section, 
    and *then* you can reboot), it will run automatically for you. You can skip the remaining steps in this section - so head to the SDelete section now
5. If you would like to compile your Python script into an .exe so that it is easier to run (and is more portable), and more 'stealthy', let's do that:
    - I suggest you make a temporary directory on your hard drive. Maybe something like *C:\PythonTemp*
    - Copy the `RemoteNukeIt.pyw` into that temporary directory
    - Hopefully you let Python add itself to the PATH of your environment variables as I suggested earlier during the installation of Python. This allows
    you to run the Python.exe and pip.exe from anywhere on your computer without specifying the full path to the .exe. If that is the case, then you
    can just run:
    `pip install pyinstaller` from the command line located anywhere on your computer to install the 'pyinstaller' package. You can just try that 
    command and see if it works. If it does not, then you'll need to provide the full path:
      - For example: `C:\Users\myusername\AppData\Local\Programs\Python\Python38-32\Scripts\pip.exe install pyinstaller`
    - Open a command prompt into your temporary location you created a minute ago (C:\PythonTemp)
    - Next, all you do is run: `pyinstaller --onefile RemoteNukeIt.pyw`
    - Now you should have a standalone .exe file named `RemoteNukeIt.exe` under the 'dist' subfolder that PyInstaller just made
    - Copy `RemoteNukeIt.exe` into the *C:\RemoteNukeIt* folder you made earlier
    - It is now safe to delete the entire temporary directory you made (i.e. *C:\PythonTemp*)
6. Assuming you don't want to manually launch the .exe everytime you start Windows, you can have the .exe start automatically with Windows. There 
are a few ways to do this, but one of the easiest ways is to press and hold the 'Windows key' on your keyboard, then press 'R'. This will pop open a window
where you want to type: "shell:startup" (without the quotes), then hit the 'Enter key' on your keyboard. In the window that pops up, create a shortcut
to your .exe file. That's it - next time you (re)-start Windows, it will run automatically for you!

However, do not manually launch your `RemoteNukeIt.exe` program yet. And do not reboot your computer to test the auto-launching upon startup yet. You 
still need to configure the `RemoteNukeItConfig.yaml` file. And you can't do that until you set up the Communication Server. So continue on with the 
instructions on this page, which is the 'SDelete' section. When you finish with the 3 main sections of this tutorial, you can then do the 
'RemoteNukeItConfig.yaml' section. Once you're done with that, *then* you can either launch the .exe or reboot.

#### SDelete
Regardless of whether you went with Option A or Option B, you'll need the command-line utility called SDelete. You can download it from Microsoft from this 
link: https://learn.microsoft.com/en-us/sysinternals/downloads/sdelete
Once it's downloaded, put it into the new folder you created from the beginning of this section's (The Target) instructions above (i.e. *C:\RemoteNukeIt*). 
Double-click on it once to launch it. This will give you an agreement window. Agree with the terms if you do, and you're good to go. The reason why we 
run it this one time is because you need to agree to the terms. If you don't, it will pop up this window the first time it's run, and you don't want this 
when Remote Nuke It is trying to nuke your file(s) for you automatically. No need to open/run it anymore manually after this. 

You can read all about how SDelete works and the command line arguments for it on the page you downloaded it from. 

Now onto the Communication Server

### The Communication Server - the middleman for The Target and The Trigger
This computer is the one that will run the NodeJS web server. It acts as a go-between to The Target and The Trigger. This could be the same 
computer as the one you're running The Target on. Or it could be on another computer on your network. Or it could be a cloud computer. Your choice. 
Just know that it needs to be running 24/7 if you want it to be available 24/7. I'm splitting up this into 2 parts because they're quite different. 
Part 1 is getting the software ready. Part 2 is some extra stuff that you most likely need to do, but I'm considering separate.

#### Part 1 - the Remote Nuke It software

1. Download (and extract/install) NodeJS from: https://nodejs.org/en/
  - Notes:
    - You can download an installable version or a 'portable' version. I opted for the 'portable' version. If you go this way, you need to create 
  a folder on your hard drive manually and put the .zip file in there, then extract the contents into that folder. On my computer, I created a folder 
  called: "C:\NodeJS v18.12.1". 
    - If you want to use the exact same version as I did, here's a direct link for your convenience: 
    https://nodejs.org/dist/v18.12.1/node-v18.12.1-win-x64.zip
    - As you may be able to tell from the link, I used v18.12.1, but any version from that version onward should work
2. Download the `RemoteNukeItCommSrv.js` file from this repository into the same directory that your new NodeJS directory resides in.
3. Open the `RemoteNukeItCommSrv.js` in a plain text editor (i.e. Notepad, Sublime Text, Notepad++, etc)
4. Change the value of the 'host' constant. You need to make it the local IP address of the computer that is running the NodeJS
server. If you need instructions on how to do this, see the following page: https://www.avast.com/c-how-to-find-ip-address#. Follow the instructions for 
finding your *local* (not public) IP address for whatever version of Windows you have. Once you find your local IP address, change the current value to 
yours. So for example, after you change the address, that whole line may look something like:
`const host = '192.168.0.5';`. Whatever you change it to, make a note of it - at the very least you're going to need it when editing the 
`RemoteNukeItConfig.yaml` file near the end of this tutorial. And most likely you'll need it next in 'Part 2'.
5. (Optional) - The port that the script is set to run on is **8003**. If you would like to change this, then look for the line that says:
`const port = 8003;` and change the value from 8003 to your preference. Whatever you change it to, make a note of it - you're going to need it when 
editing the `RemoteNukeItConfig.yaml` file near the end of this tutorial
6. Download the `B5HJU9QF0SP3WI8MNX4A.txt` file from this repository into your NodeJS folder. After you do this, I highly recommend you rename this to 
something else. Make it fairly long, and do not use special characters. Use only uppercase letters and numbers. i.e. F876BPQOCN61CVX.txt or 
P50ZA7LNH4T0RRW2.txt.
7. Whatever you renamed the file to, make a note of it - you'll need that info when you edit the `RemoteNukeItConfig.yaml` later. 
8. We want NodeJS and the `RemoteNukeItCommSrv.js` script to run automatically when your computer boots. Navigate to the folder that NodeJS was installed 
in, or to the folder that you created and extracted the contents of the .zip file into if you downloaded the portable version.
9. Right-click on the `node.exe` file, and click on 'Create Shortcut'
10. Right-click on the new shortcut (it's probably called `node.exe - Shortcut`), and choose 'Properties'
11. In the 'Target' field, put your cursor after the last '"' at the very end of the path. Hit spacebar to make a space, then enter the name of the .js file
which should be `RemoteNukeItCommSrv.js`. So an example of what is in the 'Target' field may look like this: 
`"C:\NodeJS v18.12.1\node.exe" RemoteNukeItCommSrv.js`
Before hitting OK on this window, let's give the shortcut a better name...
12. Click on the 'General' tab
13. Near the top should be a field with a current value of "node.exe - Shortcut". Change that to something else like "Run Communication Server", or whatever 
will help you remember what it is.
14. Click OK
15. Now we want to actually put this new shortcut in the correct place so that it launches every time Windows starts. Right-click on the new shortcut that 
you just made, and choose 'Cut'.
16. Press and hold the 'Windows key' on your keyboard, then press 'R'. This will pop open a window where you want to type: "shell:startup" (without 
the quotes), then hit the 'Enter key' on your keyboard. Now paste the shortcut into this location and you're done. Next time you (re)-start Windows, 
it will run automatically for you!
    - Note that there are other ways to get NodeJS and the .js script to launch automatically with Windows, but this is one of the easier/safer methods.


#### Part 2 - Making it accessible from the outside

(If you never intend to send the trigger signal from outside of the network that your Target is on, then you can skip this whole Part 2 section. But I 
doubt that is the case)

Your Communication Server needs to be accessible from anywhere in order for you to send the trigger signal from anywhere. If it's on a PC on your home 
network (as opposed to a 'cloud' machine), it most likely won't be accessible from outside your network because of how your router works. This means you 
can't send the trigger signal from outside your home network. What you need to do is set up a 'port forward' (that's what most router manufacturers 
call it) on your router to allow a specific kind of traffic (http) on a specific port to your Communication Server.

I can't tell you exactly how to do this due to there being so many routers out there, but I can give you the information you need to figure out how to do 
it yourself.

There are 3 pieces of information you'll need to set up the port forward:
1. Your Communication Server IP address (this is the IP address that you just took note of in Step 4 above)
2. The port that your Communication Server is running on (unless you changed it in Step 5 above, it should be 8003)
3. Protocol - if it asks for TCP or UDP, choose TCP

Now that you have those 3 pieces of information you can add a port forward on your router. If you don't know how to do this, check out the following website: 
https://portforward.com/ 
Doing this is out of the scope of this readme so the above link is your best bet. It has articles/instructions how to set up port forwards on many many 
different router manufacturers and models, so they most likely have instructions for whatever your have. Once you do that, then we probably need to do 
one more thing:

Your Public IP address probably changes from time to time (Dynamic IP address). A sure way to find out if you have a Dynamic IP (likely) is to contact your 
ISP and ask them if you have a Dynamic IP (a changing Public IP) or a Static IP (fixed Public IP - never changes). If you have a Static IP, that will make 
your life a little easier. Then you can just go to:
https://whatismyipaddress.com/ which will show you your IPv4 address. This is your Public, or WAN IP address. Take note of it - you will need this for The 
Trigger. You can stop here in this section and move on to The Trigger section.

However, if you have a Dynamic IP address, you will need to do some more work. Remember, if you have a Dynamic IP address, that means it will change in the 
future. You won't know when it changes or what it changes to. Once it changes, then your Trigger will not work anymore. This is obviously a problem. So, in
order to get around this, you need to use a Dynamic DNS service. Here is a free one you can use: https://www.noip.com/
Sign up for an account, choose a host name (i.e. jimsremotenukeit), install the software client on your computer (or configure it on your router if it 
supports it - many newer routers do). When you're all done, you won't need to use an IP address - you'll use an address/URL like:
jimsremotenukeit.hopto.org.

Take note of your new address when you make the account - you'll need it for The Trigger.



### The Trigger
This is the device (it could be a smartphone, tablet, laptop, Chromebook, PC, etc.) that you use to trigger the secure deletion of your files. All you 
really need is a browser. You just point your browser to your IP address (if you have a 'Static IP address') or URL (if you have a 'Dynamic IP address'), 
with some querystring name/value pairs like this:
http://1.2.3.4:8003/?CID=T8VIP4DX3M0J3SZ&requestreason=execute
Your trigger URL will be different. You would replace the '1.2.3.4' with either the 'Public IP' address (if you have a 'Static IP address') 
that you took note of earlier in the Communication Server section OR the Dynamic DNS URL (if you have a 'Dyanmic IP address') that you set up 
(i.e. jimsremotenukeit.hopto.org) in the Communication Server section. So your full trigger URL would look something like:

http://96.186.45.67:8003/?CID=T8VIP4DX3M0J3SZ&requestreason=execute

**OR**

http://jimsremotenukeit.hopto.org:8003/?CID=T8VIP4DX3M0J3SZ&requestreason=execute

Next, another possible change you may need to make to the full trigger URL would be the port number. If you recall, the 'default' port number is 8003. But 
if you changed it, you would need to change your full URL. For example, if you changed it to 8093, your URL might look something like:

http://96.186.45.67:8093/?CID=T8VIP4DX3M0J3SZ&requestreason=execute

**OR**

http://jimsremotenukeit.hopto.org:8093/?CID=T8VIP4DX3M0J3SZ&requestreason=execute

Lastly, you will want to the change the value after 'CID'. Here you will want to change the value to whatever the file name you decided to create in 
Step 6 of the Communication Server section. For example, if you changed your file to be named 9I440S1PRQM7FX0TE2.txt, you would make your URL look 
something like this:

http://96.186.45.67:8093/?CID=9I440S1PRQM7FX0TE2&requestreason=execute

**OR**

http://jimsremotenukeit.hopto.org:8093/?CID=9I440S1PRQM7FX0TE2&requestreason=execute

So, now that you have your final URL, that's the last thing you really need to know. At any time, from any browser, from any location you have Internet 
access, from any device, you can just point your browser to that URL, and voila! Your pre-defined file(s) on The Target computer will (permanently!) 
disappear within the time frame you specified in your .yaml file!

Again, be very careful how you 'save' this URL - you could create a browser bookmark for it, but just be very careful not to click on it on accident! 

What I do, is I use an app called HTTP Request Shortcuts. If you're on Android, here's a link: 
https://play.google.com/store/apps/details?id=ch.rmy.android.http_shortcuts&hl=en_US&gl=US&pli=1
It's pretty straightforward to set up. You add/create a 'Regular HTTP Shortcut'. Give it a name, and description, and for the URL, enter your full 
URL that we just figured out. For the 'Method' make sure it says 'GET'. Save it, and back on the app's home screen will be your new shortcut. When you 
need to nuke your files, you just open the app, tap the shortcut and boom. Bye bye files!

#### Possible caveat

Depending on your router, you may not be able to use The Trigger using the above URL from the same network that your Communication Server is on. 
For instance, if your Communication Server is on your home network, and you use another computer that is on your home network, or say a mobile device that 
is on the same network, you can't use the same URL. 

This is another reason for full testing of everything. So do a test with some test files. If this works, then great, but if not, then you'll want to 
make note of a different URL. Instead of using the Dynamic DNS name (i.e. jimsremotenukeit.hopto.org), or Public IP (i.e. 96.186.45.67), you'll want to 
replace it with the local IP address of your Communication Server. You should already have note of this from the Communication Server section above. 
So for instance, if the local IP address of your Communication Server is: 192.168.1.4, then the URL for The Trigger when you're on the same network, would 
be something like: 

http://192.168.1.4:8003/?CID=9I440S1PRQM7FX0TE2&requestreason=execute

Assuming you left the port number to the default of 8003, and the file you have on the Communication Server is named: 9I440S1PRQM7FX0TE2.txt.

So if you already created a bookmark for your trigger, just create a new one with the appropriate URL for internal use, and name the bookmark slightly 
different using the word 'internal' or something like that. 

If you are using the HTTP Shortcuts app like me, just create a new shortcut with a different name (maybe include the word 'internal' for this one), with 
the slightly modified full URL. 

When you're on the same network as the Communication Server and want to send The Trigger signal, use this 'internal' bookmark or HTTP Shortcut, and you're 
good to go!


## RemoteNukeItConfig.yaml
This is the important configuration file for the .exe or Python script on The Target. If you don't configure this file correctly, the .exe or Python 
script won't run properly (or at all).

It is important you understand how to enter the correct values in the file. At the very least you're going to need to make 2 changes to this file: 1. the 
list of files you want to delete, and 2. The IP of the Comm Server. Be careful when editing this file. Keep the formatting the way it is with the spaces 
and 'tabs', etc. Yaml files need to be formatted a specific way. If you want to learn more about this, search Google for something like 'anatomy of a 
.yaml file'. Moving along, let's get your file configured. Open up your `RemoteNukeItConfig.yaml` file in a plain text editor (i.e. Notepad, Sublime Text, 
Notepad++, etc.) and let's make some changes:
  - Under the 'commserver' section:
    - IP - this is the IP address of your Communication Server (the one running the NodeJS web server). If you followed the instructions properly, you 
    would have made a note of this address in the Communications Server section at Step 4 of Part 1. Even if you're running the Communication Server on the 
    same PC as your Target PC, you still need to put the address here.
    - Port - this is the port number that the Communication Server (the one running the NodeJS web server) is running on. You should have taken note of 
    this number in Step 5 of Part 1 of the Communication Server section), so match it to that. If you recall it was set to 8003, so unless you changed it, 
    that's what you want it to be here.
  - Under the 'client' section:
    - ID - back in Step 6 of of Part 1 in the Communication Server section, you renamed a .txt file to a series of random characters and numbers and made 
    a note of it. Whatever that is, change the ID here to that. But note that you do not include the '.txt' part - just the first part of the filename.
      - For example, if you renamed your .txt file to T8VIP4DX3M0J3SZ.txt, then you would enter T8VIP4DX3M0J3SZ as the value for 'ID' in the .yaml file
    - Interval - this is how often the Python script (or .exe file) will check in with the Communication Server. The value is in seconds. So the smaller 
      the number, the more frequently the Target will check in with the Communication Server. Therefore a smaller number will decrease the time delay 
      between when the Trigger sends a request to nuke your files and when it actually happens. And conversely, a larger number will increase the time 
      delay.
  - Under the 'nukelist' section:
    - This is a file, or list of files, or directory, or directories, or any combination of those that you want to delete data from. Please note that 
      although using something like the \*.\* wildcards (like the 1st entry in the .yaml file provided here), the SDELETE program will recursively delete 
      any and all files in subdirectories, BUT it will **NOT** actually delete the subdirectories themselves. Apparently this is a bug in SDELETE. So just
      be aware of this unfortunate behavior. It's not a big deal in my case, but maybe it is in yours. If it *is* a big deal in your case, then you would 
      need to find another command-line program that can securely delete files, and make the adjustments in the Python script accordingly.

You are done with this file now. If your Communication Server isn't running, go ahead and run it. And finally, *now* you can manually launch the 
`RemoteNukeIt.exe` file (or the `RemoteNukeIt.pyw` Python script) manually if you want, or reboot your computer to make sure that you've got either of 
those configured to launch with Windows set properly. 

Enjoy!

## Frequently Asked Questions (FAQs)
Q. Can I have the Communication Server (the NodeJS web server) run on the same machine as the Target (the computer you may want to delete files on)?

A. Yes, absolutely!

Q. Can I have the Communication Server (the NodeJS web server) run on Linux?

A. This should definitely be possible (although I haven't *fully* tested that yet). NodeJS is pretty much platform independent so it doesn't care what
it is running on (you would just need to download/install the appropriate version of course). There are NodeJS packages available for Windows, Linux, 
and MacOS.

Q. I can successfully nuke my files on my home PC (The Target) when I'm away from my home, but when I'm at home it doesn't work - I get an error on 
The Trigger. What's going on?

A. Your router probably doesn't support 'NAT Traversal'. Please see the 'Possible Caveat' sub-heading under 'The Trigger' section

Q. How do I know that the .exe is actually running properly on The Target since there's no window?

A. There's a couple things you can do. First look in the directory (remember C:\RemoteNukeIt ?) that you created in The Target section of this Readme. 
If there is a file called `RemoteNukeItLogfile.txt` then open that up. If there is no file called that and you know you launched the .exe properly, then 
it's most likely running just fine. We can double-check by opening your 'Task Manager' and looking for 'RemoteNukeIt.exe' in there. If it's there, then 
you're good to go.

Q. Is it OK to have spaces in directory and/or file names in the list of items to be nuked in the .yaml file?

A. Yes

Q. How to I stop the `RemoteNukeIt.exe` if I need to?

A. Open up Task Manager, find `RemoteNukeIt.exe`, right-click, and choose 'End Task'. There may be 2 of them for some reason (I don't know why), so you 
may need to end both. (I noticed that if you click on one of them then both will end sometimes)

## To Dos 
  - Add an email function to notify user when files have been nuked
  - Fix bug on Communication Server: sometimes when 'checking in', it will recognize that a matching file exists, and says so properly on the console, but 
  for some reason will also spit out an extra line that says that the file does not exist. This seems to happen more in Firefox
  - Add a 'cancel nuke' option?
  - Add a nuke confirmation step?





