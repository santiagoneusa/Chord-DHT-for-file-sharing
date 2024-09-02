import threading
from Peer import Peer
from utils import print_response

def main():
    try:
        peer = Peer()
        response = peer.connect()
        print_response(response)

        if response['status'] == 'success':
            peer_listener_thread = threading.Thread(target = peer.peer_listener)
            peer_listener_thread.start()

            menu_thread = threading.Thread(target = peer.menu)
            menu_thread.start()

            check_shared_files_thread = threading.Thread(target = peer.check_shared_files)
            check_shared_files_thread.start()

            menu_thread.join()
            peer_listener_thread.join()
            check_shared_files_thread.join()

    except KeyboardInterrupt:
        peer_listener_thread.join()
        menu_thread.join()
        check_shared_files_thread.join()
        print('Forced shutdown. Good bye.')

    except Exception as e:
        print(e)
        peer_listener_thread.join()
        menu_thread.join()
        check_shared_files_thread.join()
        print('An error occurred. You are being disconnected.')

if __name__ == '__main__':
    main()