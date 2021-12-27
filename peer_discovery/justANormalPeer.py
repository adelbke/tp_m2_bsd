import socket
import struct
import sys
# import time
# import threading


def join(message):

    multicast_group = ('224.3.29.71', 10000)

    # Create the datagram socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set a timeout so the socket does not block indefinitely when trying
    # to receive data.
    sock.settimeout(300)

    # Set the time-to-live for messages to 1 so they do not go past the
    # local network segment.
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    # try:

        # Send data to the multicast group
    print(sys.stderr, 'sending "%s"' % message)
    sent = sock.sendto(bytes(message, 'UTF-8'), multicast_group)

        # Look for responses from all recipients

    #     print('waiting to receive')
    #     try:
    #         data, server = sock.recvfrom(1024)
    #     except socket.timeout:
    #         print('timed out, no more responses')
    #     else:
    #         print('received "%s" from %s' % (data, server))

    # finally:
    #     print('closing socket')
    #     sock.close()


def Listen_and_say_welcome():
    hostname = socket. gethostname()
    local_ip = socket. gethostbyname(hostname)

    multicast_group = '224.3.29.71'
    server_address = ('0.0.0.0', 10000)

    # Create the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind to the server address
    sock.bind(server_address)

    # Tell the operating system to add the socket to the multicast group
    # on all interfaces.
    group = socket.inet_aton(multicast_group)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    # Receive/respond loop

    print('\nwaiting to receive message')
    data, address = sock.recvfrom(1024)

    print('received %s bytes from %s' % (len(data), address))
    print(data)

    print('sending acknowledgement to', address)
    sock.sendto(bytes('ack', 'UTF-8'), address)


message = 'hi guys im new here'
# thread_generator(1, join, message)
join(message)
# while (1):
Listen_and_say_welcome()
