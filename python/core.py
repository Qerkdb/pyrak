import ctypes
import os
from utils import Utils

# Загрузите core.dll, предполагая, что он находится в той же папке, что и core.py
dll_path = os.path.join(os.path.dirname(__file__), "RakNetLibrary.dll")
core_dll = ctypes.CDLL(dll_path)


class BitStream:
    def __init__(self, data=None, lengthInBytes=0, copyData=True):
        # Определение конструктора BitStream
        core_dll.BitStream_new.argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.c_uint, ctypes.c_bool]
        core_dll.BitStream_new.restype = ctypes.c_void_p
        
        # Преобразование Python-данных в ctypes для передачи в конструктор C++
        data = (ctypes.c_ubyte * len(data))(*data) if data else None
        self.obj = core_dll.BitStream_new(data, lengthInBytes, copyData)

    def Reset(self):
        core_dll.BitStream_Reset(self.bitstream)

    def ResetReadPointer(self):
        core_dll.BitStream_ResetReadPointer(self.bitstream)

    def ResetWritePointer(self):
        core_dll.BitStream_ResetWritePointer(self.bitstream)

    def SetWriteOffset(self, offset):
        core_dll.BitStream_SetWriteOffset(self.bitstream, ctypes.c_int(offset))

    def GetWriteOffset(self):
        core_dll.BitStream_GetWriteOffset.restype = ctypes.c_int
        return core_dll.BitStream_GetWriteOffset(self.bitstream)

    def SetReadOffset(self, offset):
        core_dll.BitStream_SetReadOffset(self.bitstream, ctypes.c_int(offset))

    def GetReadOffset(self):
        core_dll.BitStream_GetReadOffset.restype = ctypes.c_int
        return core_dll.BitStream_GetReadOffset(self.bitstream)

    def GetNumberOfBitsUsed(self):
        core_dll.BitStream_GetNumberOfBitsUsed.restype = ctypes.c_int
        return core_dll.BitStream_GetNumberOfBitsUsed(self.bitstream)

    def GetNumberOfBytesUsed(self):
        core_dll.BitStream_GetNumberOfBytesUsed.restype = ctypes.c_int
        return core_dll.BitStream_GetNumberOfBytesUsed(self.bitstream)

    def GetNumberOfUnreadBits(self):
        core_dll.BitStream_GetNumberOfUnreadBits.restype = ctypes.c_int
        return core_dll.BitStream_GetNumberOfUnreadBits(self.bitstream)

    def IgnoreBits(self, bits):
        core_dll.BitStream_IgnoreBits(self.bitstream, ctypes.c_int(bits))

    def IgnoreBytes(self, bytes):
        bits_to_ignore = bytes * 8
        core_dll.BitStream_IgnoreBits(self.bitstream, ctypes.c_int(bits_to_ignore))

    def WriteUInt8(self, value):
        core_dll.BitStream_WriteUInt8(self.bitstream, ctypes.c_uint8(value))

    def WriteUInt16(self, value):
        core_dll.BitStream_WriteUInt16(self.bitstream, ctypes.c_uint16(value))

    def WriteUInt32(self, value):
        core_dll.BitStream_WriteUInt32(self.bitstream, ctypes.c_uint32(value))

    def WriteFloat(self, value):
        core_dll.BitStream_WriteFloat(self.bitstream, ctypes.c_float(value))

    def WriteString(self, value):
        core_dll.BitStream_WriteString(self.bitstream, ctypes.c_char_p(value.encode('utf-8')))

    def ReadUInt8(self):
        core_dll.BitStream_ReadUInt8.restype = ctypes.c_uint8
        return core_dll.BitStream_ReadUInt8(self.bitstream)

    def ReadUInt16(self):
        core_dll.BitStream_ReadUInt16.restype = ctypes.c_uint16
        return core_dll.BitStream_ReadUInt16(self.bitstream)

    def ReadUInt32(self):
        core_dll.BitStream_ReadUInt32.restype = ctypes.c_uint32
        return core_dll.BitStream_ReadUInt32(self.bitstream)

    def ReadFloat(self):
        core_dll.BitStream_ReadFloat.restype = ctypes.c_float
        return core_dll.BitStream_ReadFloat(self.bitstream)

    def ReadString(self, size):
        core_dll.BitStream_ReadString.restype = ctypes.c_char_p
        return core_dll.BitStream_ReadString(self.bitstream, ctypes.c_int(size)).decode('utf-8')

    def GetData(self):
        core_dll.BitStream_GetData.restype = ctypes.POINTER(ctypes.c_ubyte)
        return core_dll.BitStream_GetData(self.bitstream)

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
        
        return core_dll.RakClient_Connect(
            self.obj, host, serverPort, clientPort, depreciated, threadSleepTimer, ctypes.byref(proxy)
        )

    def Disconnect(self, blockDuration, orderingChannel):
        core_dll.RakClient_Disconnect(self.obj, blockDuration, orderingChannel)

    def SendBitStream(self, data, length, priority, reliability, orderingChannel):
        return core_dll.RakClient_SendBitStream(self.obj, data.encode('utf-8'), length, priority, reliability, orderingChannel)

    def SendData(self, data, length, priority, reliability, orderingChannel):
        return core_dll.RakClient_SendData(self.obj, data.encode('utf-8'), length, priority, reliability, orderingChannel)

    def Receive(self):
        return core_dll.RakClient_Receive(self.obj)

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
