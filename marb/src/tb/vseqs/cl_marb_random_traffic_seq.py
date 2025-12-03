import cocotb
import vsc
from cocotb.triggers import Combine

from cl_marb_tb_base_seq import cl_marb_tb_base_seq

from uvc.sdt.src.cl_sdt_seq_lib import cl_sdt_single_zd_seq
from uvc.sdt.src.cl_sdt_seq_lib import cl_sdt_consumer_rsp_seq

_THRESHOLD = 67

@vsc.randobj
class cl_marb_random_traffic_seq(cl_marb_tb_base_seq):
    def __init__(self, name="cl_marb_random_traffic_seq"):
        super().__init__(name)

        # Iteration parameter to control number of requests
        self.num_transactions_cif0 = vsc.rand_uint32_t()
        self.num_transactions_cif1 = vsc.rand_uint32_t()
        self.num_transactions_cif2 = vsc.rand_uint32_t()

    @vsc.constraint
    def itr_nbr_c(self):
        self.num_transactions_cif0.inside(vsc.rangelist(vsc.rng(1,_THRESHOLD)))
        self.num_transactions_cif1.inside(vsc.rangelist(vsc.rng(1, _THRESHOLD)))
        self.num_transactions_cif2.inside(vsc.rangelist(vsc.rng(1, _THRESHOLD)))

    async def body(self):
        await super().body()

        # Calculate total expected transactions
        total_expected = (self.num_transactions_cif0 +
                         self.num_transactions_cif1 +
                         self.num_transactions_cif2)

        # Configure memory consumer - access through virtual sequencer
        self.sequencer.sdt_mem_sequencer.cfg.num_consumer_seq = total_expected

        self.sequencer.logger.info(
            f"Starting random traffic: CIF0={self.num_transactions_cif0}, "
            f"CIF1={self.num_transactions_cif1}, "
            f"CIF2={self.num_transactions_cif2}, "
            f"Total Expected={total_expected}"
        )

        print(
            f"Starting random traffic: CIF0={self.num_transactions_cif0}, "
            f"CIF1={self.num_transactions_cif1}, "
            f"CIF2={self.num_transactions_cif2}, "
            f"Total Expected={total_expected}"
        )

        # Create tasks for each client interface
        cif0_task = cocotb.start_soon(self.client0_traffic())
        cif1_task = cocotb.start_soon(self.client1_traffic())
        cif2_task = cocotb.start_soon(self.client2_traffic())
        mem_task = cocotb.start_soon(self.memory_traffic())

        # Wait for all tasks to complete
        await Combine(cif0_task, cif1_task, cif2_task, mem_task)

    async def client0_traffic(self):
        """Generate random traffic for Client Interface 0"""
        for i in range(int(self.num_transactions_cif0)):
            seq = cl_sdt_single_zd_seq.create(f"cif0_seq_{i}")
            seq.randomize()  # Randomize the sequence
            await seq.start(self.sequencer.sdt_client0_sequencer)

    async def client1_traffic(self):
        """Generate random traffic for Client Interface 1"""
        for i in range(int(self.num_transactions_cif1)):
            seq = cl_sdt_single_zd_seq.create(f"cif1_seq_{i}")
            seq.randomize()
            await seq.start(self.sequencer.sdt_client1_sequencer)

    async def client2_traffic(self):
        """Generate random traffic for Client Interface 2"""
        for i in range(int(self.num_transactions_cif2)):
            seq = cl_sdt_single_zd_seq.create(f"cif2_seq_{i}")
            seq.randomize()
            await seq.start(self.sequencer.sdt_client2_sequencer )

    async def memory_traffic(self):
        """Memory consumer responds to requests"""
        seq = cl_sdt_consumer_rsp_seq.create(f"mem_consumer_seq")
        await seq.start(self.sequencer.sdt_mem_sequencer )