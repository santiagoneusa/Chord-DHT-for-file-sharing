from utils import hash_message_zone_key, get_random_node_index
import peering_pb2_grpc, peering_pb2
import grpc
from concurrent import futures

def calling(ip_port, rpc_call, **kwargs):
    try:
        with grpc.insecure_channel(ip_port) as channel:
            stub=peering_pb2_grpc.PeeringServiceStub(channel)
            if rpc_call=='1': # Upload a File
                upload_request=peering_pb2.UploadFileRequest(filename=kwargs['filename'], type=kwargs['type'])
                upload_response=stub.UploadFile(upload_request)
                print(upload_response.response)
            elif rpc_call=='2':
                download_request=peering_pb2.DownloadFileRequest(filename=kwargs['filename'])
                download_response=stub.DownloadFile(download_request)
                return download_response
    except Exception:
        print(Exception)
class Peer(peering_pb2_grpc.PeeringServiceServicer):
    def __init__(self, ip=0, port=0):
        self.id = f'{ip}:{port}'
        self.zone_key = 0
        self.ip = ip
        self.port = port
        self.files = {
            'proper': [],
            'shared': [],
        }
    def UploadFile(self, request, context):
        reply=peering_pb2.UploadFileResponse()
        try:
            self.files['proper'].append(request.filename) # Storing the file at the own database
            reply.response='File succesfully uploaded'
        except Exception:
            reply.response=Exception
        return reply
    def DownloadFile(self, request, context):
        try:
            if request.filename in self.files['proper']:
                file=self.files['proper'][self.files['proper'].index(request.filename)]
            elif request.filename in self.files['shared']:
                file=self.files['shared'][self.files['shared'].index(request.filename)]
            else:
                return peering_pb2.DownloadFileResponse(file='', confirmation=False)
            return peering_pb2.DownloadFileResponse(file=file, confirmation=True)
        except Exception:
            return peering_pb2.DownloadFileResponse(file='', confirmation=False)
            
        
            
            
        return super().DownloadFile(request, context)
    """def connect(self, server_ip, server_port):
        try:
            server = grpc(connect_to_server(server_ip, server_port))
            self.id, self.zone_key, self.number_of_zones, self.zone_size = grpc(server.register(self.ip, self.port))
            return True
        except:
            return False

    def disconnect(self, server_ip, server_port):
        try:
            server = grpc(connect_to_server(server_ip, server_port))
            return grpc(server.unregister(self.zone_key, self.id))
        except:
            return False

    def upload(self, message):
        message_zone_key = hash_message_zone_key(message, self.number_of_zones)

        server = grpc(connect_to_server(server_ip, server_port))
        available_nodes = grpc(server.get_available_nodes_by_zone(message_zone_key))
        if available_nodes['id']: 
            node_index = get_random_node_index(available_nodes['id'])
            node = grpc(connect_to_node(available_nodes['ip:port'][node_index]))
            return grpc(node.send_file(message, 'proper_files'))
        else:
            file_sent = True


    def download(self, message, server_ip, server_port):
        pass

    def check_shared(self):
        pass
    """

if __name__=='__main__':
    while True:
        try:
            ip_port='localhost:'+input("port: ") ## In the test case it will be 50051
            break
        except Exception:
            print(Exception)
        
        
    peer1=Peer()
    server=grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    peering_pb2_grpc.add_PeeringServiceServicer_to_server(peer1,server)
    server.add_insecure_port(ip_port)
    server.start()
    while True:
        try:
            option=input('What you wanna do: \n1. Upload a File\n2. Download a File\n3.Print Current Files\n4. Terminate program\n')
            if option=='1':
                port_sending='localhost:'+input('Enter the port we want to send data: ') ## In the test case it will be 50051
                filename=input('Enter the filename: ')
                type=input('Enter the type \n1. Proper\n2. Shared\n',)
                calling(port_sending, '1', filename=filename, type=type)
                ## Saber a qué dirección y puerto
            elif option=='2':
                port_requesting='localhost:'+input('Enter the port we wanto to retrieve the data from: ')
                filename=input('Enter the data we want to recover: ')
                response=calling(port_requesting, '2', filename=filename)
                if response.confirmation:
                    print(f'Archive {response.file} succesfully received')
                    peer1.files['proper'].append(response.file)
                else:
                    print('There was an error, please try again')
                
            elif option=='3':
                print(peer1.files)
            else:
                break
            
        except Exception:
            print(Exception)
    server.wait_for_termination()