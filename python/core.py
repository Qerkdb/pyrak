import ctypes
import os
from utils import Utils

# Загрузите core.dll, предполагая, что он находится в той же папке, что и core.py
dll_path = os.path.join(os.path.dirname(__file__), "RakNetLibrary.dll")
core_dll = ctypes.CDLL(dll_path)


core_dll.SetMTUSize.argtypes = [ctypes.c_void_p, ctypes.c_int]  # Указатель на RakClient и int
core_dll.SetMTUSize.restype = ctypes.c_bool   

core_dll.RakClient_SetFakePing.argtypes = [ctypes.c_void_p, ctypes.c_bool, ctypes.c_int]
core_dll.RakClient_SetFakePing.restype = None

class PlayerID(ctypes.Structure):
    _fields_ = [("binaryAddress", ctypes.c_uint), ("port", ctypes.c_ushort)]

class Packet(ctypes.Structure):
    _fields_ = [
        ("playerIndex", ctypes.c_int),  # Предположим, что PlayerIndex - это int
        ("playerId", PlayerID),
        ("length", ctypes.c_uint),
        ("bitSize", ctypes.c_uint),
        ("data", ctypes.POINTER(ctypes.c_ubyte)),  # Указатель на данные
        ("deleteData", ctypes.c_bool)
    ]


core_dll.RakClient_Receive.restype = ctypes.POINTER(Packet)
core_dll.RakClient_Receive.argtypes = [ctypes.c_void_p]  # Аргумент: RakClient*


