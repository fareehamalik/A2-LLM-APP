#for testing wit tests.json
import json 
import os
import sys

#logic import from main.py (where game lives )

try:
    from main import check_safe, build_prompt, call_ollama, RULES, state_changes
except ImportError:
    print("EROOR: import main.py fail. Check file directory")
    sys.exit(1)

TEST_FILE = "tests.json"

def run_eval():
    #loading tests json 
    if not os.path.exists (TEST_FILE):
        print(f"ERROR: {TEST_FILE} not found")
        return
    
    with open(TEST_FILE, "r") as f:
        tests = json.load(f) #loading the json file tests.json

    #offline eval for terminal debug
    print(f"offline evaluation running ({len(tests)})") #15
    passed=0 #counter 

    for i, test in enumerate(tests):
        test_input = test["input"]
        expected = test["expected_behaviour"] #TODO: laterrecheck my spellings
        test_type = test["type"]

        print(f"Test {i+1} [{test_type}]: '{test_input}' , end=")  #:]")


#safety check 
      
        if test_type == "safety":
            safe, message = check_safe(test_input) #i think inconsistent message vs messages, check time permitting
            if not safe:
                print("PASS!")
                passed+=1
            safe, message = check_safe(test_input) #if fasle, then pass 

    
        else:
            print(f"Fail!! (Safety guard rails didnt catch)")
            continue

#some issue with logic
        if not safe:
            print("Fail")
            passed +=1 #counter for end report

    #mock testing so i can test in mid-game too 
        mock_state = RULES["START"].copy()
        mock_state ["inventory"] = ["pencil"] #random dummy item for inventory
        mock_state["flags"] ={}


        if test_type == "lock_check":
            mock_state["flags"]={}
        
        if test_type == "quest_trigger":
            pass #time dependent palceholder

        try: #ollama manual
            message = build_prompt(test_input, mock_state)
            response = call_ollama(message)

            response_str = json.dumps(response).lower() #looking thru rules.json stuff convo_w_prof, move etc

            if expected.lower() in response_str:
                print(f"PASS")
                passed+=1
            elif expected == "state_changes" and response.get("state_changes"):
                print(f"PASS")
                passed+=1

            else: 
                print(f"FAIL")
                print(f"Expected: {expected}")
                print(f" Received {response_str}")

        except Exception as e:
            print(f"ERROR: {e}")

        #report 
        score = (passed/len(tests)) * 100 #percent
        print(f"Final Score: {score}") #TODO: make sure percent

if __name__== "__main__":
    run_eval()


    '''
    REMOVED CODE
       #if not safe:
            #print("Pass")
            #passed +=1 #counter for end report


              #if test_type.startswith("safety"):
            ''' 