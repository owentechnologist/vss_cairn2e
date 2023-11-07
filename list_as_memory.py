import redis

class ListAsMemory:

    def __init__(self, list_key_name, redis):
      self.list_key_name = list_key_name
      self.redis = redis

    # we guarantee that no more than 50 entries will exist in any one list:  
    def addEntryToMyListMemory(self,entry_value):
        print(f'adding event_value to list in redis: {entry_value}')
        self.redis.lpush(self.list_key_name, entry_value)
        self.redis.ltrim(self.list_key_name,0,49)

    # we deduct 1 from the how_many provided so that if 10 are requested
    # 10 are returned (if they exist)
    def getMemories(self,how_many):
        print(f'fetching {how_many} memories from list in redis: ')
        memories = self.redis.lrange(self.list_key_name,0,(how_many-1))
        return memories

    # we assume no more than 50 entries will exist in any one list:
    def getOldMemories(self,how_many):
        starting_point = (how_many)*-1
        print(f'fetching {how_many} old memories from list in redis: ')
        memories = self.redis.lrange(self.list_key_name,starting_point,50)
        return memories
        