class BitStream:
    def __init__(self, data=None, lengthInBytes=0, copyData=True):
        # Define argtypes and restype for the constructor
        core_dll.BitStream_new.argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.c_uint, ctypes.c_bool]
        core_dll.BitStream_new.restype = ctypes.c_void_p
        
        # Convert Python data to ctypes array if it's not None
        print(bytes(data), lengthInBytes)
        if data:
            data = (bytes(data) * lengthInBytes)(*data)
        
        # Create the BitStream object using the C++ function
        self.bitstream = core_dll.BitStream_new(data, lengthInBytes, copyData)


    def Delete(self):
        # Убедитесь, что bitstream существует
        if self.bitstream:
            # Явно кастуем указатель в ctypes.c_void_p
            ptr = ctypes.cast(self.bitstream, ctypes.c_void_p)
            core_dll.BitStream_delete(ptr)  # Удаляем объект
            self.bitstream = None  # Зануляем указатель после удаления

    def __del__(self):
        # Безопасное удаление объекта при уничтожении Python-объекта
        self.Delete()

    def Reset(self):
        core_dll.Reset.argtypes = [ctypes.c_void_p]
        core_dll.Reset(self.bitstream)

    def ResetReadPointer(self):
        core_dll.ResetReadPointer.argtypes = [ctypes.c_void_p]
        core_dll.ResetReadPointer(self.bitstream)

    def ResetWritePointer(self):
        core_dll.ResetWritePointer.argtypes = [ctypes.c_void_p]
        core_dll.ResetWritePointer(self.bitstream)

    def SetWriteOffset(self, offset):
        core_dll.SetWriteOffset.argtypes = [ctypes.c_void_p, ctypes.c_int]
        core_dll.SetWriteOffset(self.bitstream, ctypes.c_int(offset))

    def GetWriteOffset(self):
        core_dll.GetWriteOffset.argtypes = [ctypes.c_void_p]
        core_dll.GetWriteOffset.restype = ctypes.c_int
        return core_dll.GetWriteOffset(self.bitstream)

    def SetReadOffset(self, offset):
        core_dll.SetReadOffset.argtypes = [ctypes.c_void_p, ctypes.c_int]
        core_dll.SetReadOffset(self.bitstream, ctypes.c_int(offset))

    def GetReadOffset(self):
        core_dll.GetReadOffset.argtypes = [ctypes.c_void_p]
        core_dll.GetReadOffset.restype = ctypes.c_int
        return core_dll.GetReadOffset(self.bitstream)

    def GetNumberOfBitsUsed(self):
        core_dll.GetNumberOfBitsUsed.argtypes = [ctypes.c_void_p]
        core_dll.GetNumberOfBitsUsed.restype = ctypes.c_int
        return core_dll.GetNumberOfBitsUsed(self.bitstream)

    def GetNumberOfBytesUsed(self):
        core_dll.GetNumberOfBytesUsed.argtypes = [ctypes.c_void_p]
        core_dll.GetNumberOfBytesUsed.restype = ctypes.c_int
        return core_dll.GetNumberOfBytesUsed(self.bitstream)

    def GetNumberOfUnreadBits(self):
        core_dll.GetNumberOfUnreadBits.argtypes = [ctypes.c_void_p]
        core_dll.GetNumberOfUnreadBits.restype = ctypes.c_int
        return core_dll.GetNumberOfUnreadBits(self.bitstream)

    def IgnoreBits(self, bits):
        core_dll.IgnoreBits.argtypes = [ctypes.c_void_p, ctypes.c_int]
        core_dll.IgnoreBits(self.bitstream, ctypes.c_int(bits))

    def IgnoreBytes(self, bytes):
        bits_to_ignore = bytes * 8
        core_dll.IgnoreBits.argtypes = [ctypes.c_void_p, ctypes.c_int]
        core_dll.IgnoreBits(self.bitstream, ctypes.c_int(bits_to_ignore))

    def WriteUInt8(self, value):
        if value < 0 or value > 255:
            raise ValueError(f"Value {value} is out of range for uint8_t (0-255)")
        core_dll.WriteUInt8.argtypes = [ctypes.c_void_p, ctypes.c_uint8]
        core_dll.WriteUInt8(self.bitstream, ctypes.c_uint8(value))

    def WriteUInt16(self, value):
        core_dll.WriteUInt16.argtypes = [ctypes.c_void_p, ctypes.c_uint16]
        core_dll.WriteUInt16(self.bitstream, ctypes.c_uint16(value))

    def WriteUInt32(self, value):
        core_dll.WriteUInt32.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
        core_dll.WriteUInt32(self.bitstream, ctypes.c_uint32(value))

    def WriteFloat(self, value):
        core_dll.WriteFloat.argtypes = [ctypes.c_void_p, ctypes.c_float]
        core_dll.WriteFloat(self.bitstream, ctypes.c_float(value))
    
    def WriteVector3D(self, vector):
        for value in vector:
            self.WriteFloat(value)

    def WriteString(self, value):
        core_dll.WriteString.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        core_dll.WriteString(self.bitstream, ctypes.c_char_p(value.encode('utf-8')))



    def ReadUInt8(self):
        core_dll.ReadUInt8.argtypes = [ctypes.c_void_p]
        core_dll.ReadUInt8.restype = ctypes.c_uint8
        return core_dll.ReadUInt8(self.bitstream)

    def ReadUInt16(self):
        core_dll.ReadUInt16.argtypes = [ctypes.c_void_p]
        core_dll.ReadUInt16.restype = ctypes.c_uint16
        return core_dll.ReadUInt16(self.bitstream)

    def ReadUInt32(self):
        core_dll.ReadUInt32.argtypes = [ctypes.c_void_p]
        core_dll.ReadUInt32.restype = ctypes.c_uint32
        return core_dll.ReadUInt32(self.bitstream)

    def ReadFloat(self):
        core_dll.ReadFloat.argtypes = [ctypes.c_void_p]
        core_dll.ReadFloat.restype = ctypes.c_float
        return core_dll.ReadFloat(self.bitstream)

    def ReadString(self, size):
        core_dll.ReadString.argtypes = [ctypes.c_void_p, ctypes.c_int]
        core_dll.ReadString.restype = ctypes.c_char_p
        return core_dll.ReadString(self.bitstream, ctypes.c_int(size)).decode('utf-8')

    def ReadVector3D(self):
        vector = []
        for _ in range(3):
            vector.append(self.ReadFloat())
        return vector

    def GetData(self):
        core_dll.GetData.argtypes = [ctypes.c_void_p]
        core_dll.GetData.restype = ctypes.POINTER(ctypes.c_ubyte)
        return core_dll.GetData(self.bitstream)

# Определение структуры PlayerID
class PlayerID(ctypes.Structure):
    _fields_ = [("id", ctypes.c_uint32)]

