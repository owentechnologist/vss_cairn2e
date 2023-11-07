import redis

class TimeSeriesEventLogger:

    def __init__(self, custom_label, time_series_key_name, redis):
      self.custom_label = custom_label
      self.time_series_key_name = time_series_key_name
      self.redis = redis
      self.ts = redis.ts()
      self.shared_label = "VSS_and_LLM"
    
    def create_ts_key(self):
        try:
            self.ts.create(self.time_series_key_name, labels={"custom_label": self.custom_label, "shared_label": self.shared_label })
        except Exception as exc:
            print('The TimeSeries key may already exist  ... continuing on...')            

    def addEventToMyTSKey(self,event_value):
        print(f'adding event_value to TSKey: {event_value}')
        self.ts.add(self.time_series_key_name, "*", event_value)

