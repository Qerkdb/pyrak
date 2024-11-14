#include "BitStream.h"
#include "RakClient.h"
#include "NetworkTypes.h"
#include <vector>
#include <string>

extern "C" __declspec(dllexport) void RakClient_SetTrackFrequencyTable(RakClient* client, bool b)
{
    client->SetTrackFrequencyTable(b);
}


extern "C" __declspec(dllexport) bool NetworkID_IsPeerToPeerMode(void)
{
    return NetworkID::IsPeerToPeerMode();
}

extern "C" __declspec(dllexport) void NetworkID_SetPeerToPeerMode(bool isPeerToPeer)
{
    NetworkID::SetPeerToPeerMode(isPeerToPeer);
}

extern "C" __declspec(dllexport) bool NetworkID_OperatorEquals(NetworkID* left, const NetworkID* right)
{
    return (*left) == (*right);
}

extern "C" __declspec(dllexport) bool NetworkID_OperatorNotEquals(NetworkID* left, const NetworkID* right)
{
    return (*left) != (*right);
}

extern "C" __declspec(dllexport) bool NetworkID_OperatorGreaterThan(NetworkID* left, const NetworkID* right)
{
    return (*left) > (*right);
}

extern "C" __declspec(dllexport) bool NetworkID_OperatorLessThan(NetworkID* left, const NetworkID* right)
{
    return (*left) < (*right);
}

extern "C" __declspec(dllexport) void NetworkID_Copy(NetworkID* destination, const NetworkID* source)
{
    *destination = *source;
}

extern "C" __declspec(dllexport) RakClient* RakClient_Create()
{
    return new RakClient();
}

extern "C" __declspec(dllexport) void RakClient_Destroy(RakClient* client)
{
    delete client;
}

extern "C" __declspec(dllexport) bool RakClient_Connect(RakClient* client, const char* host, unsigned short serverPort, unsigned short clientPort, unsigned int depreciated, int threadSleepTimer, void* pProxy)
{
    try {
        if (client == nullptr) {
            printf("RakClient_Connect received a nullptr for client\n");
            return false;
        }
        printf("Connecting to host: %s, serverPort: %d, clientPort: %d\n", host, serverPort, clientPort);
        return client->Connect(host, serverPort, clientPort, depreciated, threadSleepTimer, pProxy);
    }
    catch (const std::exception& e) {
        printf("Exception in RakClient_Connect: %s\n", e.what());
        return false;
    }
    catch (...) {
        printf("Unknown exception in RakClient_Connect\n");
        return false;
    }
}



extern "C" __declspec(dllexport) void RakClient_Disconnect(RakClient* client, unsigned int blockDuration, unsigned char orderingChannel)
{
    client->Disconnect(blockDuration, orderingChannel);
}

extern "C" __declspec(dllexport) bool RakClient_SendBitStream(RakClient* client, const char* data, int length, PacketPriority priority, PacketReliability reliability, char orderingChannel)
{
    RakNet::BitStream bitStream;
    bitStream.Write(data, length);  // Записываем данные в BitStream
    return client->Send(&bitStream, priority, reliability, orderingChannel);
}

extern "C" __declspec(dllexport) bool RakClient_SendData(RakClient* client, const char* data, int length, PacketPriority priority, PacketReliability reliability, char orderingChannel)
{
    return client->Send(data, length, priority, reliability, orderingChannel);
}

extern "C" __declspec(dllexport) Packet* RakClient_Receive(RakClient* client)
{
    return client->Receive();
}

extern "C" __declspec(dllexport) void RakClient_DeallocatePacket(RakClient* client, Packet* packet)
{
    client->DeallocatePacket(packet);
}

extern "C" __declspec(dllexport) void RakClient_PingServer(RakClient* client)
{
    client->PingServer();
}

extern "C" __declspec(dllexport) int RakClient_GetAveragePing(RakClient* client)
{
    return client->GetAveragePing();
}

extern "C" __declspec(dllexport) int RakClient_GetLastPing(RakClient* client)
{
    return client->GetLastPing();
}

extern "C" __declspec(dllexport) int RakClient_GetLowestPing(RakClient* client)
{
    return client->GetLowestPing();
}

extern "C" __declspec(dllexport) int RakClient_GetPlayerPing(RakClient* client, const PlayerID playerId)
{
    return client->GetPlayerPing(playerId);
}