core_dll.RakClient_Create.restype = ctypes.c_void_p
core_dll.RakClient_Connect.argtypes = [
    ctypes.c_void_p,    # RakClient*
    ctypes.c_char_p,    # const char* host
    ctypes.c_ushort,    # unsigned short serverPort
    ctypes.c_ushort,    # unsigned short clientPort
    ctypes.c_uint,      # unsigned int depreciated
    ctypes.c_int,       # int threadSleepTimer
    ctypes.c_void_p     # void* pProxy
]
core_dll.RakClient_Destroy.argtypes = [ctypes.c_void_p]

# Функции из C++ для работы с RakClient и NetworkID
class RakClient:
    def __init__(self):
        self.obj = core_dll.RakClient_Create()
        if not self.obj:
            raise ValueError("Failed to create RakClient object.")

    def __del__(self):
        if self.obj:
            try:
                core_dll.RakClient_Destroy(self.obj)
            except Exception as e:
                print("Error destroying RakClient:", e)
                self.obj = None

    def Connect(self, host, serverPort, clientPort, depreciated, threadSleepTimer, pProxy=None):
        # Проверка, что объект был инициализирован
        if not self.obj:
            raise ValueError("RakClient object is not initialized.")

        # Если прокси передан, получаем его указатель
        if pProxy:
            print(1)
            proxy = pProxy.ctypes.byref(self.proxy_obj)
            # proxy = ctypes.create_string_buffer(f"{pProxy[0]}:{pProxy[1]}".encode())  # f"ip:port"
        else:
            print(2)
            proxy = ctypes.c_void_p()  # Нулевой указатель, если прокси не используется
            # proxy = None
        
        print( host, serverPort, clientPort, depreciated, threadSleepTimer)
        return core_dll.RakClient_Connect(self.obj, host, serverPort, clientPort, depreciated, threadSleepTimer, ctypes.byref(proxy))

    def Disconnect(self, blockDuration, orderingChannel):
        core_dll.RakClient_Disconnect(self.obj, blockDuration, orderingChannel)

    def SendBitStream(self, data, length, priority, reliability, orderingChannel):
        return core_dll.RakClient_SendBitStream(self.obj, data.encode('utf-8'), length, priority, reliability, orderingChannel)

    def SendData(self, data, length, priority, reliability, orderingChannel):
        return core_dll.RakClient_SendData(self.obj, data.encode('utf-8'), length, priority, reliability, orderingChannel)

    def Receive(self):
        packet_ptr = core_dll.RakClient_Receive(self.obj)
        print(1)

        if not packet_ptr:
            print("No packet received (packet is None or 0)")
            return None  # Пакет не был получен

        print(2)
        packet = packet_ptr.contents
        print(f"Packet data (as bytes)python: {bytes(packet.data)}")  # Первые 10 байт пакета
        print(f"Packet length python: {packet.length}")
        return packet


    def DeallocatePacket(self, packet):
        core_dll.RakClient_DeallocatePacket(self.obj, packet)

    def PingServer(self):
        core_dll.RakClient_PingServer(self.obj)

    def GetAveragePing(self):
        return core_dll.RakClient_GetAveragePing(self.obj)

    def GetLastPing(self):
        return core_dll.RakClient_GetLastPing(self.obj)

    def GetLowestPing(self):
        return core_dll.RakClient_GetLowestPing(self.obj)

    def SetFakePing(self, use_fake_ping, ping_value):
        """
        Устанавливает поддельный пинг для RakClient.
        
        :param rak_client_ptr: указатель на RakClient
        :param use_fake_ping: логическое значение для использования поддельного пинга
        :param ping_value: значение пинга
        """
        core_dll.RakClient_SetFakePing(self.obj, use_fake_ping, ping_value)

    def GetPlayerPing(self, playerId):
        return core_dll.RakClient_GetPlayerPing(self.obj, playerId)

    def IsConnected(self):
        return core_dll.RakClient_IsConnected(self.obj)

    def GetSynchronizedRandomInteger(self):
        return core_dll.RakClient_GetSynchronizedRandomInteger(self.obj)

    def GenerateCompressionLayer(self, inputFrequencyTable, inputLayer):
        return core_dll.RakClient_GenerateCompressionLayer(self.obj, inputFrequencyTable, inputLayer)

    def DeleteCompressionLayer(self, inputLayer):
        return core_dll.RakClient_DeleteCompressionLayer(self.obj, inputLayer)

    def RegisterAsRemoteProcedureCall(self, uniqueID, functionPointer):
        core_dll.RakClient_RegisterAsRemoteProcedureCall(self.obj, uniqueID, functionPointer)

    def UnregisterAsRemoteProcedureCall(self, uniqueID):
        core_dll.RakClient_UnregisterAsRemoteProcedureCall(self.obj, uniqueID)

    def RPC_Data(self, uniqueID, data, bitLength, priority, reliability, orderingChannel, shiftTimestamp, networkID, replyFromTarget):
        return core_dll.RakClient_RPC_Data(self.obj, uniqueID, data.encode('utf-8'), bitLength, priority, reliability, orderingChannel, shiftTimestamp, networkID, replyFromTarget)

    def RPC_BitStream(self, uniqueID, bitStream, priority, reliability, orderingChannel, shiftTimestamp, networkID, replyFromTarget):
        return core_dll.RakClient_RPC_BitStream(self.obj, uniqueID, bitStream, priority, reliability, orderingChannel, shiftTimestamp, networkID, replyFromTarget)

    def AttachPlugin(self, messageHandler):
        core_dll.RakClient_AttachPlugin(self.obj, messageHandler)

    def DetachPlugin(self, messageHandler):
        core_dll.RakClient_DetachPlugin(self.obj, messageHandler)

    def GetStaticServerData(self):
        return core_dll.RakClient_GetStaticServerData(self.obj)

    def SetStaticServerData(self, data, length):
        core_dll.RakClient_SetStaticServerData(self.obj, data.encode('utf-8'), length)

    def GetStaticClientData(self, playerId):
        return core_dll.RakClient_GetStaticClientData(self.obj, playerId)

    def SetStaticClientData(self, playerId, data, length):
        core_dll.RakClient_SetStaticClientData(self.obj, playerId, data.encode('utf-8'), length)

    def SendStaticClientDataToServer(self):
        core_dll.RakClient_SendStaticClientDataToServer(self.obj)

    def GetServerID(self):
        return core_dll.RakClient_GetServerID(self.obj)

    def GetPlayerID(self):
        return core_dll.RakClient_GetPlayerID(self.obj)

    def GetInternalID(self):
        return core_dll.RakClient_GetInternalID(self.obj)
    
    def SetMTUSize(self, size):
        return core_dll.SetMTUSize(self.obj, size)

