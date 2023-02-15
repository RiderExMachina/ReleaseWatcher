# == Setup file == #
## Is called from the main file, but can be ran standalone.
## Runs a setup wizard that initializes the settings.json file
## Exported information looks something like:
# {
#   "info-dir": "/etc/cpb"
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
try:
    import requests
except:
    print("Unable to import 'requests' package. Please install via pip!")
    exit()

def init():
    ## Initialize new dictionary to insert JSON data into
    info = {}
    ## Get some basic information about the system
    homeFolder = os.path.expanduser("~")
    if "vm" in os.popen("hostnamectl | grep Chassis").read():
        print("Running in a VM, probably a server?")
        defaultMainFolder = "/etc/cpb"
    else:
        print("Assuming we're running on a PC")
        defaultMainFolder = f"{homeFolder}/.config/cpb"
    ## Get the desired folder from the User and add it to the empty dictionary above
    info["info-dir"] = defaultMainFolder

    ## I'd like to break out the following part into its own function, but I don't know if it's worth it
    ## Keeping for now.
    ## In my case, I want to follow 3 feeds, but others may want to follow a different number. This allows for that.
    feeds = input("How many projects do you want to follow?\n\t=> ")
    ## TODO: Break this into a try-except case? Is it worth it?
    if int(feeds):
        print(f"\tOkay, let's set up your {feeds} projects.")

    links = {}
    for feed in range(1, int(feeds)+1):
        feedURL = input("Please enter the github.com url of the project you wish to follow\n\t=> ")
        ## Split the url into different chunks
        feedSplit = str(feedURL).split("/")
        ## API URL will look something like [... "repos", "owner_name", "project_name"]
        ## Normal Github URL will look something like [... "github.com", "owner_name", "project_name"]
        ## This looks for each, and assigns the number to a variable for use later
        if "repos" in feedSplit:
            owner = feedSplit[feedSplit.index("repos") + 1]
            project = feedSplit[feedSplit.index("repos") + 2]
        else:
            owner = feedSplit[feedSplit.index("github.com") + 1]
            project = feedSplit[feedSplit.index("github.com") + 2]
        print(f"\t- Received project owner {owner} with project {project}")

        ## Replace bad characters or duplicate words with something more manageable
        ## and then make a foldername from the new name
        ## TODO: Maybe add a more robust filter list?
        apiURL = f"https://api.github.com/repos/{owner}/{project}"
        if requests.get(apiURL).status_code == 200:
            print(f"\t\t- {project} verified! Adding to list")
            links[feed] = {"project_owner": owner, "project_name": project, "prev-release": 0}
        else:
            print(f"\t\t- Unable to verify {project}. Skipping for now.")
        ## send the new information to a temporary dictionary above
    ## send the information from the temporary dictionary to the main one
    info["projects"] = links
    ## We have all the inforamation we need, now we can write it to the file
    with open("settings.json", "a") as settingsFile:
        json.dump(info, settingsFile, indent=4)
    ## Verifying the write was correct
    ## TODO: initialize the folders?
    if os.path.isfile("settings.json"):
        print("Data written successfully to `settings.json`, you should be all set!")
        exit()
print("Settings File (settings.json) not found!")
createFile = input("Would you like to create one? [Y/n]\n\t=> ")

if createFile.lower() in ["", "yes", "y"]:
    init()
else:
    print("Okay, quitting!")
    exit()
