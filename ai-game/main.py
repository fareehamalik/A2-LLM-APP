#Simple Python Code

#importing 
import json 
import os

MAX_PARAGRAPHS = 2 #document shows json and say to do this in python, recheck later
SAVE_FILE = "save.json" #optional requirement
TRANSCRIPT_FILE = "transcript.json" #saving trasncript? need to reconfirm if doc means

#loading rules from json file 
with open("rules.json") as f:
    RULES = json.load(f)

#game state , tracking


state={
    "location":"home",
    "inventory": [], 
    "flags":{}, 
    "hp":100, #health 
    "turns":0 #
}

transcript = [] #

#helper functions 

#saving game 
def save_game():
    with open(SAVE_FILE, "w") as f:
        json.dump(state,f)
    print("Game saved!")

#loading game 
def load_game():
    global state #was outside
    if os.path.exists(SAVE_FILE): #check if no file
        with open(SAVE_FILE) as f:
            state = json.load(f)
        print("Game loaded!")
    else: 
        print("No saved game found.")


#TODO: quitting game

#TODO: state changes

#TODO: error if something not listed in rules.json 


#End condition 
def end_condition_check():
    #WIN when all WIN_ALL_FLAGS true and/or after a win narration.
    if all(state["flags"].get(f) for f in RULES.get("WIN_ALL_FLAGS", [])):
        return "win" #TODO: make sure LLM not suppoesd to
    
     #LOSE when any LOSE_ANY_FLAGS true or turns exceed MAX_TURNS.
    if any(state["flags"].get(f) for f in RULES.get("LOSE_ANY_FLAGS", [])):
        return "lose"
    if state["turns"]>= RULES.get("MAX_TURNS", 100): #TODO: implent max turns
        return "lose"
    return None 

   



#REFERENCES
#https://www.geeksforgeeks.org/python/json-load-in-python/
#https://www.geeksforgeeks.org/python/reading-and-writing-json-to-a-file-in-python/

#TODO: handling of commands RECHECK IF THIS SHOULD ONLY BE IN JSON

if player_input == "inventory":
    print_inventory()
    continue
elif player_input == "save":
    save_game()
    continue

elif player_input =="load":
    load_game()
    continue
elif player_input =="quit":
    continue

elif player_input =="help":
    continue


#TODO: check Transcript saving in correct struct 
with open(TRANSCRIPT_FILE, "w") as f:
    json.dump(transcript, f, indent=2)