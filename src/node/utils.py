import hashlib
import random

def hash_message_zone_key(message: str, number_of_zones: int) -> int:
    hash_object = hashlib.sha256(message.encode())
    hash_value = int(hash_object.hexdigest(), 16)
    zone_key = hash_value % number_of_zones

    return zone_key

def get_random_node_index(node_ids):
    return random.randint(1, len(node_ids))
