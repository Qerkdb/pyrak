import core
from samp.client_file import PyClient
# from LuaRak.proxy import LuaProxy
from core import BitStream


class LuaRak:
    """Класс LuaRak для создания клиента, BitStream, proxy и доступа к ядру RakNet."""
    # @staticmethod
    def client(self, nickname) -> PyClient:
        print(nickname)
        """Создает новый экземпляр клиента SAMP."""
        return PyClient(nickname)

    def BitStream(self, *args) -> BitStream:
        """Создает новый буфер BitStream."""
        return BitStream(*args)

    # def proxy(self, address: str, port: int, user: str, password: str) -> LuaProxy:
    #     """Создает SOCKS5 UDP прокси."""
    #     return LuaProxy(address, port, user, password)

    def getCore(self):
        """Возвращает основную библиотеку RakNet."""
        return core


# Экземпляр класса для использования в других частях программы
py_rak = LuaRak()
