class Peer:
    def __init__(self, ip, port):
        self.id = f'{ip}:{port}'
        self.files = {
            'proper': [],
            'shared': [],
        }

    def connect(self):
        pass

    def disconnect(self):
        pass

    def upload(self):
        pass

    def download(self):
        pass

    def check_shared(self):
        pass