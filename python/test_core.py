from core import RakClient

client = RakClient()

print("RakClient create")

try:
    result = client.Connect(
        host=b"193.84.90.20",
        serverPort=7777,
        clientPort=7777,
        depreciated=0,
        threadSleepTimer=30,
        pProxy=None
    )
    print("Connection successful:", result)
except Exception as e:
    print("Connection failed with:", e)

print("RakClient destroyed.")


# from bitstream import BitStream
from core import BitStream
bitstream = BitStream()

# Запись данных
bitstream.WriteUInt8(2)         # Записываем 8-битное число
bitstream.WriteUInt16(65535)      # Записываем 16-битное число
bitstream.WriteUInt32(4294967295) # Записываем 32-битное число
bitstream.WriteFloat(3.14)        # Записываем число с плавающей точкой

# Запись 3D-вектора
vector = [1.0, 2.0, 3.0]
bitstream.WriteVector3D(vector)

# Запись строки
bitstream.WriteString("Hello")
# Сброс указателей чтения и записи
# bitstream.ResetReadPointer()
# bitstream.ResetWritePointer()

# Чтение данных
value_uint8 = bitstream.ReadUInt8()
value_uint16 = bitstream.ReadUInt16()
value_uint32 = bitstream.ReadUInt32()
value_float = bitstream.ReadFloat()

value_vector_3d = bitstream.ReadVector3D()
# Чтение строки (укажите размер строки, который хотите прочитать)
value_string = bitstream.ReadString(5)  # Пример для строки длиной 12 байт
# Получение информации о потоке битов
write_offset = bitstream.GetWriteOffset()
read_offset = bitstream.GetReadOffset()
bits_used = bitstream.GetNumberOfBitsUsed()
bytes_used = bitstream.GetNumberOfBytesUsed()
unread_bits = bitstream.GetNumberOfUnreadBits()

# Игнорирование части данных
# bitstream.IgnoreBits(8)       # Пропустить 8 бит
# bitstream.IgnoreBytes(2)       # Пропустить 2 байта

# Получение указателя на данные
data_ptr = bitstream.GetData()
print("Vector 3D:", value_vector_3d)
print("8-bit unsigned int:", value_uint8)
print("16-bit unsigned int:", value_uint16)
print("32-bit unsigned int:", value_uint32)
print("Float:", value_float)
print("Write Offset:", write_offset)
print("Read Offset:", read_offset)
print("Bits Used:", bits_used)
print("Bytes Used:", bytes_used)
print("Unread Bits:", unread_bits)
print("Data Pointer:", data_ptr)
print("String:", value_string)