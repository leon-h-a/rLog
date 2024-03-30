import os
import socket


class Dispatch:
    def __init__(self):
        self.cli_conn: socket = None
        self.que_conn: socket = None
        self.create_sockets()

    def create_sockets(self):
        self.cli_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.que_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.que_conn.connect(("0.0.0.0", 7777))

    def run_process(self):
        host = os.environ['rLogLocalIP']
        port = int(os.environ['rLogLocalPORT'])

        print("dispatch online")
        # self.que_conn.send(b"hello")
        # resp = self.que_conn.recv(100)
        # print(f"init ping resp: {resp}")

        with self.cli_conn as s:
            s.bind((host, port))
            s.listen()
            try:
                conn, addr = s.accept()
                while True:

                    data = conn.recv(1024)
                    if not data:
                        print("client closed connection")
                        break
                    else:
                        print(f"got data: {data}")

                        q_resp = self.que_conn.send(data)
                        print(f"q resp: {q_resp}")

                        conn.sendall(bytes("ACK", "ascii"))

            except Exception as err:
                raise err

            finally:
                self.kill_process()

    def kill_process(self):
        self.cli_conn.close()
        self.que_conn.close()
        print("gracefull exit")


if __name__ == "__main__":
    dispatch = Dispatch()
    dispatch.run_process()

