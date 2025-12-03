import pyuvm

from cocotb.clock import Clock

import os, warnings

from uvc.sdt.src import *
from uvc.sdt.src.sdt_if_assertions import * #Need this for some reason
from uvc.apb.src import *

from cl_marb_tb_config import cl_marb_tb_config
from cl_marb_tb_env import cl_marb_tb_env

_LOG_LEVELS = ["DEBUG", "CRITICAL", "ERROR", "WARNING", "INFO", "NOTSET", "NullHandler"]

@pyuvm.test()
class cl_marb_tb_base_test(uvm_test):
    def __init__(self, name = "cl_marb_tb_base_test", parent = None):
        # ----------------------------------------------------------------------
        if os.getenv("PYUVM_LOG_LEVEL") in _LOG_LEVELS:
            _PYUVM_LOG_LEVEL = os.getenv('PYUVM_LOG_LEVEL')
        else:
            _PYUVM_LOG_LEVEL = "INFO"
            if os.getenv("PYUVM_LOG_LEVEL") != None:
                uvm_root().logger.warning(F"{'='*50}\n   Wrong value for 'PYUVM_LOG_LEVEL' in Makefile. Changing to default value: 'INFO'.\n    {'='*50}")

        uvm_report_object.set_default_logging_level(_PYUVM_LOG_LEVEL)
        # ----------------------------------------------------------------------

        super().__init__(name, parent)

        # Access the DUT through the cocotb.top handler
        self.dut = cocotb.top

        # APB configuration interface
        self.apb_if = None

        #SSDT assertion checkers:
        self.assert_check_sdt_client0 = None
        self.assert_check_sdt_client1 = None
        self.assert_check_sdt_client2 = None
        self.assert_check_sdt_mem     = None

        # Configuration object handler
        self.cfg = None

        # TB environment handler
        self.marb_tb_env = None

        # Quick fix because of warnings og PYVSC
        warnings.simplefilter("ignore")

    def build_phase(self):
        self.logger.info("Start build_phase() -> MARB base test")
        super().build_phase()

        # Create configuration object
        self.cfg = cl_marb_tb_config("cfg")

        # Connect dut and config
        self.cfg.dut = self.dut

        # ------------------------------------------------------------------------------
        # APB
        # ------------------------------------------------------------------------------
        # APB agent configuration
        self.cfg.apb_cfg.driver                      = apb_common.DriverType.PRODUCER
        self.cfg.apb_cfg.seq_item_override           = apb_common.SequenceItemOverride.USER_DEFINED
        self.cfg.apb_cfg.create_default_coverage     = False
        self.cfg.apb_cfg.enable_masked_data          = False
        self.cfg.apb_cfg.active_low_reset            = False

        # Set ADDR and DATA width for APB interface
        self.cfg.apb_cfg.ADDR_WIDTH  = 32
        self.cfg.apb_cfg.DATA_WIDTH  = 32
        self.cfg.apb_cfg.STRB_WIDTH  = self.cfg.apb_cfg.DATA_WIDTH // 8

        # Set enable_masked_data as false for register access
        self.cfg.apb_cfg.enable_masked_data = False

        # Set interfaces in apb
        self.apb_if       = cl_apb_interface(self.dut.clk, self.dut.rst)

        # Set interfaces in cfg
        self.cfg.apb_cfg.vif           = self.apb_if
        self.apb_if._set_width_parameters(self.cfg.apb_cfg.ADDR_WIDTH, self.cfg.apb_cfg.DATA_WIDTH)

        # Assertions checkers
        self.assert_check_apb = if_apb_assert_check(clk_signal  = self.dut.clk,
                                                    rst_signal  = self.dut.rst)
        self.assert_check_apb.cfg = self.cfg.apb_cfg

        # TODO: Update the interfaces assertions WIDTHs and rd_data val when no ACK

        # ------------------------------------------------------------------------------
        # SDT
        # ------------------------------------------------------------------------------

        self.cfg.sdt_client0_cfg.vif = cl_sdt_interface(self.dut.clk, self.dut.rst, "sdt_client0_vif")
        self.cfg.sdt_client1_cfg.vif =  cl_sdt_interface(self.dut.clk, self.dut.rst, "sdt_client1_vif")
        self.cfg.sdt_client2_cfg.vif = cl_sdt_interface(self.dut.clk, self.dut.rst, "sdt_client2_vif")
        self.cfg.sdt_mem_cfg.vif = cl_sdt_interface(self.dut.clk, self.dut.rst, "sdt_mem_vif")

        self.cfg.sdt_client0_cfg.DATA_WIDTH = self.dut.DATA_WIDTH.value
        self.cfg.sdt_client0_cfg.ADDR_WIDTH = self.dut.ADDR_WIDTH.value
        self.cfg.sdt_client1_cfg.DATA_WIDTH = self.dut.DATA_WIDTH.value
        self.cfg.sdt_client1_cfg.ADDR_WIDTH = self.dut.ADDR_WIDTH.value
        self.cfg.sdt_client2_cfg.DATA_WIDTH = self.dut.DATA_WIDTH.value
        self.cfg.sdt_client2_cfg.ADDR_WIDTH = self.dut.ADDR_WIDTH.value
        self.cfg.sdt_mem_cfg.DATA_WIDTH     = self.dut.DATA_WIDTH.value
        self.cfg.sdt_mem_cfg.ADDR_WIDTH     = self.dut.ADDR_WIDTH.value


        # TODO: Implement assert checkers such that this works

        self.assert_check_sdt_client0 = sdt_if_assertions(clk_signal     = self.dut.clk,
                                                          rst_signal     = self.dut.rst,
                                                          wr_signal      = self.dut.c0_wr,
                                                          wr_data_signal = self.dut.c0_wr_data,
                                                          rd_signal      = self.dut.c0_rd,
                                                          rd_data_signal = self.dut.c0_rd_data,
                                                          addr_signal    = self.dut.c0_addr,
                                                          ack_signal     = self.dut.c0_ack,
                                                          name           = "ssdt_if_assertion_c0"
                                                          )
        self.assert_check_sdt_client0.set_width_values(self.cfg.sdt_client0_cfg.DATA_WIDTH)

        self.assert_check_sdt_client1 = sdt_if_assertions(clk_signal=self.dut.clk,
                                                          rst_signal=self.dut.rst,
                                                          wr_signal=self.dut.c1_wr,
                                                          wr_data_signal=self.dut.c1_wr_data,
                                                          rd_signal=self.dut.c1_rd,
                                                          rd_data_signal=self.dut.c1_rd_data,
                                                          addr_signal=self.dut.c1_addr,
                                                          ack_signal=self.dut.c1_ack,
                                                          name="ssdt_if_assertion_c1"
                                                          )
        self.assert_check_sdt_client1.set_width_values(self.cfg.sdt_client1_cfg.DATA_WIDTH)

        self.assert_check_sdt_client2 = sdt_if_assertions(clk_signal=self.dut.clk,
                                                          rst_signal=self.dut.rst,
                                                          wr_signal=self.dut.c2_wr,
                                                          wr_data_signal=self.dut.c2_wr_data,
                                                          rd_signal=self.dut.c2_rd,
                                                          rd_data_signal=self.dut.c2_rd_data,
                                                          addr_signal=self.dut.c2_addr,
                                                          ack_signal=self.dut.c2_ack,
                                                          name="ssdt_if_assertion_c2"
                                                          )
        self.assert_check_sdt_client2.set_width_values(self.cfg.sdt_client2_cfg.DATA_WIDTH)

        self.assert_check_sdt_mem = sdt_if_assertions(clk_signal=self.dut.clk,
                                                          rst_signal=self.dut.rst,
                                                          wr_signal=self.dut.m_wr,
                                                          wr_data_signal=self.dut.m_wr_data,
                                                          rd_signal=self.dut.m_rd,
                                                          rd_data_signal=self.dut.m_rd_data,
                                                          addr_signal=self.dut.m_addr,
                                                          ack_signal=self.dut.m_ack,
                                                          name="ssdt_if_assertion_m"
                                                          )
        self.assert_check_sdt_mem.set_width_values(self.cfg.sdt_mem_cfg.DATA_WIDTH)

        # ------------------------------------------------------------------------------
        # ENVIRONMENT
        # ------------------------------------------------------------------------------

        # Instantiate environment
        ConfigDB().set(self, "marb_tb_env", "cfg", self.cfg)
        self.marb_tb_env = cl_marb_tb_env("marb_tb_env", self)

       # TODO: If width issues _>  uvm_factory().set_type_override_by_type(cl_sdt_seq_item, sdt_change_width(8,8))


        self.logger.info("End build_phase() -> MARB base test")

    def connect_phase(self):
        self.logger.info("Start connect_phase() -> MARB base test")
        super().connect_phase()

        # ------------------------------------------------------------------------------
        # APB
        # ------------------------------------------------------------------------------

        self.apb_if.connect(wr_signal            = self.dut.conf_wr,
                            sel_signal           = self.dut.conf_sel,
                            enable_signal        = self.dut.conf_enable,
                            addr_signal          = self.dut.conf_addr,
                            wdata_signal         = self.dut.conf_wdata,
                            strb_signal          = self.dut.conf_strb,
                            rdata_signal         = self.dut.conf_rdata,
                            ready_signal         = self.dut.conf_ready,
                            slverr_signal        = self.dut.conf_slverr)

        self.assert_check_apb.connect()

        # ------------------------------------------------------------------------------
        # SDT
        # ------------------------------------------------------------------------------

        self.cfg.sdt_client0_cfg.vif._set_width_values(ADDR_WIDTH = self.cfg.dut.ADDR_WIDTH,
                                                       DATA_WIDTH = self.cfg.dut.DATA_WIDTH)

        self.cfg.sdt_client1_cfg.vif._set_width_values(ADDR_WIDTH = self.cfg.dut.ADDR_WIDTH,
                                                       DATA_WIDTH = self.cfg.dut.DATA_WIDTH)

        self.cfg.sdt_client2_cfg.vif._set_width_values(ADDR_WIDTH = self.cfg.dut.ADDR_WIDTH,
                                                       DATA_WIDTH = self.cfg.dut.DATA_WIDTH)

        self.cfg.sdt_mem_cfg.vif._set_width_values(ADDR_WIDTH = self.cfg.dut.ADDR_WIDTH,
                                                   DATA_WIDTH = self.cfg.dut.DATA_WIDTH)

        self.cfg.sdt_client0_cfg.vif.connect(
            rd_signal=self.dut.c0_rd,
            wr_signal=self.dut.c0_wr,
            addr_signal=self.dut.c0_addr,
            wr_data_signal=self.dut.c0_wr_data,
            rd_data_signal=self.dut.c0_rd_data,
            ack_signal=self.dut.c0_ack
        )

        self.cfg.sdt_client1_cfg.vif.connect(
            rd_signal=self.dut.c1_rd,
            wr_signal=self.dut.c1_wr,
            addr_signal=self.dut.c1_addr,
            wr_data_signal=self.dut.c1_wr_data,
            rd_data_signal=self.dut.c1_rd_data,
            ack_signal=self.dut.c1_ack
        )

        self.cfg.sdt_client2_cfg.vif.connect(
            rd_signal=self.dut.c2_rd,
            wr_signal=self.dut.c2_wr,
            addr_signal=self.dut.c2_addr,
            wr_data_signal=self.dut.c2_wr_data,
            rd_data_signal=self.dut.c2_rd_data,
            ack_signal=self.dut.c2_ack
        )

        self.cfg.sdt_mem_cfg.vif.connect(
            rd_signal=self.dut.m_rd,
            wr_signal=self.dut.m_wr,
            addr_signal=self.dut.m_addr,
            wr_data_signal=self.dut.m_wr_data,
            rd_data_signal=self.dut.m_rd_data,
            ack_signal=self.dut.m_ack
        )

        self.logger.info("End connect_phase() -> MARB base test")

    async def run_phase(self):
        self.logger.info("Start run_phase() -> MARB base test")
        await super().run_phase()

        await self.start_clock()
        await self.trigger_reset()

        # TODO: Start SDT IF assertions chekers for producers and consumer
        self.assert_check_sdt_client0.check_prod_assertions()
        self.assert_check_sdt_client1.check_prod_assertions()
        self.assert_check_sdt_client2.check_prod_assertions()
        self.assert_check_sdt_mem.check_cons_assertions()

        # TODO: Start the global ACK checker

        # Start APB IF assertion checker
        cocotb.start_soon(self.assert_check_apb.check_assertions())

        self.logger.info("End run_phase() -> MARB base test")

    async def start_clock(self):
        # start a clock of randomizd clock period [1, 5] ns
        self.clk_period = randint(1, 5)
        cocotb.start_soon(Clock(self.dut.clk, self.clk_period, 'ns').start())


    async def trigger_reset(self):
        """Activation and deactivation of reset """

        # Wait randomized number of clock cyles in [0, 5]
        await ClockCycles(self.dut.clk, randint(0, 5))

        # Activate reset
        self.logger.info("Waiting for reset")
        self.dut.rst.value = 1

        # Wait randomized number of clock cycles before deactivating reset
        await ClockCycles(self.dut.clk, randint(1, 20))
        self.dut.rst.value = 0

        self.logger.info("Reset Done")

    def end_of_elaboration_phase(self):
        super().end_of_elaboration_phase()

    def report_phase(self):
        self.logger.info("Start report_phase() -> MARB base test")
        super().report_phase()

        assert self.assert_check_apb.passed, "APB IF assertions failed"

        # Creating coverage report with PyVSC in txt format
        try:
            test_number = cocotb.plusargs["test_number"]
        except:
            test_number = 0

        # Writing coverage report in txt-format
        f = open(f'sim_build/{self.get_type_name()}_{test_number}_cov.txt', "w")
        f.write(f"Coverage report for {self.get_type_name()} #{test_number} \n")
        f.write("------------------------------------------------\n \n")
        vsc.report_coverage(fp=f, details=True)
        f.close()

        # Writing coverage report in xml-format
        vsc.write_coverage_db(
            f'sim_build/{self.get_type_name()}_{test_number}_cov.xml')

        self.logger.info("End report_phase() -> MARB base test")
