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
    indexSampling = 0
    indexUART = 0
    lastBit = 1

    def __init__(self, baudrate=9600, sampling=100000, percentReading=50):  # only default arguments here
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
        self.percentReading = percentReading
        self.lastBit = 1
        self.indexSampling = 0
        self.indexUART = 0
        self.carac = 0

    def work(self, input_items, output_items):
        for i in range(len(input_items[0])):

            if(self.indexUART > 0):
                nbrSampleSeuil = int(self.sampling/self.baudrate)
                if(self.indexSampling == nbrSampleSeuil*(1+2*self.indexUART)): #on lit le bit mid trame
                    if(self.indexUART < 9):
                        #print(int(input_items[0][i]),end="")
                        self.carac = self.carac + (pow(2, self.indexUART-1)*int(input_items[0][i]))
                        self.indexUART = self.indexUART + 1
                    elif((self.indexUART == 9 and input_items[0][i] == 1) or (self.indexUART == 10 and input_items[0][i] == 0)): #on check la parite qui doit etre a zero, et le bit de stop
                        self.carac = 0
                        self.indexSampling = -1
                        self.indexUART = 0
                        #print("")
                    elif(self.indexUART == 10 and input_items[0][i] == 1): #bit de stop et stame aquise correctement (enfin presque)
                        if(self.carac >= 97 and self.carac <= 122):
                            print(chr(self.carac))
                        self.carac = 0
                        self.indexSampling = -1
                        self.indexUART = 0
                        #print("")
                    else:
                        self.indexUART = self.indexUART + 1
                self.indexSampling = self.indexSampling + 1

            if(self.lastBit == 1 and input_items[0][i] == 0):#falling
                if(self.indexUART == 0 and self.indexSampling == 0): #bit de start maybe
                    #print("start : ", end="")
                    self.indexUART = 1
                    self.indexSampling = self.indexSampling + 1



            self.lastBit = input_items[0][i]
            output_items[0][i] = input_items[0][i]

            """
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
                self.indexCarac = 0"""

        #print(input_items[0])
        #output_items[0][:] = input_items[0] * self.example_param
        return len(output_items[0])
