from rLog.server.utils.q_deque import Dequeuer
from rLog.server.streams import Stream


if __name__ == "__main__":
    dq = Dequeuer(Stream)
    dq.run()