extern "C" __declspec(dllexport) void RakClient_StartOccasionalPing(RakClient* client)
{
    client->StartOccasionalPing();
}

extern "C" __declspec(dllexport) void RakClient_StopOccasionalPing(RakClient* client)
{
    client->StopOccasionalPing();
}

extern "C" __declspec(dllexport) bool RakClient_IsConnected(RakClient* client)
{
    return client->IsConnected();
}

extern "C" __declspec(dllexport) unsigned int RakClient_GetSynchronizedRandomInteger(RakClient* client)
{
    return client->GetSynchronizedRandomInteger();
}

extern "C" __declspec(dllexport) bool RakClient_GenerateCompressionLayer(RakClient* client, unsigned int inputFrequencyTable[256], bool inputLayer)
{
    return client->GenerateCompressionLayer(inputFrequencyTable, inputLayer);
}

extern "C" __declspec(dllexport) bool RakClient_DeleteCompressionLayer(RakClient* client, bool inputLayer)
{
    return client->DeleteCompressionLayer(inputLayer);
}

extern "C" __declspec(dllexport) void RakClient_RegisterAsRemoteProcedureCall(RakClient* client, int* uniqueID, void (*functionPointer)(RPCParameters* rpcParms))
{
    client->RegisterAsRemoteProcedureCall(uniqueID, functionPointer);
}

extern "C" __declspec(dllexport) void RakClient_UnregisterAsRemoteProcedureCall(RakClient* client, int* uniqueID)
{
    client->UnregisterAsRemoteProcedureCall(uniqueID);
}

extern "C" __declspec(dllexport) bool RakClient_RPC_Data(RakClient* client, int* uniqueID, const char* data, unsigned int bitLength, PacketPriority priority, PacketReliability reliability, char orderingChannel, bool shiftTimestamp, NetworkID networkID, RakNet::BitStream* replyFromTarget)
{
    return client->RPC(uniqueID, data, bitLength, priority, reliability, orderingChannel, shiftTimestamp, networkID, replyFromTarget);
}

extern "C" __declspec(dllexport) bool RakClient_RPC_BitStream(RakClient* client, int* uniqueID, RakNet::BitStream* bitStream, PacketPriority priority, PacketReliability reliability, char orderingChannel, bool shiftTimestamp, NetworkID networkID, RakNet::BitStream* replyFromTarget)
{
    return client->RPC(uniqueID, bitStream, priority, reliability, orderingChannel, shiftTimestamp, networkID, replyFromTarget);
}

extern "C" __declspec(dllexport) bool RakClient_GetSendFrequencyTable(RakClient* client, unsigned int outputFrequencyTable[256])
{
    return client->GetSendFrequencyTable(outputFrequencyTable);
}

extern "C" __declspec(dllexport) float RakClient_GetCompressionRatio(RakClient* client)
{
    return client->GetCompressionRatio();
}

extern "C" __declspec(dllexport) float RakClient_GetDecompressionRatio(RakClient* client)
{
    return client->GetDecompressionRatio();
}

extern "C" __declspec(dllexport) void RakClient_AttachPlugin(RakClient* client, PluginInterface* messageHandler)
{
    client->AttachPlugin(messageHandler);
}

extern "C" __declspec(dllexport) void RakClient_DetachPlugin(RakClient* client, PluginInterface* messageHandler)
{
    client->DetachPlugin(messageHandler);
}

extern "C" __declspec(dllexport) RakNet::BitStream* RakClient_GetStaticServerData(RakClient* client)
{
    return client->GetStaticServerData();
}

extern "C" __declspec(dllexport) void RakClient_SetStaticServerData(RakClient* client, const char* data, int length)
{
    client->SetStaticServerData(data, length);
}

extern "C" __declspec(dllexport) RakNet::BitStream* RakClient_GetStaticClientData(RakClient* client, const PlayerID playerId)
{
    return client->GetStaticClientData(playerId);
}

extern "C" __declspec(dllexport) void RakClient_SetStaticClientData(RakClient* client, const PlayerID playerId, const char* data, int length)
{
    client->SetStaticClientData(playerId, data, length);
}

extern "C" __declspec(dllexport) void RakClient_SendStaticClientDataToServer(RakClient* client)
{
    client->SendStaticClientDataToServer();
}

