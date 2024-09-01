import sys
import os
proto_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'proto'))
sys.path.append(proto_path)
import peering_pb2, peering_pb2_grpc

import grpc
from concurrent import futures
from utils import get_random_zone_key, get_number_of_zones
from dotenv import load_dotenv, find_dotenv

class Server(peering_pb2_grpc.PeeringServiceServicer):

    def __init__(self) -> None:
        load_dotenv(find_dotenv())
        self.ip_port = f'{os.environ.get('IP')}:{os.environ.get('PORT')}'
        self.network_size = int(os.environ.get('NETWORK_SIZE'))

        try:
            self.number_of_zones = int(os.environ.get('NUMBER_OF_ZONES'))
        except:
            self.number_of_zones = get_number_of_zones(self.network_size)
        self.zone_size = self.network_size // self.number_of_zones
        
        self.registered_peers = 0
        self.network_zones_directory = {}
        for i in range(1, self.number_of_zones+1):
            zone_end = i * self.zone_size
            self.network_zones_directory[zone_end] = {}
            self.network_zones_directory[zone_end]['id'] = []
            self.network_zones_directory[zone_end]['ip_port'] = []

    def __repr__(self) -> str:
        return f'IP Port: {self.ip_port}\nNetwork size={self.network_size}\nnumber_of_zones={self.number_of_zones}\nzone_size={self.zone_size}\nnetwork_zones_directory={self.network_zones_directory})'

    def server_listener(self):
        server_listener = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        peering_pb2_grpc.add_PeeringServiceServicer_to_server(self, server_listener)
       
        server_listener.add_insecure_port(self.ip_port)
        server_listener.start()
       
        server_listener.wait_for_termination()

        print('\nServer is up.\n')

    # method overrided from peering_pb2_grpc
    def Register(self, request, context):
        if self.registered_peers == self.network_size:
            return peering_pb2.RegisterResponse(
                status = 'failed', message = f'The network is currently full.', 
                peerId = 0, zoneKey = 0, numberOfZones = 0, zoneSize = 0
            )

        available_zone_key = self.get_available_zone_key()
        if available_zone_key:
            peer_id = available_zone_key - self.zone_size
        else:
            search_peer_id = True
            while search_peer_id:
                available_zone_key = get_random_zone_key(self.number_of_zones, self.zone_size)
                ids = self.network_zones_directory[available_zone_key]['id']
                for i in range(available_zone_key - self.zone_size, available_zone_key):
                    if i not in ids:
                        peer_id = i
                        search_peer_id = False
                        break

        self.registered_peers += 1
        self.network_zones_directory[available_zone_key]['id'].append(peer_id)
        self.network_zones_directory[available_zone_key]['ip_port'].append(f'{request.ip}:{request.port}')
        return peering_pb2.RegisterResponse(
            status = 'success', message = f'The peer {peer_id} was registered on zone {available_zone_key}.', 
            peerId = peer_id, zoneKey = available_zone_key, numberOfZones = self.number_of_zones, zoneSize = self.zone_size
        )

    # method overrided from peering_pb2_grpc
    def Unregister(self, request, context):
        try:
            peer_id_index = self.network_zones_directory[request.zoneKey]['id'].index(request.id)
            self.network_zones_directory[request.zoneKey]['id'].pop(peer_id_index)
            self.network_zones_directory[request.zoneKey]['ip_port'].pop(peer_id_index)
            return peering_pb2.UnregisterResponse(status = 'success', message = f'The peer {request.id} was registered on zone {request.zoneKey}.')
        except:
            return peering_pb2.UnregisterResponse(status = 'failed', message = f'The peer {request.id} was not unregistered from zone {request.zoneKey}.')

    # method overrided from peering_pb2_grpc
    def PeersByZone(self, request, context):
        try:
            return peering_pb2.PeersByZoneResponse(
                status = 'success', message = f'Peers of the zone {request.zone}', 
                id = self.network_zones_directory[request.zone]['id'], ipPort = self.network_zones_directory[request.zone]['ip_port']
            )
        except:
            return peering_pb2.PeersByZoneResponse(
                status = 'success', message = f'Peers of the zone {request.zone}', 
                id = [], ipPort = []
            )

    def get_available_zone_key(self) -> int:
        for key, peers in self.network_zones_directory.items():
            if not peers['id']: return key
        return 0