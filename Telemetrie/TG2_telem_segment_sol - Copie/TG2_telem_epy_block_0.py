"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""
    indexSampling = 0
    q1 = [1,1,1,1,1,1,1,1,1,1,1]
    lastBit = 1

    def pileSlide(self, val):
        for i in range(10):
            self.q1[i] = self.q1[i+1]
        self.q1[10] = val

    def processPile(self):
        if(self.q1[0] == 0 and self.q1[9] == 1 and self.q1[10] == 1):#noice
            carac = 0
            for i in range(8):
                carac = carac + pow(2,i)*self.q1[i+1]
                self.q1[i+1] = 1
            self.q1[0] = 1
            self.q1[9] = 1
            self.q1[10] = 1
            if((int(carac) >= 32 and int(carac) <= 126) or int(carac) == 10):
                print(chr(carac), end="")

    def __init__(self, baudrate=9600, sampling=100000):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=[np.float32],
            out_sig=[np.float32]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.baudrate = baudrate
        self.sampling = sampling
        self.indexSampling = 0
        self.lastBit = 1
        for i in range(11):
            self.q1[i] = 1

    def work(self, input_items, output_items):
        for i in range(len(input_items[0])):
            bit = int(input_items[0][i])
            if(self.lastBit == 1 and bit == 0):#falling
                self.indexSampling = -1

            if((self.indexSampling%int(self.sampling/self.baudrate)) == int((self.sampling/self.baudrate)/2)): #on est au milieu d un bit
                self.pileSlide(bit)
                self.processPile()

            self.lastBit = bit
            self.indexSampling = self.indexSampling + 1


        output_items[0][:] = input_items[0]
        return len(output_items[0])