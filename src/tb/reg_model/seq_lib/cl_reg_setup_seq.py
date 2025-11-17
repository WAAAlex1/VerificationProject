from pyuvm import *
from .cl_reg_base_seq import *

class cl_reg_setup_seq(cl_reg_base_seq):
    """Setup sequence for control registers"""

    def __init__(self, name = "cl_reg_setup_seq"):
        super().__init__(name)

    async def body(self):
        await super().body()

        #######################
        #  Start setup sequence
        #######################
        self.sequencer.logger.debug("Starting setup sequence for dprio_reg in map, ", self.bus_map)
        status, read_val = await self.sequencer.reg_model.dprio_reg.read(self.bus_map, path_t.FRONTDOOR, check_t.NO_CHECK)

        # Check the status received
        if status == status_t.IS_OK:
            self.sequencer.logger.info(
                f"Setup SEQ: read {read_val} "
                f"from dprio_reg, status = {status}")
        else:
            self.sequencer.logger.error("STATUS is NOT_OK")


        write_val = 0
        status = await self.sequencer.reg_model.dprio_reg.write(write_val, self.bus_map, path_t.FRONTDOOR, check_t.NO_CHECK)
        # Check the status received
        if status == status_t.IS_OK:
            self.sequencer.logger.info(
                f"SETUP SEQ: written {write_val} "
                f"to dprio_reg, status = {status}")
        else:
            self.sequencer.logger.error("STATUS is NOT_OK")
