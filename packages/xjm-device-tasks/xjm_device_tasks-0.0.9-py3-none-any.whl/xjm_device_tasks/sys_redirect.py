import sys


class FakeStdOut:
    def __init__(self, filename="sys.log"):
        # self.log = open(filename,'a')
        pass

    def write(self, message):
        # 可以写入
        # self.log.write(message)
        pass

    def flush(self):
        pass

    def isatty(self):
        return True

