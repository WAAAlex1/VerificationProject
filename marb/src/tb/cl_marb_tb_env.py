from pyuvm import *
from pyuvm import uvm_env

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

        ###############################################
        # SDT #
        ###############################################

        # Instantiate the SDT UVCs and pass handler to cfg
        self.sdt_client0_agent  = cl_sdt_agent.create("sdt_client0_agent", self)
        self.sdt_client1_agent  = cl_sdt_agent.create("sdt_client1_agent", self)
        self.sdt_client2_agent  = cl_sdt_agent.create("sdt_client2_agent", self)
        self.sdt_mem_agent      = cl_sdt_agent.create("sdt_mem_agent", self)

        ConfigDB().set(self, "sdt_client0_agent", "cfg", self.cfg.sdt_client0_cfg)
        ConfigDB().set(self, "sdt_client1_agent", "cfg", self.cfg.sdt_client1_cfg)
        ConfigDB().set(self, "sdt_client2_agent", "cfg", self.cfg.sdt_client2_cfg)
        ConfigDB().set(self, "sdt_mem_agent", "cfg", self.cfg.sdt_mem_cfg)

        # TODO: Add sdt connections to scoreboard and reference model

        #########################################################
        #  REG MODEL
        ############################################################

        self.reg_model = cl_reg_block()                     #Create reg model
        self.adapter   = cl_apb_reg_adapter()               #Create apb adapter
        self.virtual_sequencer.reg_model = self.reg_model   #Give to virtual sequencer

        self.logger.info("End build_phase() -> MARB env")

    def connect_phase(self):
        self.logger.info("Start connect_phase() -> MARB env")
        super().connect_phase()

        self.virtual_sequencer.sdt_client0_sequencer    = self.sdt_client0_agent.sequencer
        self.virtual_sequencer.sdt_client1_sequencer    = self.sdt_client1_agent.sequencer
        self.virtual_sequencer.sdt_client2_sequencer    = self.sdt_client2_agent.sequencer
        self.virtual_sequencer.sdt_mem_sequencer        = self.sdt_mem_agent.sequencer

        # Connect reg_model and APB sequencer
        self.reg_model.bus_map.set_sequencer(self.apb_agent.sequencer)
        self.reg_model.bus_map.set_adapter(self.adapter)

        self.logger.info("End connect_phase() -> MARB env")
