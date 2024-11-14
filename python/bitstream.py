from core import BitStream as RakCoreBitStream
import utils

class BitStream:
    def __init__(self, *args):
        if len(args) == 0 or len(args) == 3:
            self.bitstream = RakCoreBitStream(*args)
        else:
            self.bitstream = args[0]

    def reset(self):
        self.bitstream.Reset()

    def resetReadPointer(self):
        self.bitstream.ResetReadPointer()

    def resetWritePointer(self):
        self.bitstream.ResetWritePointer()

    def setWriteOffset(self, offset):
        self.bitstream.SetWriteOffset(offset)

    def getWriteOffset(self):
        return self.bitstream.GetWriteOffset()

    def setReadOffset(self, offset):
        return self.bitstream.SetReadOffset(offset)

    def getReadOffset(self):
        return self.bitstream.GetReadOffset()

    def getNumberOfBitsUsed(self):
        return self.bitstream.GetNumberOfBitsUsed()

    def getNumberOfBytesUsed(self):
        return self.bitstream.GetNumberOfBytesUsed()

    def getNumberOfUnreadBits(self):
        return self.bitstream.GetNumberOfUnreadBits()

    def getNumberOfUnreadBytes(self):
        return utils.convertBitsToBytes(self.getNumberOfUnreadBits())

    def ignoreBits(self, bits):
        self.bitstream.IgnoreBits(bits)

    def ignoreBytes(self, bytes):
        self.bitstream.IgnoreBits(utils.convertBytesToBits(bytes))

    def writeUInt8(self, value):
        self.bitstream.WriteUInt8(value)

    def writeUInt16(self, value):
        self.bitstream.WriteUInt16(value)

    def writeUInt32(self, value):
        self.bitstream.WriteUInt32(value)

    def writeFloat(self, value):
        self.bitstream.WriteFloat(value)

    def writeVector3D(self, vector):
        for value in vector:
            self.bitstream.WriteFloat(value)

    def writeString(self, value):
        self.bitstream.WriteString(value)

    def readUInt8(self):
        return self.bitstream.ReadUInt8()

    def readUInt16(self):
        return self.bitstream.ReadUInt16()

    def readUInt32(self):
        return self.bitstream.ReadUInt32()

    def readFloat(self):
        return self.bitstream.ReadFloat()

    def readString(self, size):
        return self.bitstream.ReadString(size)

    def getBitStream(self):
        return self.bitstream

    def getDataPtr(self):
        return utils.getPointer(self.bitstream.GetData())
