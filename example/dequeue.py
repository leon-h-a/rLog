from rLog.server.utils.q_deque import Dequeuer
from streams import Stream

dq = Dequeuer(Stream)
dq.run()
