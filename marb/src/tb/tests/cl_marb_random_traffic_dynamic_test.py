import pyuvm
from pyuvm import *
from cocotb.triggers import ClockCycles

from cl_marb_tb_base_test import cl_marb_tb_base_test
from cl_marb_tb_base_seq import cl_marb_tb_base_seq
from vseqs.cl_reg_simple_dynamic_seq import cl_reg_simple_dynamic_seq
from vseqs.cl_marb_random_traffic_seq import cl_marb_random_traffic_seq
from uvc.sdt.src import *


@pyuvm.test(timeout_time=10000, timeout_unit='ns')
class cl_marb_random_traffic_dynamic_test(cl_marb_tb_base_test):
    """Random traffic test with dynamic priority configuration"""

    def __init__(self, name="cl_marb_random_traffic_dynamic_test", parent=None):
        super().__init__(name, parent)

    def start_of_simulation_phase(self):
        self.logger.info("Start start_of_simulation_phase() -> MARB random traffic dynamic test")
        super().start_of_simulation_phase()

        # Reuse the same random traffic sequence as static test
        uvm_factory().set_type_override_by_type(
            cl_marb_tb_base_seq,
            cl_marb_random_traffic_seq
        )
        self.logger.info("End start_of_simulation_phase() -> MARB random traffic dynamic test")

    async def run_phase(self):
        self.logger.info("Start run_phase() -> MARB random traffic dynamic test")
        self.raise_objection()
        await super().run_phase()

        # Configure Memory Arbiter with DYNAMIC priority
        conf_seq = cl_reg_simple_dynamic_seq.create("conf_seq")
        cocotb.start_soon( conf_seq.start(self.marb_tb_env.virtual_sequencer))         # TODO: NOTE - AWAIT OR START_SOON?

        self.logger.debug("Starting random traffic seq (vseqs/cl_marb_random_traffic_seq)")
        random_traffic_seq = cl_marb_random_traffic_seq.create("random_traffic_seq")
        random_traffic_seq.randomize() #Randomize the number of transactions
        await random_traffic_seq.start(self.marb_tb_env.virtual_sequencer)

        # Traffic sequence runs via factory override
        await ClockCycles(self.dut.clk, 20)
        self.drop_objection()

        self.logger.info("End run_phase() -> MARB random traffic dynamic test")