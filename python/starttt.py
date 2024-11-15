import time
import threading

# Установка путей для импорта модулей
import sys
sys.path.append('..')


# from nicial import LuaRak 
from core import BitStream, RakClient, NetworkID
from samp.client_file import PyClient

def runner(nickname, host, port):
    print(nickname, host, port)
    # client = LuaRak.client(nickname)
    client = PyClient(nickname)

    def on_receive_packet(id, bitstream):
        print(f"RECEIVE PACKET: ID - {id} | LENGTH - {bitstream.GetNumberOfBytesUsed()}")

    # Обработчик для RPC
    def on_receive_rpc(id, bitstream):
        print(f"RECEIVE RPC: ID - {id} | LENGTH - {bitstream.GetNumberOfBytesUsed()}")
        if id == 101:
            bitstream.IgnoreBytes(2)
            text = bitstream.ReadString(bitstream.ReadUInt32())
            print(f"[CHAT] {text}")
        elif id == 93:
            bitstream.IgnoreBytes(4)
            text = bitstream.ReadString(bitstream.ReadUInt32())
            print(f"[MESSAGE] {text}")

    # Установка обработчиков
    client.add_event_handler("onReceivePacket", on_receive_packet)
    client.add_event_handler("onReceiveRPC", on_receive_rpc)

    # Настройка клиента и прокси
    client.get_rak_client().SetFakePing(True, 2 ** 16)
    # proxy.connect()
    client.connect(host, port, None)

    # Бесконечный цикл для обновления сети
    while True:
        time.sleep(0.001)  # Ожидание в 1 мс
        client.update_network()


# Запуск 3 экземпляров клиента
# for i in range(1, 4):
# runner('Nivkde', b'46.174.49.47', 7844)

try:
    threading.Thread(target=runner, args=("LuaRakTest1", b"185.180.230.26", 3331)).start()
except Exception as e:
    print(e)

# Поддержание основной программы в активном состоянии
while True:
    time.sleep(1)
