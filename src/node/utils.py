import random

def get_random_zone_key(number_of_zones, zone_size):
    return random.randint(1, number_of_zones) * zone_size