# == Setup file == #
## Is called from the main file, but can be ran standalone.
## Runs a setup wizard that initializes the settings.json file
## Exported information looks something like:
# {
#   "info-dir": "/etc/release-watcher"
#   projects :{
#       0: {
#           "project-owner": "owner",
#           "project-name": "project",
#           "prev-release": "0",
#       }
#    }
#}
import os, json
import relay
import add_projects
relay = relay.relay
try:
    import requests
except:
    relay("Unable to import 'requests' package. Please install via pip!")
    exit()

def init():
    ## Initialize new dictionary to insert JSON data into
    info = {}
    ## Get some basic information about the system
    homeFolder = os.path.expanduser("~")
    if "vm" in os.popen("hostnamectl | grep Chassis").read():
        relay("Running in a VM, probably a server?")
        defaultMainFolder = "/etc/release-watcher"
    else:
        relay("Assuming we're running on a PC")
        defaultMainFolder = f"{homeFolder}/.config/release-watcher"
    ## Get the desired folder from the User and add it to the empty dictionary above
    info["info-dir"] = defaultMainFolder
    info["projects"] = {}

    ## We have all the inforamation we need, now we can write it to the file
    with open("settings.json", "w") as settingsFile:
        json.dump(info, settingsFile, indent=4)

    add_projects.getNewFeeds()
    ## Verifying the write was correct
    ## TODO: initialize the folders?
    if os.path.isfile("settings.json"):
        relay("Data written successfully to `settings.json`, you should be all set!")
        exit()
relay("Settings File (settings.json) not found!")
createFile = input("Would you like to create one? [Y/n]\n\t=> ")

if createFile.lower() in ["", "yes", "y"]:
    init()
else:
    print("Okay, quitting!")
    exit()
