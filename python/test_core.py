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