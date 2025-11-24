from pyuvm import *

from uvc.sdt.src.cl_sdt_config import *
from uvc.apb.src.cl_apb_config import *

class cl_marb_tb_config(uvm_object):
    def __init__(self, name = "cl_marb_tb_config"):
        super().__init__(name)

        self.apb_cfg            = cl_apb_config.create("apb_cfg")
        self.sdt_client0_cfg    = cl_sdt_config.create("sdt_client0_cfg")
        self.sdt_client1_cfg    = cl_sdt_config.create("sdt_client1_cfg")
        self.sdt_client2_cfg    = cl_sdt_config.create("sdt_client2_cfg")
        self.sdt_mem_cfg        = cl_sdt_config.create("sdt_mem_cfg")
