class Sys(object):
    def __init__(self, user, passwd, ip, port):
        pass

    def send(self, body) -> bool:
        return True


class SysFake(object):
    def __init__(self):
        pass

    def send(self) -> bool:
        return False
