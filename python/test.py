import ctypes

# Загрузка библиотеки
raknet = ctypes.CDLL("./RakNetLibrary.dll")

# Определите возвращаемый тип функции RakClient_Create как c_void_p
raknet.RakClient_Create.restype = ctypes.c_void_p

# Вызовите функцию и сохраните результат в переменную client
client = raknet.RakClient_Create()

# Теперь client содержит указатель на объект RakClient
print("RakClient instance created:", client)

# Определение аргументов и возвращаемого типа для RakClient_Connect
raknet.RakClient_Connect.argtypes = [
    ctypes.c_void_p,    # RakClient*
    ctypes.c_char_p,    # const char* host
    ctypes.c_ushort,    # unsigned short serverPort
    ctypes.c_ushort,    # unsigned short clientPort
    ctypes.c_uint,      # unsigned int depreciated
    ctypes.c_int,       # int threadSleepTimer
    ctypes.c_void_p     # void* pProxy
]
raknet.RakClient_Connect.restype = ctypes.c_bool  # bool return type

# Пример вызова функции с нужными параметрами
host = b"193.84.90.20"  # IP-адрес в байтовом формате
server_port = 7777
client_port = 7777
depreciated = 0
thread_sleep_timer = 30
proxy = ctypes.c_void_p()  # Создаёт пустой объект как proxy

# Вызов функции Connect
try:
    result = raknet.RakClient_Connect(
        client,              # Передаем указатель на RakClient, созданный через RakClient_Create
        host,
        server_port,
        client_port,
        depreciated,
        thread_sleep_timer,
        ctypes.byref(proxy)
    )
    print("Connection successful:", result)
except OSError as e:
    print("Connection failed with OSError:", e)

# Убедитесь, что клиент очищается после использования, вызвав RakClient_Destroy
raknet.RakClient_Destroy.argtypes = [ctypes.c_void_p]
raknet.RakClient_Destroy(client)
print("RakClient destroyed.")
