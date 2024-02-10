from multiprocessing import Process
from socket import socket


class Handler(Process):
    def __init__(self, conn: socket, addr):
        super().__init__()
        self.conn = conn
        self.addr = addr

    def csv_output(self, data):
        print(f"csv: {data}")

    def db_output(self, data):
        print(f"db: {data}")

    def run(self):
        print("handler running")
        # todo: get self attrs and check streams list (if inside, use it)
        while True:
            data = self.conn.recv(1024)
            print(data)
            if not data:
                self.exit()
                break
            self.conn.sendall(bytes("ACK", "ascii"))

    def exit(self):
        self.conn.close()
        print("client disconnected")


if __name__ == "__main__":
    pass
