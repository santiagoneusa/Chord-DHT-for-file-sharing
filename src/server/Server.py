from utils import get_random_zone_key

class Server():

    def __init__(self, ip, port, network_size, number_of_zones) -> None:
        self.ip = ip
        self.port = port
        self.network_size = network_size
        self.registered_nodes = 0
        self.number_of_zones = number_of_zones
        self.zone_size = network_size // number_of_zones
        self.network_zones_directory = {}
        for i in range(1, number_of_zones+1):
            zone_end = i * self.zone_size
            self.network_zones_directory[zone_end] = {}
            self.network_zones_directory[zone_end]['id'] = []
            self.network_zones_directory[zone_end]['ip:port'] = []

    def __repr__(self) -> str:
        return f"""ip={self.ip}\nport={self.port}\nnetwork_size={self.network_size}\nnumber_of_zones={self.number_of_zones}\nzone_size={self.zone_size}\nnetwork_zones_directory={self.network_zones_directory})"""

    def register_node(self, node_ip, node_port):
        if self.registered_nodes == self.network_size: return -1, -1, -1

        available_zone_key = self.get_available_zone_key()
        if available_zone_key:
            node_id = available_zone_key - self.zone_size
        else:
            search_node_id = True
            while search_node_id:
                available_zone_key = get_random_zone_key(self.number_of_zones, self.zone_size)
                ids = self.network_zones_directory[available_zone_key]['id']
                for i in range(available_zone_key - self.zone_size, available_zone_key):
                    if i not in ids:
                        node_id = i
                        search_node_id = False
                        break

        self.registered_nodes += 1
        self.network_zones_directory[available_zone_key]['id'].append(node_id)
        self.network_zones_directory[available_zone_key]['ip:port'].append(f'{node_ip}:{node_port}')
        return node_id, available_zone_key, self.number_of_zones, self.zone_size

    def unregister_node(self, zone, node_id) -> bool:
        try:
            node_id_index = self.network_zones_directory[zone]['id'].index(node_id)
            self.network_zones_directory[zone]['id'].pop(node_id_index)
            self.network_zones_directory[zone]['ip:port'].pop(node_id_index)
            return True
        except:
            return False

    def get_available_nodes_by_zone(self, zone) -> dict:
        try:
            return self.network_zones_directory[zone]
        except:
            return {'id': [], 'ip:port': []}

    def get_available_zone_key(self) -> int:
        for key, nodes in self.network_zones_directory.items():
            if not nodes['id']: return key
        return 0