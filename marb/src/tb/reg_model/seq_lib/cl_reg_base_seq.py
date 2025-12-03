from pyuvm import *

class cl_reg_base_seq(uvm_sequence):
    """Base sequence for register sequences"""

    def __init__(self, name = "cl_reg_base_seq"):
        super().__init__(name)

        self.start_mask        = 0x00000001
        self.dynamic_prio_mask = 0x00000002

        self.cfg     = None
        self.bus_map = None


    async def pre_body(self):

        if self.sequencer is not None:
            self.sequencer.logger.debug("Setting bus map and cfg in reg-sequence")

            self.bus_map = self.sequencer.reg_model.bus_map
            self.cfg = self.sequencer.cfg

        else:
            raise UVMFatalError("Sequencer for Reg Model not set")

    async def body(self):
        await super().body()

        if self.bus_map is None:
            raise UVMFatalError("Bus map not set, pre_body might not have run")
