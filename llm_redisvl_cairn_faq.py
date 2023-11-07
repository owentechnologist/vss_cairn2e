from redisvl.index import SearchIndex
from redisvl.query import VectorQuery
import openai
from sentence_transformers import SentenceTransformer
from keys_and_such import *
import os

# for use with OPENAI LLM: 
openai.api_key = os.environ.get("apikey")
print(f'mykey is: {os.environ.get("apikey")}')

os.environ["TOKENIZERS_PARALLELISM"] = "False"

def ask_openai(question):
    response = openai.completions.create(
      model="text-davinci-002",
      prompt=question,
      max_tokens=200
    )
    return response.choices[0].text.strip()

# Some suggested LLM queries:
"""
What is the effect of a short rest in Cairn?

When should players role saving throws

What happens when a player takes critical damage

How can a Warden make the game fun?

How is advancement for players handled

How do players level up their characters

List the steps involved when rolling for an encounter

List the steps involved when creating a character
"""

# if you export your redis URL to the system you can execute:
# rvl stats -i idx_cairn
# and 
# rvl index info -i idx_cairn
# export REDIS_URL=f"redis://{username}:{password}@{host}:{port}"
username = redis_username
host = redis_host
port = redis_port
password = redis_password


REDIS_URL = f"redis://{username}:{password}@{host}:{port}"

os.environ["REDIS_URL"] = REDIS_URL

# create a vectorizer
# choose your model from the huggingface website
encoder = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

# initialize the index and connect to Redis
# construct a search index from the schema
index = SearchIndex.from_yaml('cairnrpg_vss_index.yaml')
#connect to Redis:
index.connect(REDIS_URL)

spacer = "\n**********************************************\n"

def display_menu():
    #display something to UI CMDLine:
    print(spacer)
    print('\tType: END   and hit enter to exit the program...\n')
    print('\tCommandline Instructions: \nType in your prompt/question as a single statement with no return characters... ')
    print('(only hit enter for the purpose of submitting your question)')
    print(spacer)
    # get user input/prompt/question:
    user_text = input('\n\tWhat is your question? (prompt):\t')
    if user_text =="END" or user_text =="end":
        print('\nYOU ENTERED --> \"END\" <-- QUITTING PROGRAM!!')
        exit(0)
    return (user_text)

while True:
    user_q = display_menu();
    query = VectorQuery(
        vector=encoder.encode(user_q),
        #filter_expression='vector_distance',
        vector_field_name='embedding',
        return_fields=['content'],
        num_results=1,
        )
    results = index.query(query)
    print(f'\n Redis VSS ... Searching for: {user_q}...\nresult:')
    for next_result in results:
        ctx = next_result.get("content")
        prompt =f'Provide a 32 word answer to this question {user_q}   Be sure to use the following information: {ctx}'
        llm_response = ask_openai(prompt)
        print(f'\n{llm_response}')


