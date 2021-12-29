import socket, struct, json

from enum import Enum

class MessageType(Enum):
    IDENTIFICATION = 'ID'
    ACKNOWLEDGEMENT = 'ACK'
    INFO = 'INFO'
    EXIT = 'EXT'

def get_own_ip():
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("192.168.1.1", 80))
        return s.getsockname()[0]


class Peer():
    def __init__(self, address, name:str):
        self.name = name
        self.address_pair= address
        self.ip = self.address_pair[0]

    def __str__(self):
        return f'ip: {self.ip}, Name: {self.name}'

    def compare(self, peer):
        return self.ip == peer.ip and self.name == peer.name
    

class Message():

    def __init__(self, data, address=None, encoding='UTF-8'):
        if type(data) == bytes:
            self.data = json.loads(data)
        elif type(data) == dict:
            self.data = data
        self.type = MessageType(self.data['type'])
        # if the address is not set, this message is being set by the peer creating it, otherwise it has been received externally
        if address is None:
            address = get_own_ip()
        # we create the peer of the sender, he's the source of the message
        self.sender = Peer(address, self.data['sender'])

        
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

    def __init__(self, name:str, peers=[], multicast_group=('224.3.29.71', 10000), listening_address=('0.0.0.0', 10000)):
        self.name = name
        self._peers = peers

        self.multicast_group = multicast_group
        self.listening_address = listening_address
        self._listening_state=False

    @property
    def peers(self):
        return self._peers
    
    @peers.setter
    def peers(self, value):
        print(f'New Peer List:')
        for peer in value:
            print(peer)
        self._peers = value
    
    def acknowledge(self, address, socket=None):
        Message({
            'sender': self.name,
            'type': MessageType.ACKNOWLEDGEMENT.value
        }).sendto(address, socket)

    def identification(self, socket=None):
        Message({
            'sender': self.name,
            'type': MessageType.IDENTIFICATION.value
        }).sendto(self.multicast_group, socket)
    
    # def received_message_handler(self, msg):
    #     pass

    def start(self, encoding='UTF-8'):        
        self.identification()

        import threading

        listening = threading.Thread(target=self.listen_routine)
        listening.start()

        listening.join()

        
    
    def stop(self):
        self._listening_state = False

    def check_peer(self, peer:Peer, add_if_absent=False, remove_if_found=False):
        # matched_peers = filter(lambda x: peer.compare(x), self.peers)
        matched_peers = [idx for idx, x in self.peers if peer.compare(x)]
                
        if len(matched_peers) == 0:
            # we don't have this peer
            if add_if_absent:
                print('Added peer ' + str(peer))
                self.peers.append(peer)
            return False
        
        if remove_if_found:
            for i in matched_peers:
                print('removing peer ' + str(self.peers[i]))
                del self.peers[i]

        return True
        

    def listen_routine(self):
        self._listening_state=True
        while self._listening_state:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Bind to the server address
            sock.bind(self.listening_address)
            # Tell the operating system to add the socket to the multicast group
            # on all interfaces.
            group = socket.inet_aton(self.multicast_group[0])
            mreq = struct.pack('4sL', group, socket.INADDR_ANY)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)


            print('\nwaiting to receive message')
            data, address = sock.recvfrom(1024)
            
            received_msg = Message(data, address)
            # if callback is not None and hasattr(callback, '__call__'):
            #     callback(received_msg)
            
            # if we receive an identification Message
            if received_msg.type == MessageType.IDENTIFICATION:
                # we check if the peer that send the message exists within our list
                print(f'received message: \n {received_msg}')
                self.check_peer(received_msg.sender, add_if_absent=True)
                # we reply with ackgnowledgement
                self.acknowledge(received_msg.sender.address_pair, socket=sock)

            if received_msg.type == MessageType.ACKNOWLEDGEMENT:
                self.check_peer(received_msg.sender, add_if_absent=True)
            
            if received_msg.type == MessageType.EXIT:
                self.check_peer(received_msg.sender,remove_if_found=True)
                
    

MulticastDiscovery('Adel PC').start()