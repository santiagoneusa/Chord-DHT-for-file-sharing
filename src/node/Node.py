from utils import hash_message_zone_key, get_random_node_index

class Peer:
    def __init__(self, ip, port):
        self.id = f'{ip}:{port}'
        self.zone_key = 0
        self.ip = ip
        self.port = port
        self.files = {
            'proper': [],
            'shared': [],
        }

    def connect(self, server_ip, server_port):
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