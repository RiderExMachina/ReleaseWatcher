import json, logging, os
import relay
relay = relay.relay
try:
    import requests
except:
    relay("Unable to import 'requests' package. Please install via pip!")
    exit()

def writeFeeds(old, data):
    with open("settings.json", "a") as settingsFile:
        json.dump(info, settingsFile, indent=4)

def checkExisting():
    if os.path.isfile("settings.json"):
        ## Read existing data
        with open('settings.json', 'r') as settingsFile:
            importedInfo = json.load(settingsFile)

        existing_projects = importedInfo["projects"]
    else:
        existing_projects = None
    return importedInfo, existing_projects

def getNewFeeds():
    info, old = checkExisting()
    start = 0
    if old != None:
        start = len(old)
        relay(f"DEBUG: Importing {start} previous projects")

    ## In my case, I want to follow 3 feeds, but others may want to follow a different number. This allows for that.
    got_num = False
    while not got_num:
        feeds = input("How many projects do you want to follow?\n\t=> ")
        if int(feeds):
            relay(f"\tOkay, let's set up your {feeds} projects.")
            got_num = True
        else:
            relay(f"ERROR: {feeds} doesn's seem to be a number")
    if old != None:
        links = old
    else:
        links = {}
    for feed in range(start+1, start+int(feeds)+1):
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
        relay(f"\t- Received project owner {owner} with project {project}")

        ## Replace bad characters or duplicate words with something more manageable
        ## and then make a foldername from the new name
        ## TODO: Maybe add a more robust filter list?
        apiURL = f"https://api.github.com/repos/{owner}/{project}"
        if requests.get(apiURL).status_code == 200:
            relay(f"\t\t- {project} verified! Adding to list")
            links[feed] = {"name": project, "url": "", "api-url": apiURL, "latest-release": 0, "tags": "#foss #OpenSource"}
        else:
            relay(f"\t\t- Unable to verify {project}. Skipping for now.")
        ## send the new information to a temporary dictionary above
    ## send the information from the temporary dictionary to the main one
    info["projects"] = links
    ## We have all the inforamation we need, now we can write it to the file

    with open("settings.json.new", "w", encoding="utf-8") as settingsFile:
        json.dump(info, settingsFile, indent=4)
