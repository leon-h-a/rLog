from threading import Thread
from socket import socket
from queue import Queue


class Queuer:
    def __init__(self):
        self.q = Queue()

    def handle_conn(self, conn: socket):
        # multiple clients shall be able to put
        # data into sync queue
        while True:
            msg = conn.recv(1024)
            if not msg:
                break
            print(f"got msg: {msg}")
            conn.send(b"wassup")

        # self.q.put_nowait(msg)

        conn.shutdown()
        conn.close()
        print("connection closed")

    def handle_targets(self):
        # allow multiple db handlers to pop
        # data from single queue (h-scale)
        pass

    def enq(self):
        # multiple clients
        pass

    def deq(self):
        # single connection
        pass

    def run_proc(self):
        s = socket()
        s.bind(("localhost", 7777))
        print("queue online")

        s.listen(2)

        try:
            while True:
                conn, addr = s.accept()
                t = Thread(target=self.handle_conn, args=[conn])
                t.run()

        except Exception as err:
            print(err)

        finally:
            s.shutdown()
            s.close()
            print("Queue graceful exit")


if __name__ == "__main__":
    asdf = Queuer()
    asdf.run_proc()
