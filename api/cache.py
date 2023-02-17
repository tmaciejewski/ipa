import time
import datetime

class Cache:
    class Item:
        def __init__(self, value):
            self.value = value
            self.time = time.time()

    def __init__(self, limit=100, duration=600):
        self.limit = limit
        self.duration = duration
        self.cache = {}

    def __setitem__(self, key, value):
        while (len(self.cache) >= self.limit):
            self.delete_oldest_item()
        self.cache[key] = self.Item(value)

    def __getitem__(self, key):
        item = self.cache[key]
        if (time.time() - item.time < self.duration):
            return self.cache[key].value
        else:
            self.cache.pop(key)
            self.cache[key]

    def delete_oldest_item(self):
        oldest = min(self.cache.items(), key = lambda item: item[1].time)[0]
        self.cache.pop(oldest)

if __name__ == "__main__":
    print('Tests')
    cache = Cache(limit=2, duration=1)
    cache['a'] = 1
    cache['b'] = 2
    assert cache['a'] == 1
    assert cache['b'] == 2
    cache['c'] = 3
    try:
        cache['a']
        assert False, 'excepted KeyError'
    except KeyError:
        pass
    assert cache['b'] == 2
    assert cache['c'] == 3
    time.sleep(1)
    try:
        cache['b']
        assert False, 'expected KeyError'
    except KeyError:
        pass
