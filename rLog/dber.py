import socket


class Dber:
    def __init__(self):
        self.q_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.q_sock.connect(("localhost", 7777))

    def get_me_values(self):
        self.q_sock.send(b"pop")
        resp = self.q_sock.recv(1024)
        print(resp)

    def disconnect(self):
        self.q_sock.close()


if __name__ == "__main__":
    pass
