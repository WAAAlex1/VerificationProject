from pyuvm import *
from .cl_ctrl_reg import cl_ctrl_reg
from .cl_dprio_reg import cl_dprio_reg
from .cl_reg_predictor import cl_reg_predictor
from .cl_uvm_reg_map_always_predict import uvm_reg_map_always_predict

class cl_reg_block(uvm_reg_block):
    def __init__(self, name = "cl_reg_block"):
        super().__init__(name)

        # Define and configure the map
        self.bus_map = uvm_reg_map_always_predict("bus_map")
        self.bus_map.configure(self, 0)
        predictor = cl_reg_predictor("marb_reg_predictor")
        predictor.configure(self.bus_map)
        self.bus_map.set_predictor(predictor)

        # Define and configure the register
        self.ctrl_reg = cl_ctrl_reg("ctrl_reg")
        self.ctrl_reg.configure(self, "0x0", "", False, False)
        self.bus_map.add_reg(self.ctrl_reg, "0X0", "RW")

        # Define and configure the register
        self.dprio_reg = cl_dprio_reg("dprio_reg")
        self.dprio_reg.configure(self, "0x4", "", False, False)
        self.bus_map.add_reg(self.dprio_reg, "0x0", "RW")
