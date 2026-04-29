import redis
import json

r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

cache_store = {}


def get_from_cache(query: str):
    return cache_store.get(query)


def save_to_cache(query: str, response: dict):
    cache_store[query] = response