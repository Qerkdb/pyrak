# Wrapper for RakClient

from core import RakClient, PacketPriority, PacketReliability, UNASSIGNED_NETWORK_ID
from utils import Utils
import utils
from core import BitStream
from samp.client.handler import PacketHandler

import ctypes

class Packet(ctypes.Structure):
    _fields_ = [("length", ctypes.c_int), ("data", ctypes.POINTER(ctypes.c_char))]



class PyClient:
    def __init__(self, nickname: str):
        # assert utils.isType(nickname, str), "Nickname is expected as a string"
        self.rak_client = RakClient()
        assert self.rak_client, "Error creating RakClient"

        self.nickname = nickname
        self.player_id = -1
        self.samp_version = "0.3.7-R3"
        self.receive_packet_handlers = []
        self.receive_rpc_handlers = []

        self.rak_client.SetMTUSize(576)

        # self.rak_client.register_receive_rpc_handler(self._rpc_handler)

    def _rpc_handler(self, rpc_id, bs):
        for handler in self.receive_rpc_handlers:
            handler(rpc_id, BitStream(bs))

    def connect(self, ip: str, port: int, proxy=None) -> bool:
        proxy = proxy.getProxy() if proxy else print("no proxy")#Proxy()
        return self.rak_client.Connect(ip, port, 0, 0, 5, None)

    def disconnect(self, timeout: int = 1):
        self.player_id = -1
        self.rak_client.Disconnect(timeout)

    def send_packet(self, *args) -> bool:
        if Utils.isType(args[0], dict):
            bs = Utils.getBitStream(args[0])
            return self.rak_client.RPC_BitStream(bs, PacketPriority.HIGH_PRIORITY, PacketReliability.RELIABLE_ORDERED, 0)
        else:
            data, length = args[0], args[1]
            return self.rak_client.RPC_Data(data, length, PacketPriority.HIGH_PRIORITY, PacketReliability.RELIABLE_ORDERED, 0)

    def send_rpc(self, rpc_id: int, *args) -> bool:
        if Utils.isType(args[0], dict):
            bs = Utils.getBitStream(args[0])
            return self.rak_client.RPC_BitStream(rpc_id, bs, PacketPriority.HIGH_PRIORITY, PacketReliability.RELIABLE_ORDERED, 0, False, UNASSIGNED_NETWORK_ID, None)
        else:
            data, length = args[0], args[1]
            return self.rak_client.RPC_Data(rpc_id, data, length, PacketPriority.HIGH_PRIORITY, PacketReliability.RELIABLE_ORDERED, 0, False, UNASSIGNED_NETWORK_ID, None)

    def update_network(self):
        packet = self.rak_client.Receive()
        if packet:
            print(f"Packet data: {packet}")
            bs = BitStream(packet.data, packet.length, False)
            packet_id = bs.readUInt8()
            for handler in self.receive_packet_handlers:
                handler(packet_id, bs)
            PacketHandler.processing(self, packet_id, bs)
            self.rak_client.DeallocatePacket(packet)



    def add_event_handler(self, event_name: str, callback):
        if event_name == "onReceivePacket":
            self.receive_packet_handlers.append(callback)
        elif event_name == "onReceiveRPC":
            self.receive_rpc_handlers.append(callback)

    def get_rak_client(self):
        return self.rak_client

    def set_samp_version(self, version: str):
        self.samp_version = version

    def set_nickname(self, nickname: str):
        self.nickname = nickname

    def get_nickname(self) -> str:
        return self.nickname

    def get_id(self) -> int:
        return self.player_id

    def send_chat(self, text: str):
        bs = BitStream()
        bs.writeUInt8(len(text))
        bs.writeString(text)
        self.send_rpc(101, bs)

    def send_command(self, command: str):
        bs = BitStream()
        bs.writeUInt32(len(command))
        bs.writeString(command)
        self.send_rpc(50, bs)

pyclient = PyClient("pluernick")