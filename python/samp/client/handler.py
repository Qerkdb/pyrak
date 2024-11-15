import utils
from core import BitStream
import samp.client.misc as misc

packet_enum = {
    12: lambda client, packet_id, bs: process_packet_12(client, packet_id, bs),
    34: lambda client, packet_id, bs: process_packet_34(client, packet_id, bs),
}

def process_packet_12(client, packet_id, bs):
    bs.ignoreBits(8)  # Игнорируем 8 бит
    length = bs.ReadUInt8()  # Читаем 1 байт
    input_str = bs.ReadString(length - 1)  # Читаем строку длиной length - 1
    auth_key = misc.generate_auth_key(input_str)  # Генерируем ключ
    if auth_key:
        bs_auth_packet = BitStream()  # Создаем новый битстрим
        bs_auth_packet.WriteUInt8(packet_id)  # Записываем id пакета
        bs_auth_packet.WriteUInt8(len(auth_key))  # Записываем длину ключа
        bs_auth_packet.WriteString(auth_key)  # Записываем сам ключ
        client.send_packet(bs_auth_packet)  # Отправляем пакет
    else:
        utils.log("Invalid auth key")  # Логируем ошибку

def process_packet_34(client, packet_id, bs):
    bs.ignoreBits(56)  # Игнорируем 56 бит
    client.player_id = bs.ReadUInt16()  # Читаем 2 байта для playerId
    challenge = bs.ReadUInt32()  # Читаем 4 байта для challenge
    version = 4057  # Версия игры

    bs_rpc_join = BitStream()  # Создаем новый битстрим
    bs_rpc_join.WriteInt32(version)  # Записываем версию
    bs_rpc_join.WriteUInt8(1)  # Записываем фиксированное значение 1
    bs_rpc_join.WriteUInt8(len(client.nickname))  # Записываем длину никнейма
    bs_rpc_join.WriteString(client.nickname)  # Записываем никнейм
    bs_rpc_join.WriteUInt32(challenge ^ version)  # Записываем challenge XOR version

    gpci = misc.generate_gpci(0x3e9)  # Генерация GPCI
    bs_rpc_join.WriteUInt8(len(gpci))  # Записываем длину GPCI
    bs_rpc_join.WriteString(gpci)  # Записываем GPCI

    bs_rpc_join.WriteUInt8(len(client.samp_version))  # Записываем длину версии SAMP
    bs_rpc_join.WriteString(client.samp_version)  # Записываем версию SAMP

    client.send_rpc(25, bs_rpc_join)  # Отправляем RPC

class PacketHandler:
    @staticmethod
    def processing(client, packet_id, bs):
        callback = packet_enum.get(packet_id)
        if callback:
            callback(client, packet_id, bs)
