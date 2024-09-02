import sys
import os
proto_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'proto'))
sys.path.append(proto_path)
import peering_pb2, peering_pb2_grpc
import grpc
from concurrent import futures
from dotenv import load_dotenv, find_dotenv
from utils import file_address, get_random_peer_ip, print_response

class Peer(peering_pb2_grpc.PeeringServiceServicer):
    def __init__(self):
        load_dotenv(find_dotenv())
        self.ip = os.environ.get('PEER_IP')
        self.port = os.environ.get('PEER_PORT')
        self.files = {
            'proper': [],
            'shared': [],
        }

        self.id = 0
        self.zone_key = 0
        self.number_of_zones = 0
        self.zone_size = 0

        self.server_channel = grpc.insecure_channel(f'{os.environ.get('SERVER_IP')}:{os.environ.get('SERVER_PORT')}')
        self.server_stub = peering_pb2_grpc.PeeringServiceStub(self.server_channel)

    def __repr__(self):
        return f'\nIP: {self.ip}\nPort: {self.port}\nProper files: {self.files['proper']}\nShared files: {self.files['shared']}\nId: {self.id}\nZone: {self.zone_key}'

    def peer_listener(self):
        try:
            peer_listener = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
            peering_pb2_grpc.add_PeeringServiceServicer_to_server(self, peer_listener)

            peer_listener.add_insecure_port(f'{self.ip}:{self.port}')
            peer_listener.start()
            peer_listener.wait_for_termination()
        except Exception as e:
            print(f"Error in peer_listener: {e}")

    def connect(self):
        try:
            connect_response = self.server_stub.Register(peering_pb2.RegisterRequest(ip = self.ip, port = str(self.port)))
            self.id = connect_response.peerId
            self.zone_key = connect_response.zoneKey
            self.zone_size = connect_response.zoneSize
            self.number_of_zones = connect_response.numberOfZones
            return {'status' : connect_response.status, 'message': connect_response.message}
        except:
            return {'status' : 'failed', 'message': 'Peer could not connect to the server.'}

    def disconnect(self):
        try:
            disconnect_response = self.server_stub.Unregister(peering_pb2.UnregisterRequest(zoneKey = self.zone_key, id = self.id))
            return {'status' : disconnect_response.status, 'message': disconnect_response.message}
        except Exception as e:
            print(f'Error in disconnect: {e}')
            return {'status' : 'failed', 'message': 'Peer could not disconnect to the server.'}

    def upload_file(self, file_name):
        try:
            file_peer_id, file_zone_key = file_address(file_name, self.number_of_zones, self.zone_size)
            peers_by_zone_response = self.server_stub.PeersByZone(peering_pb2.PeersByZoneRequest(zone = file_zone_key))
            while not peers_by_zone_response.id:
                file_zone_key -= 1
                peers_by_zone_response = self.server_stub.PeersByZone(peering_pb2.PeersByZoneRequest(zone = file_zone_key))

            if file_peer_id in peers_by_zone_response.id:
                peer_friend_ip = peers_by_zone_response.ipPort[peers_by_zone_response.id.index(file_peer_id)]
                proper_file = True
            else:
                peer_friend_ip = get_random_peer_ip(peers_by_zone_response.ipPort)
                proper_file = False

            peer_friend_channel = grpc.insecure_channel(peer_friend_ip)
            peer_friend_stub = peering_pb2_grpc.PeeringServiceStub(peer_friend_channel)

            recieve_file_response = peer_friend_stub.RecieveFile(peering_pb2.RecieveFileRequest(fileName = file_name, properFile = proper_file))
            return {'status': recieve_file_response.status, 'message': recieve_file_response.message}
        except Exception as e:
            return {'status': 'failed', 'message': f'Failed on upload_file: {e}'}

    # method overrided from peering_pb2_grpc
    def RecieveFile(self, request, context):
        try:
            if request.properFile:
                self.files['proper'].append(request.fileName)
            else:
                self.files['shared'].append(request.fileName)
            return peering_pb2.RecieveFileResponse(status = 'success', message = f'The file {request.fileName} was uploaded.')
        except Exception as e:
            return peering_pb2.RecieveFileResponse(status = 'failed', message = f'Failed on RecieveFile: {e}')

    def download_file(self, file_name):
        try:
            file_peer_id, file_zone_key = file_address(file_name, self.number_of_zones, self.zone_size)
            peers_by_zone_response = self.server_stub.PeersByZone(peering_pb2.PeersByZoneRequest(zone = file_zone_key))
            while not peers_by_zone_response.id:
                file_zone_key -= 1
                peers_by_zone_response = self.server_stub.PeersByZone(peering_pb2.PeersByZoneRequest(zone = file_zone_key))

            if file_peer_id in peers_by_zone_response.id:
                peer_friend_ip = peers_by_zone_response.ipPort[peers_by_zone_response.id.index(file_peer_id)]
                
                with grpc.insecure_channel(peer_friend_ip) as peer_friend_channel:
                    peer_friend_stub = peering_pb2_grpc.PeeringServiceStub(peer_friend_channel)

                    send_file_response = peer_friend_stub.SendFile(peering_pb2.SendFileRequest(fileName = file_name, properFile = True))
                    return {'status': send_file_response.status, 'message': send_file_response.message, 'file': send_file_response.file}
            else:
                peer_index = 0
                while peer_index < len(peers_by_zone_response.ipPort):
                    peer_friend_ip = peers_by_zone_response.ipPort[peer_index]
                    
                    with grpc.insecure_channel(peer_friend_ip) as peer_friend_channel:
                        peer_friend_stub = peering_pb2_grpc.PeeringServiceStub(peer_friend_channel)

                        send_file_response = peer_friend_stub.SendFile(peering_pb2.SendFileRequest(fileName = file_name, properFile = False))
                        if send_file_response.status == 'success':
                            return {'status': send_file_response.status, 'message': send_file_response.message, 'file': send_file_response.file}                        
                
                return {'status': 'failed', 'message': f'The file {file_name} was not found.', 'file': ''}
        except Exception:
            return {'status': 'failed', 'message': f'The file {file_name} was not downloaded.', 'file': ''}

    # method overrided from peering_pb2_grpc
    def SendFile(self, request, context):
        try:
            if request.properFile and request.file in self.files['proper']:
                return peering_pb2.SendFileResponse(status = 'success', message = f'The file {request.fileName} was downloaded.', file = request.fileName)
            elif not request.properFile and request.file in self.files['shared']:
                return peering_pb2.SendFileResponse(status = 'success', message = f'The file {request.fileName} was downloaded.', file = request.fileName)
            else:
                return peering_pb2.SendFileResponse(status = 'failed', message = f'The file {request.fileName} was not downloaded.', file = request.fileName)
        except:
            return peering_pb2.SendFileResponse(status = 'failed', message = f'The file {request.fileName} was not downloaded.', file = request.fileName)

    # falta implementar
    def check_shared_files(self):
        pass

    def menu(self):
        try:
            while True:
                option = int(input('\nOptions:\n[1] Disconnect\n[2] Upload file\n[3] Download file\n[4] Print attributes\n\nSelect an option: '))
                if option == 1:
                    response = self.disconnect()
                    print_response(response)
                    break
                elif option == 2:
                    file_name = input('Type the name of the file you want to upload: ')
                    response = self.upload_file(file_name)
                    print_response(response)
                elif option == 3:
                    file_name = input('Type the name of the file you want to download: ')
                    response = self.download_file(file_name)
                    print_response(response)
                elif option == 4:
                    print(self)
                else:
                    print('Invalid option.')
        except:
            response = self.disconnect()
            print_response(response)
            print('An error occurred. You are being disconnected.')
            exit(0)
