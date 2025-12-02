#importing 
import json 
import os
import ollama #incase, was working without but slow
import time 
from datetime import datetime


#MAX_PARAGRAPHS = 2 #document shows json and say to do this in python, recheck later

#adding for file saving issues specific to transcript.txt
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SAMPLE_DIR = os.path.join(BASE_DIR, "samples")

#if folder dont exit, add
os.makedirs(SAMPLE_DIR, exist_ok=True)

#file path def
SAVE_FILE = "save.json" #optional requirement
TRANSCRIPT_FILE = os.path.join(SAMPLE_DIR, "transcript.txt") 
#check for saving
print(f" saving transcitp to: {TRANSCRIPT_FILE}")

GM_PROMPT_FILE = "prompts/gm.txt"
RULES_FILE = "rules.json"
TELEMETRY_FILE = "telemetry.log"
MAX_INPUT_LENGTH = 1000 #safety chars

#loading rules from json file 
try: 
    with open(RULES_FILE) as f:
        RULES = json.load(f)

    #reading prompt 
    with open(GM_PROMPT_FILE) as f:
        GM_PROMPT=f.read()

except FileNotFoundError as e:
    print("f: ERROR: missing required rules fine:{e}")
    exit()

#state initializations
state = RULES["START"].copy() #avoids overriwting by ollama
state["turns"] =0 #turn counter
transcript = []

#telemtry helper function
def log_telemetry(data):
    try: 
        with open(TELEMETRY_FILE, "a") as f:
            f.write(json.dumps(data)+"\n")
    except Exception as e:
        print(f"Telemtry Error: could not write log: {e}")

#prompting model , changed to build_prompt
def build_prompt(player_input, state): #was commented not sure why, accdient

#RAG enhancement
    retrieved_syllabus = retrieved_context(player_input)

#if smth found ing rag
    rag_section =""
    if retrieved_syllabus:
        rag_section = {retrieved_syllabus}
        #print(f"successful RAG retrieval: {}")
        print(f"successful RAG retrieval: {retrieved_syllabus}\n") #terminal view



    rules_text = json.dumps(RULES, indent=2) #beter formatting
    state_text = json.dumps(state, indent=2)
 # return f"""{GM_PROMPT}
    system_content = f"""{GM_PROMPT} #TODO: later for full system with instruction and rules and state
  

RULES:
{rules_text}

CURRENT_STATE:
{state_text}

PLAYER_INPUT:
{player_input}
"""
    
    return[
        {"role": "system", "content": system_content},
        {"role": "user", "content": f"The player comman: {player_input}"} #better struct now
    ]

#ollama call
def call_ollama(prompt, model="qwen3:0.6b"): #recheck correct name

#telemtry data added 
    start_time = time.time()
    telemetry_data = {"model": model, "timestamp":datetime.now().isoformat(), "success": False, "pathway":"game_turn"}

    try:
        response= ollama.chat(
            model=model,
            messages=messages,
            format="json" #json output 
        )
        end_time = time.time()

        raw_content=response['message']['content']
        ollama_reply = json.loads(raw_content)

        telemetry_data.update({
            "success": True,
            "latency": (end_time-start_time)
            "tokens_in": response.get('prompt_eval_count', 'N/A'),
            "tokens_out": response.get('eval_count', 'N/A')
        })

        log_telemetry(telemetry_data)
        return{
            "narration": ollama_reply('narration', 'N/A'),
            "state_change": ollama_reply.get('state_change',[]),
            "raw_output": raw_content #transcript
        }
    

    except json.JSONEncoder as e:
        telemetry_data.update({"latency": (time.time()-start_time)})
        log_telemetry(telemetry_data)

    #not json, handle that output from ollama
    raw_output = response.get('message', {}).get('content', 'no output given by OLLAMA!')
    print(f"LLM ERROR, invalid JSON received. Raw output: {raw_output}")

    return{
        "narration: Game master failed to parse thoughts, try rephrasing.",
        "state_change:"[],
        "raw_output:" raw_output
    }

except Exception as e:
log_telemetry(telem)

   

 

#HELPER FUNCTIONS 
#state changes, looping (MVPs)
def state_changes(updates):
    for u in updates:
        act = u.get("action")
        if act == "add_flag":
            state["flags"][u["flag"]]=True
        elif act =="remove_flag":
            state["flags"].pop(u["flag"],None)
        elif act =="add_item":
            if len(state["inventory"])<RULES["INVENTORY_LIMIT"]:
                state["inventory"].append(u["item"])
            else:
                print("Inventory full, cant add item") #plceholder
        elif act =="move":
            dest = u["place"]
            lock=RULES.get("LOCKS", {})
            if dest in lock:  #and not all(flag in state["flags"] for flag in lock[dest]):
                required_flags = lock[dest]
                if not all (flag in state["flags"] for flag in required_flags):
                    print(f"cannot move to {dest}, missing required flags {required_flags}") #placeholder
                    continue
           #else:
            state["location"]=dest
        elif act=="hp_change":
            state["hp"]+=u["amount"]
            if state["hp"]<=0:
                state["flags"]["hp_zero"]=True
                print("hp is zero!")


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
        print("No saved game found.") #TODO: remove later for ollama to do





