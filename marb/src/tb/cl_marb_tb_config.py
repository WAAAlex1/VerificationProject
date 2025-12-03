from pyuvm import *

from uvc.sdt.src.cl_sdt_config import *
from uvc.apb.src.cl_apb_config import *

from uvc.sdt.src.cl_sdt_interface import cl_sdt_interface
from uvc.sdt.src.sdt_common import DriverType, SequenceItemOverride

class cl_marb_tb_config(uvm_object):
    def __init__(self, name = "cl_marb_tb_config"):
        super().__init__(name)

        # CONFIGS
        self.apb_cfg            = cl_apb_config.create("apb_cfg")
        self.sdt_client0_cfg    = cl_sdt_config.create("sdt_client0_cfg")
        self.sdt_client1_cfg    = cl_sdt_config.create("sdt_client1_cfg")
        self.sdt_client2_cfg    = cl_sdt_config.create("sdt_client2_cfg")
        self.sdt_mem_cfg        = cl_sdt_config.create("sdt_mem_cfg")

        #  DUT REFERENCE
        self.dut = None

        # SDT CONFIGS
        # SDT CLIENT 0 agent configuration
        self.sdt_client0_cfg.is_active                      = uvm_active_passive_enum.UVM_ACTIVE
        self.sdt_client0_cfg.num_consumer_seq               = None
        self.sdt_client0_cfg.driver                         = DriverType.PRODUCER
        self.sdt_client0_cfg.seq_item_override              = SequenceItemOverride.DEFAULT
        self.sdt_client0_cfg.enable_transaction_coverage    = True
        self.sdt_client0_cfg.enable_delay_coverage          = True
        self.sdt_client0_cfg.no_ack_value                   = 'X'
        #self.sdt_client0_cfg.ADDR_WIDTH                     = self.ADDR_WIDTH
        #self.sdt_client0_cfg.DATA_WIDTH                     = self.DATA_WIDTH

        # SDT CLIENT 1 agent configuration
        self.sdt_client1_cfg.is_active                      = uvm_active_passive_enum.UVM_ACTIVE
        self.sdt_client1_cfg.num_consumer_seq               = None
        self.sdt_client1_cfg.driver                         = DriverType.PRODUCER
        self.sdt_client1_cfg.seq_item_override              = SequenceItemOverride.DEFAULT
        self.sdt_client1_cfg.enable_transaction_coverage    = True
        self.sdt_client1_cfg.enable_delay_coverage          = True
        self.sdt_client1_cfg.no_ack_value                   = 'X'
        #self.sdt_client1_cfg.ADDR_WIDTH                     = self.ADDR_WIDTH
        #self.sdt_client1_cfg.DATA_WIDTH                     = self.DATA_WIDTH

        # SDT CLIENT 2 agent configuration
        self.sdt_client2_cfg.is_active                      = uvm_active_passive_enum.UVM_ACTIVE
        self.sdt_client2_cfg.num_consumer_seq               = None
        self.sdt_client2_cfg.driver                         = DriverType.PRODUCER
        self.sdt_client2_cfg.seq_item_override              = SequenceItemOverride.DEFAULT
        self.sdt_client2_cfg.enable_transaction_coverage    = True
        self.sdt_client2_cfg.enable_delay_coverage          = True
        self.sdt_client2_cfg.no_ack_value                   = 'X'
        #self.sdt_client2_cfg.ADDR_WIDTH                    = self.ADDR_WIDTH
        #self.sdt_client2_cfg.DATA_WIDTH                    = self.DATA_WIDTH

        # SDT MEM agent configuration
        self.sdt_mem_cfg.is_active                      = uvm_active_passive_enum.UVM_ACTIVE
        self.sdt_mem_cfg.num_consumer_seq               = None
        self.sdt_mem_cfg.driver                         = DriverType.CONSUMER
        self.sdt_mem_cfg.seq_item_override              = SequenceItemOverride.DEFAULT
        self.sdt_mem_cfg.enable_transaction_coverage    = True
        self.sdt_mem_cfg.enable_delay_coverage          = True
        self.sdt_mem_cfg.no_ack_value                   = 'X'
        #self.sdt_mem_cfg.ADDR_WIDTH                    = self.ADDR_WIDTH
        #self.sdt_mem_cfg.DATA_WIDTH                    = self.DATA_WIDTH


