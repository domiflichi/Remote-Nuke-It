import yaml
import requests
import subprocess
from time import sleep
from datetime import datetime



# To dos:
# 1. Add email/msg notification if nodejs server is down ??? Necessary ???
# 2. Add email/msg if/when execution takes place ??? Necessary ???
#


# Codes from NodeJS server:
#
# 000 = 'Nojoy' / Nothing to do
# 111 = Web server could not find corresponding file (Log this on client side!)
# 222 = Execute / Nuke! (Log this on client side!)
#


# Constants
LOGFILE = 'RemoteNukeItLogfile.txt'                                                     # Constant that defines location and name of our logfile
CONFIGFILE = 'RemoteNukeItConfig.yaml'                                                  # Constant that defines location and name of our configuration .yaml file
EXECUTABLEFILE = 'sdelete.exe'                                                          # Constant that defines location and name of our command line driven secure file deletion executable file

# 'Global' variable
textResponseFromCommServer = ''                                                         # Variable to hold the response given from our Communication Server



# Our little log writing function for when something goes wrong
def writeToLogFile(textToWrite):

    dt = datetime.now()                                             # Variable to hold the date. Initialize to the current date/time (will format it soon)
    t = datetime.now()                                              # Variable to hold the time. Initialize to the current date/time (will format it soon)
    dt = dt.strftime('%m/%d/%Y')                                    # Format our current date variable to be: MM/DD/YYYY
    t = t.strftime('%X')                                            # Format our current time variable to be: HH:MM:SS

    file1 = open(LOGFILE,"a")                                       # Open logfile for 'a'ppending data to it
    file1.write(dt + " " + t + " " + textToWrite + "\n")            # Write out a line, formatted with the data and time and the message that was passed to it
    file1.close()                                                   # Closet the file - we're done




# Function to launch our external program windowless (I did not write this function. I found it somewhere and just modified it slightly)
def launchNukeWithoutConsole(command, args):
    # """Launches 'command' windowless and waits until finished"""
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    return subprocess.Popen([command] + args, startupinfo=startupinfo).wait()



try:
    # Read the config file and assign variables
    with open(CONFIGFILE) as file:                          # Open our config file
        try:                                                # Try, and if successful:
            mydict = yaml.safe_load(file)                   # Read the contents of the file into our 'mydict' dictionary

                                                            # Create and assign new variables and dictionaries to hold the various items from the config file
            serverdict = mydict['commserver']
            ServerIP = serverdict['IP']                     # The IP address of the Communication Server
            ServerPort = serverdict['Port']                 # The port of the Communication Server

            clientdict = mydict['client']
            ClientID = clientdict['ID']                     # The client ID. Hopefully something fairly long (I.e. DL78CAMA1GP02MXWLGH3PFN362)
            LoopInterval = clientdict['Interval']           # The interval (in seconds) of how often the script will check in with the Communication Server

            filelist = mydict['nukelist']                   # This is the list of files to be nuked if given the go-ahead
          
        except (yaml.YAMLError, KeyError) as exc:                       # If something went wrong (maybe a formatting issue or something)
            writeToLogFile("KeyError on: " + str(exc))                        # Write/pass the problem on to our log file
            raise SystemExit(exc)                           # And quit. Because if we have a problem at this step, then it's useless to go any further



except (FileNotFoundError, PermissionError, OSError) as fileReadError:                      # If there was some kind of issue finding/reading/opening/etc. the file
    writeToLogFile(str(fileReadError))                                                      # Write/pass the problem on to our log file
    raise SystemExit(fileReadError)                                                         # And quit. Because if we have a problem at this step, then it's useless to go any further




# Now everything else / below will run in a loop
while(True):


    
    try:                                                                                                                            # Try to access the communication server
        #r = requests.get('http://www.dksierndmkdfjklssdf.com')                                                                     ### Uncomment this line to test an invalid website call ####
        r = requests.get('http://' + str(ServerIP) + ':' + str(ServerPort) + '/?CID=' + ClientID + '&requestreason=checkin')        # Execute the request using the ServerIP, ServerPort, and ClientID variables that were acquired from the .yaml file
        textResponseFromCommServer = r.text                                                                                         # Assign the text returned from the server to our appropriate variable
    except requests.exceptions.RequestException as e:                                                                               # If we can't,...
        writeToLogFile(str(e))                                                                                                      # Then write the error out to our log file





    # Our if/then structure to decide what to do after receiving a response from the Communication Server
    if textResponseFromCommServer == '000':                                                                             # If '000'
        pass                                                                                                            # Then there's nothing to do - it's just a checkin
    elif textResponseFromCommServer == '111':                                                                           # If '111'
        writeToLogFile("The communication server couldn't find a matching/corresponding .txt file")                     # Then the Communication Server couldn't find a corresponding text file, write this message to the log file
    elif textResponseFromCommServer == '222':                                                                           # If '222'
                                                                                                                        # EXECUTE!
        for xitem in filelist:                                                                                          # Start looping through the file list from the .yaml file
            launchNukeWithoutConsole(EXECUTABLEFILE, ["-p", "3", "-s", xitem])                                          # Note - the '-p' , '3', and '-s' will be sent as parameters to the command line program, SDELETE. '-p 3' means 3 passes, and the '-s' is to run recursively
        writeToLogFile("Execution has commenced!")                                                                      # And write to our log file that execution has commenced
    else:                                                                                                               # If any other text than the above has been returned by the communication server,
        writeToLogFile("An unknown error occurred - an unexpected response was given from the Communication Server")    # Then write a message that says as much to the logfile.


    sleep(LoopInterval)                                                                                 # Sleep for the specified amount of time (in seconds) set in the .yaml file