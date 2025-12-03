import vsc

from uvc.sdt.src import *
from cl_marb_tb_base_seq import cl_marb_tb_base_seq
from reg_model.seq_lib.cl_reg_setup_seq import cl_reg_setup_seq
from reg_model.seq_lib.cl_reg_dynamic_seq import cl_reg_dynamic_seq

@vsc.randobj
class cl_reg_simple_dynamic_seq(cl_marb_tb_base_seq, object):
    """Setup and start Memory Arbiter with dynamic configuration"""

    def __init__(self, name="cl_reg_simple_dynamic_seq"):
        cl_marb_tb_base_seq.__init__(self, name)
        object.__init__(self)

    async def body(self):
        await super().body()

        # Step 1: Run setup sequence (disables arbiter, resets dprio_reg)
        self.sequencer.logger.debug("Starting setup seq (reg_model/seq_lib/cl_reg_setup_seq.py)")
        setup_seq = cl_reg_setup_seq.create("setup_seq")
        await setup_seq.start(self.sequencer)

        # Step 2: Run dynamic sequence (sets priorities and enables dynamic mode)
        self.sequencer.logger.debug("Starting dynamic seq (reg_model/seq_lib/cl_reg_dynamic_seq.py)")
        dynamic_seq = cl_reg_dynamic_seq.create("dynamic_seq")
        dynamic_seq.randomize()  # Randomize the priority values!
        await dynamic_seq.start(self.sequencer)