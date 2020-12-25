#!/usr/bin/python
import sys

DEBUG_PRINT = 0

###############################################################################
class Reception:
    f = open("test1.bin", "rb")
    base_axis = 0

    def __init__(self):
        print("init")

    ###########################################################################
    def lookForHeader(self):
        if DEBUG_PRINT: print("\n Getting header:")
        # packets structure:
        # 2 headers (with base_axis and checksum) + 4 photodiodes * 2 bytes

        if (self.readByte(True) & 0x90) != 0x80:
            print("HEADER 1 ERROR")

        if (self.readByte(    ) & 0xF0) != 0x80:
            print("HEADER 2 ERROR")

        #TODO: handle checksum

    ###########################################################################
    def readByte(self, save_base_axis = False):
        byte = self.f.read(1)
        byte = int("{0:b}".format(ord(byte)),2)  # convert from string
        if DEBUG_PRINT: print(format(byte, '08b'))

        if save_base_axis:
            self.base_axis = byte

        return byte

    ###########################################################################
    def parse_data(self):
        self.lookForHeader()

        base = (self.base_axis >> 6) & 1
        axis = (self.base_axis >> 5) & 1
        if DEBUG_PRINT: print("base, axis:", base, axis,
                              "\n\n Getting Centroids:")
        centroidNum = 4
        centroids = [0 for i in range(centroidNum)]
        for i in range(centroidNum):
            centroids[i] = self.decodeTime()
            if DEBUG_PRINT: print("=> centroids[", i, "] =", centroids[i])

        return base, axis, centroids


    ###############################################################################
    def decodeTime(self):
        rxh = self.readByte()        # MSB first
        rxl = self.readByte()        # LSB last
        time = (rxh << 8) + rxl     # reconstruct packets
        time <<= 2                  # (non-significant) lossy decompression
        time /= 16.                 # convert to us

        if (time >= 6777 or time < 1222):
            print(" >>> INVALID TIME:", str(time))
            time = 0

        return time


###############################################################################
# This is just for debug, or to use as example
if __name__ == "__main__":

    # create an object (it also does the initialization)
    rx = Reception()

    while True:
        # base = 0 or 1 (B or C)
        # axis = 0 or 1 (horizontal or vertical)
        # centroids = array of 4 floats in microseconds

        try:
            base, axis, centroids = rx.parse_data()

            if not DEBUG_PRINT:
                print( base, axis, centroids )

        except:
            print("END OF FILE")
            sys.exit()


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