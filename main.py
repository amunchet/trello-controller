#!/usr/bin/env python3
import os
import sys
import dotenv
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

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])