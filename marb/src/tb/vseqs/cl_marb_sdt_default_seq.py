import cocotb

from cocotb.triggers import Combine
from uvc.sdt.src import *
from cl_marb_tb_base_seq import cl_marb_tb_base_seq

from uvc.sdt.src.uvc_sdt_seq_lib import cl_sdt_single_zd_seq

class cl_marb_sdt_default_seq(cl_marb_tb_base_seq):
    """Start virutal sequence of rd and wr in parallel for each producer"""

    def __init__(self, name = "cl_marb_basic_seq"):
        super().__init__(name)

        self.mem_seq = cl_sdt_single_zd_seq.create("sdt_mem_seq")
        self.client0_seq = cl_sdt_single_zd_seq.create("sdt_client0_seq")
        self.client1_seq = cl_sdt_single_zd_seq.create("sdt_client1_seq")
        self.client2_seq = cl_sdt_single_zd_seq.create("sdt_client2_seq")

    async def body(self):
        self.sequencer.logger.info("STARTING SUPER:BODY")
        await super().body()

        self.sequencer.logger.info("STARTING STARTING SEQUENCES")

        mem_task = cocotb.start_soon(self.mem_seq.start(self.sequencer.sdt_mem_sequencer))
        client0_task = cocotb.start_soon(self.client0_seq.start(self.sequencer.sdt_client0_sequencer))
        client1_task = cocotb.start_soon(self.client1_seq.start(self.sequencer.sdt_client1_sequencer))
        client2_task = cocotb.start_soon(self.client2_seq.start(self.sequencer.sdt_client2_sequencer))

        # Finishes when ALL tasks finishes
        await Combine(
            mem_task,
            client0_task,
            client1_task,
            client2_task
        )