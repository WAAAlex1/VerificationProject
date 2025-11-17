from pyuvm import *

from uvc.sdt.src import *

from cl_marb_tb_virtual_sequencer import cl_marb_tb_virtual_sequencer

from reg_model.cl_reg_block import cl_reg_block

from uvc.apb.src.cl_apb_agent import cl_apb_agent
from uvc.apb.src.cl_apb_reg_adapter import cl_apb_reg_adapter

class cl_marb_tb_env(uvm_env):
    def __init__(self, name, parent):
        super().__init__(name, parent)

        # Configuration object handle
        self.cfg = None

        # Virtual sequencer
        self.virtual_sequencer = None

        # Register model
        self.reg_model = None


        self.apb_agent = None

    def build_phase(self):
        self.logger.info("Start build_phase() -> MARB env")
        super().build_phase()

        # Get the configuration object
        self.cfg = ConfigDB().get(self, "", "cfg")

        # Create virtual_sequencer and pass handler to cfg
        ConfigDB().set(self, "virtual_sequencer", "cfg", self.cfg)
        self.virtual_sequencer = cl_marb_tb_virtual_sequencer.create("virtual_sequencer", self)


        # Instantiate the APB UVC and pass handler to cfg
        ConfigDB().set(self, "apb_agent", "cfg", self.cfg.apb_cfg)
        self.apb_agent = cl_apb_agent("apb_agent", self)

        self.reg_model = cl_reg_block()
        self.adapter   = cl_apb_reg_adapter()

        # Set register model in virtual sequencer
        self.virtual_sequencer.reg_model = self.reg_model

        self.logger.info("End build_phase() -> MARB env")

    def connect_phase(self):
        self.logger.info("Start connect_phase() -> MARB env")
        super().connect_phase()


        # Connect reg_model and APB sequencer
        self.reg_model.bus_map.set_sequencer(self.apb_agent.sequencer)
        self.reg_model.bus_map.set_adapter(self.adapter)

        self.logger.info("End connect_phase() -> MARB env")
