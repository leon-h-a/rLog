from abc import ABCMeta


class Parser(metaclass=ABCMeta):
    identifier = None

    def __init__(self, serialized_msg):
        self.serialized_msg = serialized_msg

    def _sanitize(self) -> str:
        raise NotImplementedError

    def _build_for_queue(self) -> str:
        raise NotImplementedError

    def parse(self):
        self._sanitize()
        self._build_for_queue()


class CSV(Parser):
    identifier = "csv"

    def __init__(self, serialized_msg):
        super().__init__(serialized_msg)

    def _sanitize(self) -> str:
        # todo: payload must not be nested
        pass

    def _build_for_queue(self) -> str:
        pass


class PSQL(Parser):
    identifier = "psql"

    def __init__(self, serialized_msg):
        super().__init__(serialized_msg)

    def _sanitize(self) -> str:
        pass

    def _build_for_queue(self) -> str:
        pass
