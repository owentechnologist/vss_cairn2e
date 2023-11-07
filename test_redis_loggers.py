import redis
from timeseries_event_logger import *
from topk_entry_logger import *

username = "default"
host = "E5VSS.centralus.redisenterprise.cache.azure.net"
port = 10000
password = "wFUzhoROOECMPsX7Cy3bk+xhfu0AzAMwSjbcSRQT6SA="

#REDIS_URL = f"redis://{username}:{password}@{host}:{port}"

creds_provider = redis.UsernamePasswordCredentialProvider(username, password)
redis_conn = redis.Redis(host=host, port=port, credential_provider=creds_provider)
redis_conn.ping()

topk_logger = TopkEntryLogger("topk:test",10,redis_conn)
topk_logger.create_topk_key()
topk_logger.addaddEntryToMyTopKKey("Subject 1")

ts_logger = TimeSeriesEventLogger("token_used_count","ts:test",redis_conn)
ts_logger.create_ts_key()
ts_logger.addEventToMyTSKey(22)

# now use redisInsight to look at the contents of these two test keys:
# topk:test and ts:test
#TS.MRANGE - + AGGREGATION avg 60000 FILTER custom_label=token_used_count
#TOPK.LIST topk:test withcount
