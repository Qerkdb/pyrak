import ctypes
import math


class Utils:
    
    def convertBitsToBytes(self, bits):
        return (bits + 7) >> 3

    def convertBytesToBits(self, bytes):
        return bytes << 3

    def getBitStream(self, bitstream):
        return bitstream if isinstance(bitstream, ctypes.Structure) else bitstream.getBitStream()

    def getProxy(self, proxy):
        return proxy if isinstance(proxy, ctypes.Structure) else proxy.getProxy()

    def log(self, text):
        print(f"[LuaRak]: {text}")

    def isType(self, value, inType):
        return isinstance(value, inType)

    def getPointer(self, cdata):
        return ctypes.cast(ctypes.pointer(ctypes.c_void_p(ctypes.addressof(cdata))), ctypes.c_void_p).value


utils = Utils()
