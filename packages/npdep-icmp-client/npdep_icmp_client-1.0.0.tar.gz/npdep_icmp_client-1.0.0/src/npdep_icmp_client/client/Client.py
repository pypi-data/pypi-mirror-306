import socket

class Client():
    def __init__(self, ip, port = 0) -> None:
        self.ip = ip
        self.port = port

    '''
    https://www.rfc-editor.org/rfc/rfc792
    ---
    Echo or Echo Reply Message
    ---
     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |     Type      |     Code      |          Checksum             |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |           Identifier          |        Sequence Number        |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    | Data...
    +-+-+~~~~~~
    '''
    def sendEchoMessage(self, echoMsgType, data, identifier = 1, seqNr = 0):
        s = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_ICMP)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, 64)
        s.settimeout(2)

        # The initial payload with checksum 0
        payload = self.__createEchoPayload(echoMsgType, identifier, seqNr, 0, data)

        # Calc checksum
        checksum = self.__calcChecksum(payload)

        # The payload with calculated checksum
        payload = self.__createEchoPayload(echoMsgType, identifier, seqNr, checksum, data)

        # Send the packet
        s.sendto(payload, (self.ip, self.port))


    def __calcChecksum(self, data):
        checksum = 0
        
        if len(data) % 2 != 0:
            data += b"\x00"

        for i in range(0, len(data) - 1, 2):
            checksum += (data[i] << 8) + data[i + 1]
            checksum  = (checksum & 0xffff) + (checksum >> 16)

        checksum = (~checksum) & 0xffff

        return checksum
    
    def __createEchoPayload(self, echoMsgType, identifier, seqNr, checksum, data):
        # The ICMP payload
        payload = bytearray(0)
        
        # Set type to echo request
        type_ = echoMsgType
        payload.extend(type_.to_bytes(1, "big"))

        # Code is always zero
        code = 0
        payload.extend(code.to_bytes(1, "big"))

        # Checksum
        payload.extend(checksum.to_bytes(2, "big"))

        # Identifier
        payload.extend(identifier.to_bytes(2, "big"))

        # Sequence Number
        payload.extend(seqNr.to_bytes(2, "big"))

        # Data to be transported via ICMP echo
        if(type(data) == str):
            data_ = data.encode(encoding="utf-8")
        elif(type(data) == int):
            data_ = data.to_bytes()
        else:
            data_ = data

        payload.extend(data_)
        
        return payload