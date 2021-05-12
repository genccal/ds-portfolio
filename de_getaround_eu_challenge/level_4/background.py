import json
import slow_computation
import redis


def background_task(data):
    r = redis.Redis("localhost", port=6379)
    vehicle = dict()
    for part in data["log"].split():
        key, value = part.split("=")
        vehicle[key] = value
    vehicle = slow_computation.compute(vehicle)
    r.rpush(11, json.dumps(vehicle))
