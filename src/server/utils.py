import random

def get_random_zone_key(number_of_zones, zone_size):
    return random.randint(1, number_of_zones) * zone_size

def get_number_of_zones(network_size):
    print("\nSince you didn't provide a value for NUMBER_OF_ZONES, we assigned one.\n")
    
    network_size = int(network_size)
    nodes_per_zone = 6
    while (network_size % nodes_per_zone) != 0: 
        nodes_per_zone += 1
    number_of_zones = network_size // nodes_per_zone
    
    return number_of_zones