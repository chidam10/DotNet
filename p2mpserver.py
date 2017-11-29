from socket import *
import os.path
import threading
import glob
import random
import sys
from threading import Thread


def carry_around_add(a, b):
    c = a + b
    return (c & 0xffff) + (c >> 16)

def checksum(msg):
    if (len(msg) % 2) != 0:
        msg += "0"

    s = 0
    for i in range(0, len(msg), 2):
        w = ord(msg[i]) + (ord(msg[i + 1]) << 8)
        s = carry_around_add(s, w)
    return ~s & 0xffff


def check(message):
    data = message[64:]
    to_check = checksum(data)
    while len(str(to_check))!=16:
        to_check = '0' + str(to_check)
    #print 'The local checksum value is: ' + to_check
    if to_check == message[32:48]:
        return 1
    else:
        return 0




if __name__ == '__main__':
    
    serverport = int(sys.argv[1])
    name = sys.argv[2]
    p = float(sys.argv[3])
    serversocket = socket(AF_INET, SOCK_DGRAM)
    serversocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serversocket.bind(('', serverport))
    print 'The server is ready to receive'
    seq = 0
    seg = 0
    while 1:
        message, clientAddress = serversocket.recvfrom(2048)
        q = random.uniform(0, 1)
        #print q
        #print message[0:32] + '\n'
        #print message[32:48] + '\n'
        #print message[48:64] + '\n'
        seq_recv = message[0:32]
        if q > float(p):
            if message[48:64]=='0101010101010101':
                if seq == int(seq_recv, 2):
                    checking_sum = check(message)
                    if checking_sum == 1:
                        with open(name, 'a+b') as f:
                            f.write(message[64:])
                            f.close()
                        serversocket.sendto('ack', clientAddress)
                        #print 'Ack sent for : ' + str(seq)
                        seq += 1
                elif int(seq_recv, 2) < seq:
                    serversocket.sendto('ack', clientAddress)
                    #print 'Ack sent for : ' + str(int(seq_recv, 2))

                    continue
        else:
            seg+=1
            #print'segment skipped: ' + str(seg)
            print 'Packet Loss, Sequence: ' + str(seq_recv)


