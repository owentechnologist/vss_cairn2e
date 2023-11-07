import openai, redis
from sentence_transformers import SentenceTransformer
import os
from list_as_memory import *
from timeseries_event_logger import *
from keys_and_such import *

# for use with OPENAI LLM: 
openai.api_key = os.environ.get("apikey")

username = redis_username
host = redis_host
port = redis_port
password = redis_password

creds_provider = redis.UsernamePasswordCredentialProvider(username, password)
redis_conn = redis.Redis(host=host, port=port, credential_provider=creds_provider,decode_responses=True)
redis_conn.ping()

print("please provide your initials and birth month now: \n")
unique_session_key=input().replace(" ","")

#setup List key in Redis to capture chat history:
chat_memory = ListAsMemory(unique_session_key,redis_conn)
token_logger = TimeSeriesEventLogger( custom_label="token_used_count", time_series_key_name="ts:chat_with_memory",redis=redis_conn)
token_logger.create_ts_key()
## doing this using redisInsight is informative:
# TS.MRANGE - + AGGREGATION avg 60000 FILTER custom_label=token_used_count

"""
# alternate method of building unique key:
# get the time from redis to ensure multiple users don't use same key 
redis_time = redis_conn.time()
unique_session_key=(f"{redis_time}").replace(" ","")
print(f"session seed looks like: {unique_session_key_seed}")
"""

our_history = chat_memory.getMemories(3)

def chat(question,our_history):
    flattened_history = ""
    for m in our_history:
        flattened_history = f"{flattened_history}  {m}"
    flattened_history = f"Use the following as Context for your reply: {flattened_history}"
    print(f"{spacer}using {flattened_history} for context...")
    chat_prompt=f"You are a friendly chat bot. A user is prompting you with: {question} {flattened_history}"
    token_logger.addEventToMyTSKey(len(chat_prompt)/4)
    response = openai.completions.create(
      model="text-davinci-002",
      prompt=chat_prompt,
      max_tokens=200
    )
    return response.choices[0].text.strip()

spacer = "\n**********************************************\n"

def display_menu():
    #display something to UI CMDLine:
    print(spacer)
    print('\tType: END   and hit enter to exit the program...\n')
    print('\tCommandline Instructions: \nType in your prompt/question as a single statement with no return characters... ')
    print('(only hit enter for the purpose of submitting your question/comment)')
    print(spacer)
    # get user input/prompt/question:
    user_text = input('\n\tWhat is your input? (prompt):\t')
    if user_text =="END" or user_text =="end":
        print('\nYOU ENTERED --> \"END\" <-- QUITTING PROGRAM!!')
        exit(0)
    return (user_text)

while True:
    user_q = display_menu();
    response = chat(user_q,chat_memory.getMemories(5))
    chat_memory.addEntryToMyListMemory(f"{user_q}")
    print(f'\n{response}')
    #print(f'\n{response.get("content")}')

