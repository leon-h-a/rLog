import socket


class Receiver:
    """
    add parser

    setup outputs (filepaths, ORMS (+db connect), etc...)
    initialize queue
    spin up receiving endpoint

    graceful exit
    """
    def __init__(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(("localhost", 5050))
            s.listen(1)
            while True:
                conn, addr = s.accept()
                with conn:
                    print('Connected by', addr)
                    while True:
                        data = conn.recv(1000)
                        # print(data)
                        if not data: break


if __name__ == "__main__":
    asdf = Receiver()
