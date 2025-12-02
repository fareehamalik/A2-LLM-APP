Install Ollama + pull a model, create venv, run steps.
How rules.json works; how to add/change quest/locks/commands.
Example session (5-10 turns) showing: locked move refusal, inventory cap, setting the quest goal, and win/lose detection.

# Ollama AI - Game

## Installing OLLAMA
LLAMA was downloaded and installed via https://ollama.com/download/windows for windows. I also inputted the command "pip install ollama" to integrate ollama and python

## Pulling a model 
After the installation, I used my cmd terminal to pull the model. The model pulled was "qwen3:0:0.6b" and variations can be found on the official ollama site. 

The command used was ollama run qwen3:0:0.6b

## Creating a venv
No venv was created for this assignment. 

## Run Steps 
To run the game, cd in your terminal to the ai-game folder. Then input "python main.py" within terminal and hit enter. Input your command and hit enter again. Unfortunately, there is an issue with parsing of json, so the proper formatting of output does not work. 

## Game concept
### Below is the detailed game concept I had envisioned. Unfortunately, the learning curve and implementation was steep, and not everything could be implemented in a timely manner. However, I plan to complete this in my spare time.

I believe that the main issues lied in how I had formatted the rules.json. I was not able to translate my game idea to something understandable for a LLM. Furthermore, the fm.txt may have been too complex, as I was debugging issues I assumed more clarity would help from that file. Finally, the JSON parsing issues resulted in difficulty with saving and revieweing what the LLM was saying.

Rooms going through: 
The science building:
Going to lab 
Attendance with TA (SECOND CHARACTER)
Finishing lab and submitting 
Walking to the Tim Hortons in Shaw 
Waiting in line for some minutes 
Placing order on screen
Paying 
Picking order 
Going to Polonsky commons 
Sitting on the Muskoka chairs 
Drinking coffee 
Friend passes by 
Start talking to them (THIRD CHARACTER)
Calendar notification for class 
Going to last class in the Onion 
Walking to the Onion 
Saying hi to Professor (FOURTH CHAR)
Sitting next to classmate, saying hi 
Classmate says hi back (small talk) (FIFTH CHAR)
Points: For every interaction 
Purpose: Have as many interactions as possible (anti-social CS student)// Touch grass 
Inventory: for every interaction +1 point, longer interactions = +2 points 
Touch grass: +5 points 
End of game: Last class (onion)
Lose points: (none ig)

## Assets 
Please consult the assets folder to see the example of AI output by the ollama model.


## List of reference used
The following links were used to help with this assignment, understanding code and solving bugs. The skeleton for rules.json and gm.txt was obtained from the class sample within the assignment document. 

https://www.arsturn.com/blog/creating-next-gen-ai-npcs-with-local-llms-ollama

https://www.cohorte.co/blog/using-ollama-with-python-step-by-step-guide

#https://www.geeksforgeeks.org/python/json-load-in-python/

#https://www.geeksforgeeks.org/python/reading-and-writing-json-to-a-file-in-python/

#https://collabnix.com/using-ollama-with-python-step-by-step-guide/

#https://docs.python.org/3/library/functions.html#repr

#https://www.sitepoint.com/test-data-json-example/

#https://dev.to/sophyia/how-to-build-a-rag-solution-with-llama-index-chromadb-and-ollama-20lb

#https://huggingface.co/blog/ngxson/make-your-own-rag

#https://www.datacamp.com/tutorial/chromadb-tutorial-step-by-step-guide

#https://docs.python.org/3/tutorial/inputoutput.html

#https://stackoverflow.com/questions/70510297/how-to-strip-a-certain-piece-of-text-from-each-line-of-a-text-file

#https://stackoverflow.com/questions/19184335/is-there-a-need-for-rangelena

#https://docs.trychroma.com/docs/collections/add-data