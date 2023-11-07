from redisvl.index import SearchIndex
from redisvl.query import VectorQuery
from sentence_transformers import SentenceTransformer

import os

# Some suggested VSS queries:
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

# set redis address
"""
username = "default"
host = "<enter your redis host here>"
port = "<enter your redis port here>"
password = "<enter your redis password here>"
"""
# if you export your redis URL to the system you can execute:
# rvl stats -i idx_cairn
# and 
# rvl index info -i idx_cairn
# export REDIS_URL="redis://default:wFUzhoROOECMPsX7Cy3bk+xhfu0AzAMwSjbcSRQT6SA=@E5VSS.centralus.redisenterprise.cache.azure.net:10000"

username = "default"
host = "E5VSS.centralus.redisenterprise.cache.azure.net"
port = "10000"
password = "wFUzhoROOECMPsX7Cy3bk+xhfu0AzAMwSjbcSRQT6SA="

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
        print(f'\n{next_result.get("content")}')


