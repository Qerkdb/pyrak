from core import RakCore
from utils import utils


class Proxy:
    def __init__(self, address, port, user=None, password=None):
        assert utils.is_type(address, str), "Address must be a string"
        port = str(port)
        self.proxy = RakCore.Proxy(address, port, user, password)

    def connect(self, is_no_auth=False):
        if is_no_auth:
            result = self.proxy.start_without_auth()
        else:
            result = self.proxy.start_with_auth()
        
        self.proxy.set_receiving_by_proxy(True)
        return result

    def get_proxy(self):
        return self.proxy
