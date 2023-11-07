from redisvl.index import SearchIndex
from redisvl.query import VectorQuery
from sentence_transformers import SentenceTransformer

import os,sys

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

if len(sys.argv) > 1:
    if sys.argv[1]=='--indexoverwrite':
        # create the index in Redis (data previously indexed in redis will be deleted with overwrite=True)
        index.create(overwrite=True)

        # Create many embeddings at once (we want to load the data from the file-system)
        #file=open("myfile.txt","r")
        file_content = []
        embeddings = []
        file_list=os.listdir('./cairn2edocs')
        for name in file_list:
            try:
                with open(f'./cairn2edocs/{name}') as f:
                    content = f.read()
                    file_content.append(content)
                    thing = encoder.encode(content)
                    embeddings.append(thing.tobytes())

            except IOError as exc:
                raise            

        data = [{"content": t,
             "embedding": v}
            for t, v in zip(file_content, embeddings)]

        # load data into the index in Redis (list of dicts)
        index.load(data)

query = VectorQuery(
    vector=encoder.encode("when to have an NPC execute a save"),
    #filter_expression='vector_distance',
    vector_field_name='embedding',
    return_fields=['content'],
    num_results=1,
)
results = index.query(query)

print(f'\n Redis VSS ... Searching for: when to have an NPC execute a save...\nresult:')
for next_result in results:
    print(f'\n{next_result}')