extern "C" __declspec(dllexport) PlayerID* RakClient_GetServerID(RakClient* client)
{
    PlayerID* serverID = new PlayerID(client->GetServerID());
    return serverID;  // Возвращаем указатель на динамически выделенный объект
}

extern "C" __declspec(dllexport) PlayerID* RakClient_GetPlayerID(RakClient* client)
{
    PlayerID* playerID = new PlayerID(client->GetPlayerID());
    return playerID;  // Возвращаем указатель на динамически выделенный объект
}

extern "C" __declspec(dllexport) PlayerID* RakClient_GetInternalID(RakClient* client)
{
    PlayerID* internalID = new PlayerID(client->GetInternalID());
    return internalID;  // Возвращаем указатель на динамически выделенный объект
}


extern "C" __declspec(dllexport) const char* RakClient_PlayerIDToDottedIP(RakClient* client, const PlayerID playerId)
{
    return client->PlayerIDToDottedIP(playerId);
}

extern "C" __declspec(dllexport) void RakClient_PushBackPacket(RakClient* client, Packet* packet, bool pushAtHead)
{
    client->PushBackPacket(packet, pushAtHead);
}

extern "C" __declspec(dllexport) void RakClient_SetRouterInterface(RakClient* client, RouterInterface* routerInterface)
{
    client->SetRouterInterface(routerInterface);
}

extern "C" __declspec(dllexport) void RakClient_RemoveRouterInterface(RakClient* client, RouterInterface* routerInterface)
{
    client->RemoveRouterInterface(routerInterface);
}

extern "C" __declspec(dllexport) void RakClient_SetTimeoutTime(RakClient* client, RakNetTime timeMS)
{
    client->SetTimeoutTime(timeMS);
}

extern "C" __declspec(dllexport) bool RakClient_SetMTUSize(RakClient* client, int size)
{
    return client->SetMTUSize(size);
}

extern "C" __declspec(dllexport) int RakClient_GetMTUSize(RakClient* client)
{
    return client->GetMTUSize();
}

extern "C" __declspec(dllexport) void RakClient_AllowConnectionResponseIPMigration(RakClient* client, bool allow)
{
    client->AllowConnectionResponseIPMigration(allow);
}

extern "C" __declspec(dllexport) void RakClient_AdvertiseSystem(RakClient* client, const char* host, unsigned short remotePort, const char* data, int dataLength)
{
    client->AdvertiseSystem(host, remotePort, data, dataLength);
}

extern "C" __declspec(dllexport) RakNetStatisticsStruct* RakClient_GetStatistics(RakClient* client)
{
    return client->GetStatistics();
}

extern "C" __declspec(dllexport) void RakClient_ApplyNetworkSimulator(RakClient* rakClient, double maxSendBPS, unsigned short minExtraPing, unsigned short extraPingVariance)
{
    rakClient->ApplyNetworkSimulator(maxSendBPS, minExtraPing, extraPingVariance);
}

extern "C" __declspec(dllexport) bool RakClient_IsNetworkSimulatorActive(RakClient* rakClient)
{
    return rakClient->IsNetworkSimulatorActive();
}

extern "C" __declspec(dllexport) int RakClient_GetPlayerIndex(RakClient* rakClient)
{
    return rakClient->GetPlayerIndex();
}

extern "C" __declspec(dllexport) void RakClient_SetFakePing(RakClient* rakClient, bool bUseFakePing, __int32 ping)
{
    rakClient->SetFakePing(bUseFakePing, ping);
}

extern "C" __declspec(dllexport) void PlayerID_SetBinaryAddress(PlayerID* playerID, const char* str)
{
    playerID->SetBinaryAddress(str);
}

