import redis

class TopkEntryLogger:

    def __init__(self, topk_key_name, topk_size, redis):
      self.topk_key_name = topk_key_name
      self.redis = redis
      self.topk_size = topk_size
      self.topk = redis.topk()
    
    def create_topk_key(self):
        try:
            self.topk.reserve(self.topk_key_name, self.topk_size, 2000, 7, 0.925)
        except Exception as exc:
                print('The topK key may already exist ... continuing on...')            

    def addEntryToMyTopKKey(self,entry_value):
        print(f'adding event_value to TopKKey: {entry_value}')
        self.topk.add(self.topk_key_name, entry_value)
    
    def listTopK(self):
        topResults = self.topk.list(self.topk_key_name)
        return topResults 
