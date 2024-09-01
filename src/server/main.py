from Server import Server

def main():
    try:
        server = Server()
        server.server_listener()
    except KeyboardInterrupt:
        print('Forced shutdown. Good bye.')
    except Exception as e:
        print(e)
        print('An error occurred. You are being disconnected.')

if __name__ ==  '__main__':
    main()