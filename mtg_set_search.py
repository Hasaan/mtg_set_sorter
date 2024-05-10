import json
import sys
import os
import argparse

import re

import multiprocessing as mp
import time

import requests


def main(argv=None):
    print("Starting")
    CLI = argparse.ArgumentParser()
    
    #CLI.add_argument("--input_json", type=str, help = "Input File")
    CLI.add_argument("--decklist", type=str, help = "Input File")
    CLI.add_argument("--output", type=str, help = "path to dump files")
    
    args = CLI.parse_args()
    
    # if(args.input_json):
        # input_json = os.path.abspath(args.input_json)
        # print("Input is: ", input_json)
    # else:
        # print("No input given")
        # exit(1)    
        
    if(args.decklist):
        decklist = os.path.abspath(args.decklist)
        print("Decklist is: ", decklist)
    else:
        print("Decklist not provided")
        exit()
        
    if(args.output):
        output = os.path.abspath(args.output)
    else:
        output = os.getcwd()
        

    #read decklist from txt
    print("Reading Decklist\n")
    card_pat = re.compile(r'\d+\s+(.*)')
    compiled_decklist = []
    with open(decklist, "r") as file:
        for line in file:
        
            search = card_pat.search(line) 
            if search:
                search_result = search.group(1)
                print(search_result)
                compiled_decklist.append(search_result)
                
            elif "Mainboard" in line:
                continue
            else:
                break
    
    cards_done = 0            
    compiled_list = {}
    print("\nRunning Comparisons")
    for card in compiled_decklist:
        print(str(round((cards_done/ len(compiled_decklist))*100)) + "% Comparing for: " + card)
        cards_done += 1
        card_data = call_scryfall(card)
        
        #need delay between queries as per Scryfall API guidelines
        time.sleep(0.1)
        
        for entry in card_data:
            
            if entry["digital"]:
                continue
            
            set_name = entry["set_name"]
            rarity = entry["rarity"]
            
            if set_name not in compiled_list:
                compiled_list[set_name] = {}
                
                compiled_list[set_name][rarity] = []
                compiled_list[set_name][rarity].append(card)
                
                compiled_list[set_name]["Counts"] = {}
                compiled_list[set_name]["Counts"][rarity] = 1
            else:
                if rarity not in compiled_list[set_name]:
                    compiled_list[set_name][rarity] = []
                    compiled_list[set_name][rarity].append(card)
                    
                    
                    try:
                        compiled_list[set_name]["Counts"][rarity] += 1
                    except:
                        compiled_list[set_name]["Counts"][rarity] = 1  
                    
                elif card in compiled_list[set_name][rarity]:
                    continue
                else:
                    compiled_list[set_name][rarity].append(card)
                    
                    try:
                        compiled_list[set_name]["Counts"][rarity] += 1
                    except:
                        compiled_list[set_name]["Counts"][rarity] = 1                

    #counting up rarities
    set_total_match = {}
    for card_set in compiled_list:
        total_card = 0
        for rarity in compiled_list[card_set]["Counts"]:
            total_card += compiled_list[card_set]["Counts"][rarity]
        #print(total_card)
        set_total_match[card_set] = total_card

    #These aren't really sets...
    if 'Secret Lair Drop' in set_total_match:
        del set_total_match['Secret Lair Drop']

    #ordering set matches by most matches to least matches
    #printing only top 10
    ordered_match = dict(reversed(sorted(set_total_match.items(), key=lambda x:x[1])))
    if len(ordered_match.items()) > 10:
        ordered_match = dict(list(ordered_match.items())[0: 10])

        
    print("\n\n")
    #print out top 10 matches with stats
    for card_set in ordered_match:
        print(card_set + ": " + str(ordered_match[card_set]))
        
        rarity_str = "| "
        if "common" in compiled_list[card_set]["Counts"]:
            rarity_str += "common" + " " + str(compiled_list[card_set]["Counts"]["common"]) + " | "
        if "uncommon" in compiled_list[card_set]["Counts"]:
            rarity_str += "uncommon" + " " + str(compiled_list[card_set]["Counts"]["uncommon"]) + " | "
        if "rare" in compiled_list[card_set]["Counts"]:
            rarity_str += "rare" + " " + str(compiled_list[card_set]["Counts"]["rare"]) + " | "
        if "mythic" in compiled_list[card_set]["Counts"]:
            rarity_str += "mythic" + " " + str(compiled_list[card_set]["Counts"]["mythic"]) + " | "
        print(rarity_str)
        
        if "common" in compiled_list[card_set]:
            print("COMMONS:")
            temp_sorted_list = sorted(compiled_list[card_set]["common"])
            for card in temp_sorted_list:
                print(card) 
            print("\n")
        if "uncommon" in compiled_list[card_set]:
            print("UNCOMMONS:")
            temp_sorted_list = sorted(compiled_list[card_set]["uncommon"])
            for card in temp_sorted_list:
                print(card)    
            print("\n")
        if "rare" in compiled_list[card_set]:
            print("RARES:")
            temp_sorted_list = sorted(compiled_list[card_set]["rare"])
            for card in temp_sorted_list:
                print(card)     
            print("\n")
        if "mythic" in compiled_list[card_set]:
            print("MYTHICS:")
            temp_sorted_list = sorted(compiled_list[card_set]["mythic"])
            for card in temp_sorted_list:
                print(card)
            print("\n")
        
        print("-------------------------------------------")   

#query Scryfall for certain english card names
def call_scryfall(card):
    api_url = "https://api.scryfall.com/cards/search"
    query = {'q':card,'lang':'en', 'unique':'prints'}
    response = requests.get(api_url, params=query)
    
    # for data in response.json()["data"]:
        # if data["set_name"] == 'Magic Online Promos':
            # print(data)
            # exit()
    
    # print( response.json()["data"][0])
    # exit()
    
    return response.json()["data"]
      
def compare_db(database, card, dataList):
    print("Starting thread for ", card)
    results = {}
    
    for entry in database:
        
        if entry["name"] == card:
            #if entry["set_name"] == 'Seventh Edition' and entry["lang"] == "en":
            #    print(entry)
            if entry["set_name"] not in results:
                results[entry["set_name"]] = []
                
            results[entry["set_name"]].append((entry["name"], entry["rarity"]))
                
                  
    print("Ending thread for ", card)
    return dataList.append(results)
    
if __name__ == '__main__':
    main(sys.argv)
    