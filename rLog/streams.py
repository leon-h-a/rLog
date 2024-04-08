from rLog.models import Stream


class CSV(Stream):
    def __init__(self, streamname: str):
        super().__init__(streamname=streamname)

    def validate(self, payload: str):
        pass

    def save(self):
        pass


class Influx(Stream):
    def __init__(self, streamname: str):
        super().__init__(streamname=streamname)

    def validate(self, payload: str):
        pass

    def save(self):
        pass


if __name__ == "__main__":
    asdf = CSV("random")
    print(asdf._streamname)
