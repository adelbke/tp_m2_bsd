import socket, struct, json

from enum import Enum

class MessageType(Enum):
    IDENTIFICATION = 'ID'
    ACKNOWLEDGEMENT = 'ACK'
    INFO = 'INFO'
    EXIT = 'EXT'

class Message():

    def __init__(self, data, address=None, encoding='UTF-8'):
        # data_string = data.decode(encoding)
        if type(data) == bytes:
            self.data = json.loads(data)
        elif type(data) == dict:
            self.data = data
        self.type = MessageType(self.data['type'])
        self.sender = self.data['sender']
        if address is not None:
            self.sender_ip = address
    
    def __str__(self):
        return str(self.data)
    def sendto(self, address, sock=None, encoding='UTF-8'):
        if sock is None:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(300)
            ttl = struct.pack('b', 1)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
        encoded_data = json.dumps(self.data, indent=2).encode('UTF-8')
        sock.sendto(encoded_data, address)


class MulticastDiscovery():
    multicast_group = ('224.3.29.71', 10000)
    listening_address = ('0.0.0.0', 10000)

    received_messages = []
    peers = []

    @classmethod
    def start(cls, encoding='UTF-8'):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Receive/respond loop
        msg = Message({
            'sender': 'Adel',
            'type': MessageType.IDENTIFICATION.value,
            'content': 'Hello world'
        })
        msg.sendto(cls.multicast_group)
        
        # Bind to the server address
        sock.bind(cls.listening_address)
        # Tell the operating system to add the socket to the multicast group
        # on all interfaces.
        group = socket.inet_aton(cls.multicast_group[0])
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)


        print('\nwaiting to receive message')
        data, address = sock.recvfrom(1024)

        # print('received %s bytes from %s' % (len(data), address))
        print(f'received Data from {address}')
        cls.received_messages.append(Message(data,  address[0]))
        print(cls.received_messages[-1])
        # print(type(data))

        print('sending acknowledgement to', address)
        # sock.sendto(bytes('ack', encoding), address)
        msg = Message({
            'sender': 'Adel',
            'type': MessageType.ACKNOWLEDGEMENT.value,
            'content': 'Hello world'
        })
        msg.sendto(address, sock)

        

MulticastDiscovery.start()