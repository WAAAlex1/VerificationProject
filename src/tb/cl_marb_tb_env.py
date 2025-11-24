from pyuvm import *

from uvc.sdt.src import *

from cl_marb_tb_virtual_sequencer import cl_marb_tb_virtual_sequencer

from reg_model.cl_reg_block import cl_reg_block

from uvc.apb.src.cl_apb_agent import cl_apb_agent
from uvc.sdt.src.cl_sdt_agent import cl_sdt_agent
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

        # APB agent
        self.apb_agent = None

        # SDT agents
        self.sdt_client0_agent = None
        self.sdt_client1_agent = None
        self.sdt_client2_agent = None
        self.sdt_mem_agent     = None

    def build_phase(self):
        self.logger.info("Start build_phase() -> MARB env")
        super().build_phase()

        # Get the configuration object
        self.cfg = ConfigDB().get(self, "", "cfg")

        # Create virtual_sequencer and pass handler to cfg
        ConfigDB().set(self, "virtual_sequencer", "cfg", self.cfg)
        self.virtual_sequencer = cl_marb_tb_virtual_sequencer.create("virtual_sequencer", self)

        #########################################
        # APB #
        #########################################

        # Instantiate the APB UVC and pass handler to cfg
        ConfigDB().set(self, "apb_agent", "cfg", self.cfg.apb_cfg)
        self.apb_agent = cl_apb_agent("apb_agent", self)

        ##############################################
        # SDT #
        ###############################################

        # Instantiate the SDT UVCs and pass handler to cfg
        ConfigDB().set(self, "sdt_client0_agent", "cfg", self.cfg.sdt_client0_agent)
        self.sdt_client0_agent = cl_sdt_agent("sdt_client0_agent", self)
        ConfigDB().set(self, "sdt_client1_agent", "cfg", self.cfg.sdt_client1_agent)
        self.sdt_client1_agent = cl_sdt_agent("sdt_client1_agent", self)
        ConfigDB().set(self, "sdt_client2_agent", "cfg", self.cfg.sdt_client2_agent)
        self.sdt_client2_agent = cl_sdt_agent("sdt_client2_agent", self)
        ConfigDB().set(self, "sdt_mem_agent", "cfg", self.cfg.sdt_mem_agent)
        self.sdt_client0_agent = cl_sdt_agent("sdt_mem_agent", self)

        self.virtual_sequencer.sdt_client0 = self.sdt_client0_agent
        self.virtual_sequencer.sdt_client1 = self.sdt_client1_agent
        self.virtual_sequencer.sdt_client2 = self.sdt_client2_agent
        self.virtual_sequencer.sdt_mem     = self.sdt_mem_agent

        # TODO: Add sdt connections to scoreboard and reference model

        #########################################################
        #  REG MODEL
        ############################################################

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
