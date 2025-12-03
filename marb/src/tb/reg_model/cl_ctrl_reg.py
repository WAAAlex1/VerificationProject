from pyuvm import *

class cl_ctrl_reg(uvm_reg):
    def __init__(self, name = "cl_ctrl_reg", reg_width = 32):
        super().__init__(name, reg_width)

        # Define the register fields
        self.F_en     = uvm_reg_field("en")
        self.F_mode   = uvm_reg_field("mode")
        self.F_unused = uvm_reg_field("unused")

    def build(self):
        # Configure (size, lsb_pos, access, is_volatile, reset)
        self.F_en.configure(self, 1, 0, "RW", 0, 0)
        # Configure (size, lsb_pos, access, is_volatile, reset)
        self.F_mode.configure(self, 2, 1, "RW", 0, 0)
        # Configure (size, lsb_pos, access, is_volatile, reset)
        self.F_unused.configure(self, 29, 3, "RW", 0, 0)

        self._set_lock()
        self.set_prediction(predict_t.PREDICT_DIRECT)