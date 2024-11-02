import time,os,json
from abstract_utilities import *
from abstract_security import *
def getAbsFile():
  return os.path.abspath(__file__)
def getAbsDir():
  return os.path.dirname(getAbsFile())
def getAbsPath(path):
  return os.path.join(getAbsDir(),path)
def getSaveStatePath():
  return getAbsPath('rate_limiter_state.json')
def readSaveState():
  path= getSaveStatePath()
  if not os.path.isfile(path):
    state = {'last_method':None,'rate_limit': [],'last_mb': {},'cooldown_time': False,'last_url':None}
    safe_dump_to_file(file_path=path,data=state)
  return safe_read_from_json(getSaveStatePath())
def is_time_interval(time_obj, interval):
    print([time.time() - time_obj,interval-1])
    return (time.time() - time_obj) < interval-1

def get_mb(sum_list, limit, last_mb):
    return (sum_list + last_mb) > limit

def datasize(data):
    if isinstance(data, str):
        return len(data.encode('utf-8'))
    elif isinstance(data, (bytes, bytearray)):
        return len(data)
    elif isinstance(data, list) or isinstance(data, dict):
        return len(json.dumps(data).encode('utf-8'))
    else:
        return len(str(data).encode('utf-8'))

class RateLimiter(metaclass=SingletonMeta):
    def __init__(self,rpc_url = None,fallback_rpc_url=None,env_directory=None):
        if not hasattr(self, 'initialized'):  # Prevent reinitialization
          self.initialized = True
          self.rpc_url = rpc_url or get_env_value(key="solana_primary_rpc_url",path=env_directory) or "https://api.mainnet-beta.solana.com"
          self.fallback_rpc_url = fallback_rpc_url or get_env_value(key="solana_fallback_rpc_url",path=env_directory)
          self.initialized = True
          self.rate_limit = []
          self.last_mb = {}
          self.cooldown_time = False
          self.url1 = self.rpc_url
          self.url2 = self.fallback_rpc_url
          self.state_file = getSaveStatePath()
          self.last_url = None
          self.last_method=None
          self.load_state()
    def get_url_2(self):
        return self.url2

    def save_state(self):
        state = {
            'last_method':self.last_method,
            'rate_limit': self.rate_limit,
            'last_mb': self.last_mb,
            'cooldown_time': self.cooldown_time,
            'last_url': self.last_url
        }
        safe_dump_to_file(self.state_file, state)

    def load_state(self):
        state = readSaveState()
        self.last_method = state.get('last_method')
        self.rate_limit = state.get('rate_limit', [])
        self.last_mb = state.get('last_mb', {})
        self.last_url = state.get('last_url')
        self.cooldown_time = state.get('cooldown_time', False)

    def set_cooldown(self, add=False):
        if add:
            self.cooldown_time = time.time() + add
        if self.cooldown_time and (time.time() > self.cooldown_time):
            self.cooldown_time = False
        return bool(self.cooldown_time)

    def get_last_rate_limit(self):
        if self.rate_limit:
            return self.rate_limit[-1]
        return {}

    def is_all_limit(self, method):
        if method not in self.last_mb:
            self.last_mb[method] = 0

        if self.set_cooldown():
            return True

        self.rate_limit = [query for query in self.rate_limit if is_time_interval(query.get('time') or 0, 30)]
        last_rate_limit = self.get_last_rate_limit()

        # Check if data size exceeds limit
        if get_mb(sum(query.get('data', 0) for query in self.rate_limit), 100, self.last_mb[method]):
            return True

        # Check if the last request for the same method was within 10 seconds
        if self.last_method == method and is_time_interval(last_rate_limit.get('time') or 0, 10):
            return True

        # Check if more than 100 requests in the last 10 seconds
        time_rate = [query for query in self.rate_limit if is_time_interval(query.get('time') or 0, 10)]
        if len(time_rate) > 100:
            return True

        # Check if more than 40 requests for the same method in the last 10 seconds
        method_specific_time_rate = [query for query in time_rate if query['method'] == method]
        if len(method_specific_time_rate) > 40:
            return True

        return False

    def log_response(self, method=None, response_data=None):
        method = method or 'default_method'
        response_data = response_data or {}
        data_size = datasize(response_data)
        self.last_mb[method] = data_size

        if self.last_url == self.url1:
            self.rate_limit.append({'method': method, 'data': data_size, 'time': time.time()})

        self.rate_limit = [query for query in self.rate_limit if is_time_interval(query['time'], 30)]
        self.save_state()

    def get_url(self, method=None):
        method = method or 'default_method'
        if self.url2 and method == 'get_url_2':
            self.last_url = self.url2
            return self.url2
        
        if not self.is_all_limit(method):
            self.last_method = method
            
            self.last_url = self.url1
        elif self.url2:
            self.last_url = self.url2
        else:
          return {"rate_limited":"limit has been reached"}
        return self.last_url