extern "C" {
    __declspec(dllexport) void* BitStream_new(unsigned char* data, unsigned int lengthInBytes, bool copyData) {
        return new RakNet::BitStream(data, lengthInBytes, copyData);
    }

    __declspec(dllexport) void BitStream_delete(void* ptr) {
        delete static_cast<RakNet::BitStream*>(ptr);
    }

    __declspec(dllexport) void SetNumberOfBitsAllocated(void* ptr, unsigned int lengthInBits) {
        static_cast<RakNet::BitStream*>(ptr)->SetNumberOfBitsAllocated(lengthInBits);
    }

    __declspec(dllexport) unsigned int GetNumberOfBitsUsed(void* ptr) {
        return static_cast<RakNet::BitStream*>(ptr)->GetNumberOfBitsUsed();
    }

    __declspec(dllexport) void WriteUInt8(void* ptr, unsigned char value) {
        static_cast<RakNet::BitStream*>(ptr)->Write(reinterpret_cast<const char*>(&value), sizeof(value));
    }

    __declspec(dllexport) void WriteUInt16(void* ptr, unsigned short value) {
        static_cast<RakNet::BitStream*>(ptr)->Write(reinterpret_cast<const char*>(&value), sizeof(value));
    }

    __declspec(dllexport) void WriteUInt32(void* ptr, unsigned int value) {
        static_cast<RakNet::BitStream*>(ptr)->Write(reinterpret_cast<const char*>(&value), sizeof(value));
    }

    __declspec(dllexport) void WriteInt8(void* ptr, char value) {
        static_cast<RakNet::BitStream*>(ptr)->Write(reinterpret_cast<const char*>(&value), sizeof(value));
    }

    __declspec(dllexport) void WriteInt16(void* ptr, short value) {
        static_cast<RakNet::BitStream*>(ptr)->Write(reinterpret_cast<const char*>(&value), sizeof(value));
    }

    __declspec(dllexport) void WriteInt32(void* ptr, int value) {
        static_cast<RakNet::BitStream*>(ptr)->Write(reinterpret_cast<const char*>(&value), sizeof(value));
    }

    __declspec(dllexport) void WriteBool(void* ptr, bool value) {
        static_cast<RakNet::BitStream*>(ptr)->Write(reinterpret_cast<const char*>(&value), sizeof(value));
    }

    __declspec(dllexport) void WriteFloat(void* ptr, float value) {
        static_cast<RakNet::BitStream*>(ptr)->Write(reinterpret_cast<const char*>(&value), sizeof(value));
    }

    __declspec(dllexport) void WriteString(void* ptr, const char* value) {
        unsigned int len = static_cast<unsigned int>(strlen(value));
        static_cast<RakNet::BitStream*>(ptr)->Write(value, len);
    }

    // Функции для чтения значений различных типов из BitStream напрямую

    __declspec(dllexport) unsigned char ReadUInt8(void* ptr) {
        unsigned char value;
        static_cast<RakNet::BitStream*>(ptr)->Read(reinterpret_cast<char*>(&value), sizeof(value));
        return value;
    }

    __declspec(dllexport) unsigned short ReadUInt16(void* ptr) {
        unsigned short value;
        static_cast<RakNet::BitStream*>(ptr)->Read(reinterpret_cast<char*>(&value), sizeof(value));
        return value;
    }

    __declspec(dllexport) unsigned int ReadUInt32(void* ptr) {
        unsigned int value;
        static_cast<RakNet::BitStream*>(ptr)->Read(reinterpret_cast<char*>(&value), sizeof(value));
        return value;
    }

    __declspec(dllexport) char ReadInt8(void* ptr) {
        char value;
        static_cast<RakNet::BitStream*>(ptr)->Read(reinterpret_cast<char*>(&value), sizeof(value));
        return value;
    }

    __declspec(dllexport) short ReadInt16(void* ptr) {
        short value;
        static_cast<RakNet::BitStream*>(ptr)->Read(reinterpret_cast<char*>(&value), sizeof(value));
        return value;
    }

    __declspec(dllexport) int ReadInt32(void* ptr) {
        int value;
        static_cast<RakNet::BitStream*>(ptr)->Read(reinterpret_cast<char*>(&value), sizeof(value));
        return value;
    }

    __declspec(dllexport) bool ReadBool(void* ptr) {
        bool value;
        static_cast<RakNet::BitStream*>(ptr)->Read(reinterpret_cast<char*>(&value), sizeof(value));
        return value;
    }

    __declspec(dllexport) float ReadFloat(void* ptr) {
        float value;
        static_cast<RakNet::BitStream*>(ptr)->Read(reinterpret_cast<char*>(&value), sizeof(value));
        return value;
    }

    __declspec(dllexport) const char* ReadString(void* ptr, unsigned int len) {
        static std::vector<char> buffer(len + 1, '\0');  // +1 для завершающего нуля
        static_cast<RakNet::BitStream*>(ptr)->Read(buffer.data(), len);
        return buffer.data();
    }
}