# Функции для работы с NetworkID
class NetworkID:
    @staticmethod
    def IsPeerToPeerMode():
        return core_dll.NetworkID_IsPeerToPeerMode()

    @staticmethod
    def SetPeerToPeerMode(isPeerToPeer):
        core_dll.NetworkID_SetPeerToPeerMode(isPeerToPeer)

    @staticmethod
    def OperatorEquals(left, right):
        return core_dll.NetworkID_OperatorEquals(left, right)

    @staticmethod
    def OperatorNotEquals(left, right):
        return core_dll.NetworkID_OperatorNotEquals(left, right)

    @staticmethod
    def OperatorGreaterThan(left, right):
        return core_dll.NetworkID_OperatorGreaterThan(left, right)

    @staticmethod
    def OperatorLessThan(left, right):
        return core_dll.NetworkID_OperatorLessThan(left, right)

    @staticmethod
    def Copy(destination, source):
        core_dll.NetworkID_Copy(destination, source)

class PacketPriority:
    SYSTEM_PRIORITY = 0   # Used internally by RakNet to send above-high priority messages
    HIGH_PRIORITY = 1     # High priority messages are sent before medium priority messages
    MEDIUM_PRIORITY = 2   # Medium priority messages are sent before low priority messages
    LOW_PRIORITY = 3      # Low priority messages are only sent when no other messages are waiting
    NUMBER_OF_PRIORITIES = 4


class PacketReliability:
    UNRELIABLE = 6                  # Similar to UDP, but discards duplicate datagrams
    UNRELIABLE_SEQUENCED = 7        # UDP with sequence counter, discards out of order messages
    RELIABLE = 8                    # Reliable message, does not guarantee order
    RELIABLE_ORDERED = 9            # Reliable and ordered message, waits for out of order messages
    RELIABLE_SEQUENCED = 10         # Reliable and sequenced, discards out of order messages

UNASSIGNED_NETWORK_ID = ((0xFFFFFFFF, 0xFFFF), 65535)
