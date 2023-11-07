# vss_cairn2e
Using Redis as a Vector Similarity Search database to provide an FAQ solution for cairn2e 

useful links to python docs for redis and search:
https://redis-py.readthedocs.io/en/stable/index.html
https://redis.readthedocs.io/en/stable/redismodules.html 

useful links for redisvl:
https://github.com/RedisVentures/redisvl/tree/main 
https://github.com/RedisVentures/redisvl 

SETUP:

For Vector Similarity Search, you need a connection to Redis running Search 2.6 or higher.

You can create a free Redis Enterprise instance for this purpose by going to https://redis.com/try-free/   (Just be sure to select Redis Stack as the type of database you create) 

## Python-preparation Steps for running the samples on your dev machine:


1. Create a virtual environment:

```
python3 -m venv redisvss
```

2. Activate it:  [This step is repeated anytime you want this venv back]

```
source redisvss/bin/activate
```

On windows you would do:

```
venv\Scripts\activate
```

3. Python will utilize this requirements.txt in the project:

```
redis>=5.0.1
redisvl>=0.0.4
etc ...
```

4. Install the libraries: 
[only necesary to do this one time per environment --> unless you add libraries to the requirements.txt file]

```
pip3 install -r requirements.txt
```

5. when you are done exploring this set of examples you can deactivate the virtual environment:

```
deactivate
```

* Note that the file: keys_and_such.py contains connectivity information for Redis - the other scripts import these values - so you only have to edit in one place.

### to run the cairn data loader program the first time execute:

``` 
python3 redisloader_redisvl_cairn_txtfiles.py --indexoverwrite
```

### If you only want to test the VSS query, you can run the cairn_query.py script instead: 

``` 
python3 redisvl_cairn_vss_query.py
```

### to use the results of a VSS query as context for an LLM generated response look at:
```
python3 llm_redisvl_cairn_faq.py
```

### to observe the behavior of using Redis to store memories, TOPK (popular stuff), and event measures like duration and or number of tokens used look at:
``` 
python3 test_redis_loggers.py
```

### to work on a beginner chatbot with memory stored in Redis see:
```
python3 chat_with_memory.py
```
