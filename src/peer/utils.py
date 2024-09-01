import hashlib
import random

def file_address(file, number_of_zones, zone_size):
    hash_file = hashlib.sha256(file.encode())
    hash_value = int(hash_file.hexdigest(), 16)

    node_id = hash_value % (number_of_zones * zone_size)
    zone_key = ((node_id // zone_size) + 1) * zone_size

    return node_id, zone_key

def get_random_node_ip(node_ips):
    return random.choice(node_ips)