#End condition 
def end_condition_check():
    #WIN when all WIN_ALL_FLAGS true and/or after a win narration.
    if all(state["flags"].get(f) for f in RULES["END_CONDITIONS"].get("WIN_ALL_FLAGS", [])):
        return "win" #TODO: make sure LLM not suppoesd to
    
     #LOSE when any LOSE_ANY_FLAGS true or turns exceed MAX_TURNS.
    if any(state["flags"].get(f) for f in RULES["END_CONDITIONS"].get("LOSE_ANY_FLAGS", [])):
        return "lose"
    if state["turns"]>= RULES["END_CONDITIONS"].get("MAX_TURNS", 100): #TODO: implent max turns
        return "lose"
    return None 

#TODO: handling of commands RECHECK IF THIS SHOULD ONLY BE IN JSON
while True: #need looping to use continue
    player_input = input("\n ").strip().lower()#handling user input
    
    #if player_input not in RULES["COMMANDS"]:
       # print("Illegal command, try one of ", ",".join(RULES["COMMANDS"]))
    if player_input == "inventory":
        print("Inventory:", state["inventory"])
        continue
    elif player_input == "save":
        save_game()
        continue
    elif player_input =="load":
        load_game()
        continue
    elif player_input =="help":
        print("Commands:", ",".join(RULES["COMMANDS"]))
        continue
    elif player_input =="quit":
        print("Game quit!") #TODO: figure out way for OLLAMAto do
        break

    #LLM 
    prompt = build_prompt(player_input, state)
    gm_output=call_ollama(prompt)

#story narration, placeholder  test
    narration = gm_output.get("text", "...")
    print(f"\n{narration}\n")

    #state changes and recording, gm=game master
    state_changes(gm_output.get("state_change", [])) #bracket issue
    transcript.append({"player": player_input, "gm": gm_output})
    state["turns"]+=1

    #end condition check 
    end_status=end_condition_check()
    if end_status:
        if end_status == "win":
         print("\n you win")
        #print({end_status})
        else: 
         print("\n game over")
        break

#TODO: check Transcript saving in correct struct 
with open(TRANSCRIPT_FILE, "w") as f:
    json.dump(transcript, f, indent=2)
   


#REFERENCES
#https://www.geeksforgeeks.org/python/json-load-in-python/
#https://www.geeksforgeeks.org/python/reading-and-writing-json-to-a-file-in-python/
#https://collabnix.com/using-ollama-with-python-step-by-step-guide/
#https://docs.python.org/3/library/functions.html#repr

#TODO: quitting game

#TODO: state changes

#TODO: error if something not listed in rules.json 
#TODO: end result (after testing with ollama)

#TODO: add checks for directory checks, in case file missing

#TODO: other commands by player, handling





#-------------------------OLD/UNUSED CODE----------------------
'''
REMOVED NOW I HAVE OLLAMA
 result = subprocess.run(
        ["ollama", "run", model],
        input=prompt.encode("utf-8"),
        capture_output=True,
        #timeout=30 #so i dont have to do ctrl c to interrupt process
        timeout=120 #prompt too large, testing with new time
    )
       output = result.stdout.decode("utf-8").strip()
    print(output) #cant see parsed json, but trying to see on terminal
    return {"state_change": [], "text": output} #non parsed no json



    #error handling fix
    try:
        if not output:
            return{"state_change": [], "text": "No response ollama"}
        return json.loads(output)
    except json.JSONDecodeError:
        #print("JSOn decode error")
        return {"state_change": [], "text": "Invalid JSON"} #output if output else "Invalid Response"}
    except subprocess.TimeoutExpired:
        return {"state_change": [], "text": "time OUT!"}
    except Exception as e:
        print(f"error calling ollama:{e}")
        return {"state_change": [], "text": "error"}
'''
   # print("ollama debut:", repr(output)) #check raw output, whats breaking
'''
  #  if not output:
       # return{"state_change:": [], "text": "No response ollama"}
    try: #json parking, avoiding error issues
        return json.loads(output)
    except json.JSONDecodeError: #as e:
        print("JSOn decode error")
     #   response = {"state_change"}
        return{"state_change:": [], "text": "No response ollama"}
    
'''
    #need to inclue some dubugging here
 

 

#game state , tracking
'''
state={
    "location":"home",
    "inventory": [], 
    "flags":{}, 
    "hp":100, #health 
    "turns":0 #
}
 #
'''
#import subprocess removing coz i imported ollama