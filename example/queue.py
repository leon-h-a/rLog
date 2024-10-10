from rLog.server.utils.q_main import QueueManager
from streams import Stream

q_manager = QueueManager(Stream)
q_manager.run()
