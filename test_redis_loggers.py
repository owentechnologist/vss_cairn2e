import redis
from timeseries_event_logger import *
from topk_entry_logger import *
from list_as_memory import *
from keys_and_such import *

import random

username = redis_username
host = redis_host
port = redis_port
password = redis_password

#REDIS_URL = f"redis://{username}:{password}@{host}:{port}"

creds_provider = redis.UsernamePasswordCredentialProvider(username, password)
redis_conn = redis.Redis(host=host, port=port, credential_provider=creds_provider,decode_responses=True)
redis_conn.ping()

topk_logger = TopkEntryLogger("topk:test",10,redis_conn)
topk_logger.create_topk_key()
topk_logger.addEntryToMyTopKKey(f"Subject {random.randint(1,10)}")
popularStuff = topk_logger.listTopK()
print("getting ranked results from topK_logger (top is most popular)")
for m in popularStuff:
    print(m)


ts_logger = TimeSeriesEventLogger("token_used_count","ts:test",redis_conn)
ts_logger.create_ts_key()
ts_logger.addEventToMyTSKey(random.randint(1,50))

memory_list = ListAsMemory("l:test",redis_conn)
memory_list.addEntryToMyListMemory(f"prompt: why make {random.randint(1,12)} donuts? response: because they are tasty")
recent_memories = memory_list.getMemories(3)
print("getting recent memories")
for m in recent_memories:
    print(m)

old_memories = memory_list.getOldMemories(2)
print("getting old memories")
for m in old_memories:
    print(m)

# now use redisInsight to look at the contents of these two test keys:
# topk:test and ts:test
#TS.MRANGE - + AGGREGATION avg 60000 FILTER custom_label=token_used_count
#TOPK.LIST topk:test withcount

