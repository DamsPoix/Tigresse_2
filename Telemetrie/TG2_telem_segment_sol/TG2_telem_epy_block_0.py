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

    def __init__(self, trigger=0.5):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Mange tes morts',   # will show up in GRC
            in_sig=[np.float32],
            out_sig=[np.float32]
            #out_sig=[void]
        )
        print("inited")
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.trigger = trigger

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        if(input_items[0] > self.trigger):
        	return 1
        else:
        	return 0

        #self.sampl_number = self.sampl_number + 1
        #return input_items[0]
