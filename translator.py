#!/usr/bin/python

class Reception:
    f = open("test1.bin", "rb")

    def __init__(self):
        print("init")
        self.f

    def lookForHeader(self):
        # packets structure:
        # 2 headers + 1 base_axis + 4 photodiodes*2 bytes
        while True:
            while int("{0:b}".format(ord(self.readByte())),2) != 255:
                pass # consume

            if int("{0:b}".format(ord(self.readByte())),2) != 255:
                continue

            break

    def readByte(self):
        byte = self.f.read(1)   # number of bytes read
        #print("###########\n")
        #print(byte)
        return byte

    def parse_data(self):
        centroidNum = 4

        base_axis = self.readByte()
        base_axis = int("{0:b}".format(ord(base_axis)),2) # convert hex to int
        
        print(base_axis)
        
        base = (base_axis >> 1) & 1
        axis = (base_axis >> 0) & 1

        print("\nbase, axis:", base, axis)

        centroids = [0 for i in range(centroidNum)]

        for i in range(centroidNum):
            centroids[i] = self.decodeTime()
            print("centroids[", i, "] =", centroids[i])

        # consumes header
        for i in range(2):
            b = int("{0:b}".format(ord(self.readByte())),2)
            if (b != 255):
                print("header problem", i)
                self.lookForHeader()
                break

        return base, axis, centroids

    def decodeTime(self):
        rxl = self.readByte()        # LSB first
        rxl = int("{0:b}".format(ord(rxl)),2)   # convert hex to int
        rxh = self.readByte()        # MSB last
        rxh = int("{0:b}".format(ord(rxh)),2)   # convert hex to int
        time = (rxh << 8) + rxl     # reconstruct packets
        time <<= 2                  # (non-significant) lossy decompression
        time /= 16.                 # convert to us

        if (time >= 6777 or time < 1222):
            time = 0
            print("INVALID TIME")

        return time


###############################################################################
# This is just for debug, or to use as example
if __name__ == "__main__":

    # create an object (it also does the port initialization)
    rx = Reception()

    #base_axis = rx.readByte()
    #print("\nbase, axis:", base_axis)
    while True:
        # base = 0 or 1 (B or C)
        # axis = 0 or 1 (horizontal or vertical)
        # centroids = array of 4 floats in microseconds
        # accelerations = array of 3 floats in G (AKA m/s^2)
        base, axis, centroids = rx.parse_data()


"""
with open("test1.bin", "rb") as f:
    g = open("toto1.txt", "wb")
    byte = f.read(1)
    while byte:
        # Do stuff with byte.
        byte = f.read(1)
        bin = "{0:b}".format(ord(byte)) # binary: 11111111
        print(bin)
        g.write(bin.encode('utf-8'))
        g.write('\n'.encode('utf-8'))

    g.close()
"""