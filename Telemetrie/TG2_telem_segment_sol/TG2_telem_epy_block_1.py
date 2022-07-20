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

    carac = 0
    indexCarac = 0

    def __init__(self, thr=0.5):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=[np.float32],
            out_sig=[np.float32]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.thr = thr
        self.carac = 0
        self.indexCarac = 0

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        #print(input_items[0])
        for i in range(len(input_items[0])):
            if(input_items[0][i] > self.thr):
                #print("1",end="")
                output_items[0][i] = 1
                self.carac = self.carac + pow(2, self.indexCarac)
                self.indexCarac = self.indexCarac + 1
            elif(input_items[0][i] < -self.thr):
                #print("0",end="")
                output_items[0][i] = -1
                self.indexCarac = self.indexCarac + 1
            else:
                output_items[0][i] = 0
                self.carac = 0
                self.indexCarac = 0

            if(self.indexCarac >= 8):#end char
                #print("")
                if(int(self.carac) >= 48 and int(self.carac) <= 126):
                    print(chr(self.carac));
                #print(int(self.carac))
                self.carac = 0
                self.indexCarac = 0

        #print(input_items[0])
        #output_items[0][:] = input_items[0] * self.example_param
        return len(output_items[0])
