# myredisclient/myredisclient/redis_client.py
import redis

class CacheClusterClient:
    def __init__(self, host='localhost', port=6379, password=None, db=0):
        self.host = host
        self.port = port
        self.password = password
        self.db = db

        # 创建 Redis 连接
        self.client = redis.StrictRedis(host=self.host, port=self.port, password=self.password, db=self.db)

    def set(self, key, value):
        try:
            return self.client.set(key, value)
        except redis.exceptions.RedisError as e:
            print(f'Error setting key {key}: {e}')
            return None

    def get(self, key):
        try:
            return self.client.get(key)
        except redis.exceptions.RedisError as e:
            print(f'Error getting key {key}: {e}')
            return None

    def incr(self, key):
        try:
            return self.client.incr(key)
        except redis.exceptions.RedisError as e:
            print(f'Error incrementing key {key}: {e}')
            return None

    def keys(self, pattern='*'):
        try:
            return self.client.keys(pattern)
        except redis.exceptions.RedisError as e:
            print(f'Error getting keys with pattern {pattern}: {e}')
            return []

# 创建 Redis 客户端实例
cache_cluster_client = CacheClusterClient(host='192.168.0.164', port=26379, password='imslave', db=0)
