import os
from dotenv import load_dotenv, find_dotenv
from Server import Server
from utils import get_number_of_zones

def main():
    load_dotenv(find_dotenv())

    IP = os.environ.get('IP')
    PORT = os.environ.get('PORT')
    NETWORK_SIZE = int(os.environ.get('NETWORK_SIZE'))
    try:
        NUMBER_OF_ZONES = int(os.environ.get('NUMBER_OF_ZONES'))
    except:
        print("Since you didn't provide a value for NUMBER_OF_ZONES, we assigned one.\n")
        NUMBER_OF_ZONES = get_number_of_zones(NETWORK_SIZE)

    server = Server(IP, PORT, NETWORK_SIZE, NUMBER_OF_ZONES)
    
    for i in range(100): 
        print(server.register_node('127.0.0.1', f'400{i}'))
    print(server.get_available_nodes_by_zone(8))
    print(server.unregister_node(8, 6))
    print(server.get_available_nodes_by_zone(8))

if __name__ ==  '__main__':
    main()