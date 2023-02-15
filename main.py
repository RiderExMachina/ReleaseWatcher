from bs4 import BeautifulSoup as soup
import requests, time, argparse, logging, json

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--debug', help="Debug mode: will not post to Twitter or Mastodon", default=False, action='store_true')
parser.add_argument('-a', '--add-project', help="Add project to watchlist", default=False, action='store_true')
args = parser.parse_args()

version = "0.0.1"
if __name__=="__main__":
    if not os.isfile("settings.json"):
        import setup
        setup()
    elif args.add_project:
        import add_projects
        add_project()
    else:
        print(f"Running script version {version}")


