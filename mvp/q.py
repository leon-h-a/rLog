from threading import Thread
import socket
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
            # print(f"got msg: {msg}")

            if msg == b"pop":
                last = self.q.get()
                conn.send(last)
            else:
                self.q.put_nowait(msg)

        conn.close()
        print("connection closed")

    def run_proc(self):
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # s.setsockopt(socket.SO_REUSEADDR)
        s.bind(("localhost", 7777))
        print("queue online")

        s.listen()

        try:
            while True:
                conn, addr = s.accept()
                print("accepted new connection")
                t = Thread(target=self.handle_conn, args=[conn])
                # t.run()
                t.start()

        except Exception as err:
            print(err)

        except KeyboardInterrupt:
            pass

        finally:
            s.close()
            print("Queue graceful exit")


if __name__ == "__main__":
    asdf = Queuer()
    asdf.run_proc()
