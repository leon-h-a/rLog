import socket
import time


class Generator:
    """
    add parser

    connect / reconnect
    emit based on predefined periods
    """
    def __init__(self):
        start = time.time()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("localhost", 5050))
            for _ in range(1000):
                s.sendall(bytes(1000))
            s.close()
            time.sleep(0.001)
        print(f"1000x 1kb elapsed time: {time.time() - start}")


if __name__ == "__main__":
    asdf = Generator()
