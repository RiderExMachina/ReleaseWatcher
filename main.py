import os, json
import requests
from mastodon import Mastodon

def relay(msg):
    print(msg)
authFile = "auth.cred"
relay("\t - Looking for Mastodon information...")
if os.path.isfile(authFile):
    with open(authFile, "r") as Auth:
        mast_info = json.load(Auth)["mastodon"]
        relay("\tFound.")
        for info in mast_info:
            MAST_CONSUMER_KEY = info["mast_api_key"]
            MAST_CONSUMER_SECRET = info["mast_api_secret"]
            MAST_ACCESS_KEY = info["mast_access_key"]
    relay("Mastodon information loaded successfully.")
mastodonURL = "botsin.space"
mastodon = Mastodon(client_id=MAST_CONSUMER_KEY, client_secret=MAST_CONSUMER_SECRET, access_token=MAST_ACCESS_KEY, api_base_url=mastodonURL)
# End Mastodon remove

def post(name, release, link, tags="#foss #OpenSource"):
    message = f"{name} has updated to {release}!\nCheckout the update here: {link}\n{tags}"
    relay(message)
    mastodon.status_post(message)

def get_github_info(url):
    page = requests.get(url, timeout=120)
    information = page.json()

    latest = information[0]
    directURL = latest['html_url']
    release = latest['tag_name']

    return directURL, release

with open("settings.json", "r", encoding="utf-8") as settingsFile:
    info = json.load(settingsFile)

updated = False
for item in info["projects"]:
    project = info["projects"][item]
    name = project["name"]
    gh_link = project["url"]
    api_link = project["api-url"]
    cached_release = project["latest-release"]
    tags = project["tags"]

    update_link, updated_release = get_github_info(api_link)

    if cached_release != updated_release:
        post(name, updated_release, update_link, tags)
        info["projects"][item]["url"] = update_link
        info["projects"][item]["latest-release"] = updated_release
        updated = True
if updated:
    with open("settings.json.new", "w", encoding="utf-8") as settingsFile:
        json.dump(info, settingsFile, indent=4)
    os.rename("settings.json.new", "settings.json")
if not updated:
    print("No updates found!")
