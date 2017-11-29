from socket import *
import socket
import os.path
import sys
import threading
import glob
import time
row = 0
w, h = 3, 6
myArray = [[None for x in range(w)] for y in range(h)]
retran = [0]
total_time = 0


with open('Peer Servers.txt', 'w') as fi:
    if len(sys.argv)==5:
        to_write = str(sys.argv[1]) + '\t' + str(sys.argv[2] + '\n')
        name = sys.argv[3]
        mss = int(sys.argv[4])
        fi.write(to_write)
    elif len(sys.argv)==6:
        to_write = str(sys.argv[1]) + '\t' + str(sys.argv[3]) + '\n' + str(sys.argv[2]) + '\t' + str(sys.argv[3]) + '\n'
        name = sys.argv[4]
        mss = int(sys.argv[5])
        fi.write(to_write)
    elif len(sys.argv)==7:
        to_write = str(sys.argv[1]) + '\t' + str(sys.argv[4]) + '\n' + str(sys.argv[2]) + '\t' + str(sys.argv[4]) + '\n'+ str(sys.argv[3]) + '\t' + str(sys.argv[4]) + '\n'
        name = sys.argv[5]
        mss = int(sys.argv[6])
        fi.write(to_write)
    elif len(sys.argv)==8:
        to_write = str(sys.argv[1]) + '\t' + str(sys.argv[5]) + '\n' + str(sys.argv[2]) + '\t' + str(sys.argv[5]) + '\n'+ str(sys.argv[3]) + '\t' + str(sys.argv[5]) + '\n' + str(sys.argv[4]) + '\t' + str(sys.argv[5]) + '\n'
        name = sys.argv[6]
        mss = int(sys.argv[7])
        fi.write(to_write)
    elif len(sys.argv)==9:
        to_write = str(sys.argv[1]) + '\t' + str(sys.argv[6]) + '\n' + str(sys.argv[2]) + '\t' + str(sys.argv[6]) + '\n'+ str(sys.argv[3]) + '\t' + str(sys.argv[6]) + '\n' + str(sys.argv[4]) + '\t' + str(sys.argv[6]) + '\n' + str(sys.argv[5]) + '\t' + str(sys.argv[6]) + '\n'
        name = sys.argv[7]
        mss = int(sys.argv[8])
        fi.write(to_write)


with open('Peer Servers.txt', 'r') as f:
    i = f.readlines()
    print i

    for line in i:
        if line != "\n":
            #print "line" + line
            tup = line.split('\t')
            peerName = tup[0]
            serverPort = tup[1]
            myArray[row][0] = peerName
            myArray[row][1] = serverPort
            myArray[row][2] = 0
            row += 1
    f.close()

count = [row]



def rdt_send():
    sk = 1  # for seeking the file
    seq = -1
    while 1:
        count[0] = row
        for i in range(h):
            if myArray[i][0] is not None:
                myArray[i][2] = 0

        with open(name, 'rb') as fi:
            fi.seek(sk)
            data = fi.read(mss)
            sk = sk + mss
            fi.close()
        seq += 1
        #print 'Sending seq No. : ' + str(seq)
        if data != '':
            packet = make_packet(data, seq)
            for i in range(h):
                if myArray[i][0] is not None:
                    thread = threading.Thread(target=stop_and_wait, args=(myArray[i][0], myArray[i][1], packet))
                    thread.daemon = True
                    thread.start()
            con = True
            while con:
                check = 0
                for i in range(h):
                    if myArray[i][0] is not None:
                        if myArray[i][2] == 1:
                            check += 1
                if check == row:
                    con = False
        else:

            with open('client_time.txt', 'a+') as f:
                f.write(str(total_time) + '\n')
                f.close()
            print'Total retransmission are:' + str(retran[0])
            return

def make_packet(data, seq):
    check_sum = checksum(data)
    seq_to = bin(seq)
    seq_to = seq_to.lstrip('0b')
    while len(seq_to) != 32:
        seq_to = '0' + seq_to

    while len(str(check_sum))!=16:
        check_sum = '0' + str(check_sum)

    packet = str(seq_to) + str(check_sum) + '0101010101010101' + data

    return packet



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


def stop_and_wait(pname, pport, data):
    global total_time
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    time_start = time.time()
    ack2 = True
    while ack2:    
        client.sendto(data, (pname, int(pport)))
        ack1 = True
        while ack1:
            try:
                client.settimeout(0.06)
                ack, address = client.recvfrom(1024)
                time_end = time.time()
                time_diff = time_end - time_start
                total_time += time_diff
                if ack:
                    ack1 = False

                    ack2 = False
                    count[0] -= 1
                    for k in range(h):
                        if myArray[k][0] == pname:
                            if myArray[k][1] == pport:
                                myArray[k][2] = 1
            except socket.timeout:
                print 'Timeout, Sequence = ' + data[0:32]
		#client.settimeout(None)
                retran[0] += 1
                ack1 = False


if __name__ == '__main__':

    rdt_send()
    print 'Finished the file transfer'
