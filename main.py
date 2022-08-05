#!/usr/bin/env python3
import os
import sys
import dotenv
import glob
import shutil

import requests

from trello import TrelloClient as t

dotenv.load_dotenv()
api_key = os.getenv("API_KEY")                                                     
api_secret = os.getenv("API_SECRET")
token = os.getenv("TOKEN")

def main(listname, years=[2018,2019,2020]):
    a = t(api_key=api_key, api_secret=api_secret, token=token)

    historical = [x for x in a.list_boards() if x.name == "Historical"]

    if not historical:
        return "Historical board not found"

    for year in years:
        print("Starting", year)
        move_list = [x for x in historical[0].list_lists() if x.name == "{} - {}".format(listname, year)]
        if not move_list:
            print("No list year", year, "found for", listname)
            continue
        else:
            print("Move list id", move_list[0].id)
            cards = [x for x in historical[0].list_lists() if x.name == listname]
            if not cards:
                break
            print("Cards List is:", cards[0])
            old_cards = [x for x in cards[0].list_cards() if x.due_date.year == year]
            print("We have", len(old_cards), "old cards")

            for old_card in old_cards:
                old_card.change_list(move_list[0].id)

            print("Done with ", year, "for", listname)

def download():
    """Downloads all attachments"""
    a = t(api_key=api_key, api_secret=api_secret, token=token)
    
    board_name = "Chester Priority"
    list_name = "Fadal photos"
    
    # Get the board
    priority = [x for x in a.list_boards() if x.name == board_name][0]
    print("Priority: ", priority)
    
    # Get the lists
    fadal_photos = [x for x in priority.list_lists() if x.name == list_name][0]
    print("Lists:", fadal_photos)
    
    
    # Get all cards that have a directory named here
    files = [x.replace("\\", "") for x in glob.glob("*/") if "venv" not in x]
    print("File:", files)
    
    cards = [x for x in fadal_photos.list_cards()]
    print("Cards:", cards)
    
    headers = {
        "Authorization" : "OAuth oauth_consumer_key=\"{}\", oauth_token=\"{}\"".format(api_key, token)
    }
    # Download all attachments to the directories
    for file in files:
        found = [x for x in cards if x.name == file]
        if found:
            print("Found a matching card:", file)
            found = found[0]
            
            for (idx, attachment) in enumerate(found.get_attachments()):
                with requests.get(attachment.url, headers=headers, stream=True) as r:
                    with open(os.path.join(file, "{}.jpg".format(idx)), "wb") as f:
                        shutil.copyfileobj(r.raw, f)
                        print("Wrote out to {}.jpg".format(idx))
                
            

def create_cards():
    """Creating cards with checklists for attachments"""
    
    static = [
        "Check All Photos",
        "Upload Videos to Youtube",
        "------------",
    ]
    
    a = t(api_key=api_key, api_secret=api_secret, token=token)

    board_name = "Chester Priority"
    list_name = "IP Checks"

    # Get the board
    priority = [x for x in a.list_boards() if x.name == board_name][0]
    print("Priority: ", priority)

    # Get the lists
    fadal_photos = [x for x in priority.list_lists() if x.name == list_name][0]
    print("Lists:", fadal_photos)
    
    # Get a list of all folders from top directory
    with open("../Auctions.txt") as f:
        raw = f.readlines()
    
    cards = [x.split("\t")[1].strip() + " " + x.split("\t")[0].strip() for x in raw]
    for card_name in cards:
        print("Creating {}".format(card_name))
        card = fadal_photos.add_card(card_name)
        card.add_checklist("TODO", static + os.listdir("../{}".format(card_name)))
    
if __name__ == "__main__":
    create_cards()
    # download()
    """
    if len(sys.argv) > 1:
        main(sys.argv[1])
    """
    
