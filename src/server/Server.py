import os
import grpc
import proto.peering_pb2_grpc as peering_pb2_grpc, proto.peering_pb2 as peering_pb2
from concurrent import futures
from utils import get_random_zone_key
from dotenv import load_dotenv, find_dotenv

class Server(peering_pb2_grpc.PeeringServiceServicer):

    # implementar load_dotenv y find_dotenv como en peer
    def __init__(self, ip, port, network_size, number_of_zones) -> None:
        self.ip = ip
        self.port = port
        self.network_size = network_size
        self.registered_peers = 0
        self.number_of_zones = number_of_zones
        self.zone_size = network_size // number_of_zones
        self.network_zones_directory = {}
        for i in range(1, number_of_zones+1):
            zone_end = i * self.zone_size
            self.network_zones_directory[zone_end] = {}
            self.network_zones_directory[zone_end]['id'] = []
            self.network_zones_directory[zone_end]['ip_port'] = []

    def __repr__(self) -> str:
        return f"""ip={self.ip}\nport={self.port}\nnetwork_size={self.network_size}\nnumber_of_zones={self.number_of_zones}\nzone_size={self.zone_size}\nnetwork_zones_directory={self.network_zones_directory})"""

    def server_listener(self):
        server_listener = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        peering_pb2_grpc.add_PeeringServiceServicer_to_server(self, server_listener)
       
        server_listener.add(self.ip_port)
        server_listener.start()
       
        server_listener.wait_for_termination()

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
            peer_id_index = self.network_zones_directory[request.zoneKey]['id'].index(request.peerId)
            self.network_zones_directory[request.zoneKey]['id'].pop(peer_id_index)
            self.network_zones_directory[request.zoneKey]['ip_port'].pop(peer_id_index)
            return peering_pb2.UnregisterResponse(status = 'success', message = f'The peer {request.peerId} was registered on zone {request.zoneKey}.')
        except:
            return peering_pb2.UnregisterResponse(status = 'failed', message = f'The peer {request.peerId} was not unregistered from zone {request.zoneKey}.')

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