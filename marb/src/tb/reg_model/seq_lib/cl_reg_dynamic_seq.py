import vsc
from cocotb.triggers import ClockCycles
from .cl_reg_base_seq import *


@vsc.randobj
class cl_reg_dynamic_seq(cl_reg_base_seq, object):
    """Dynamic priority sequence for registers"""

    def __init__(self, name="cl_reg_dynamic_seq"):
        cl_reg_base_seq.__init__(self, name)
        object.__init__(self)

        # Randomizable priority values (8 bits each)
        self.cif0_priority = vsc.rand_uint8_t()
        self.cif1_priority = vsc.rand_uint8_t()
        self.cif2_priority = vsc.rand_uint8_t()

    @vsc.constraint
    def c_priority_values(self):
        # Priorities in range 1-255 (0 would mean no priority)
        self.cif0_priority in vsc.rangelist(vsc.rng(1, 255))
        self.cif1_priority in vsc.rangelist(vsc.rng(1, 255))
        self.cif2_priority in vsc.rangelist(vsc.rng(1, 255))

    async def pre_body(self):
        await super().pre_body()

    async def body(self):
        await super().body()

        self.sequencer.logger.info("=" * 70)
        self.sequencer.logger.info("DYNAMIC PRIORITY CONFIGURATION SEQUENCE")
        self.sequencer.logger.info("=" * 70)

        #######################
        # STEP 1: Write to dprio_reg (Dynamic Priority Register)
        #######################
        self.sequencer.logger.info("STEP 1: Writing random priorities to dprio_reg")

        # Pack priorities: [23:16]=cif2, [15:8]=cif1, [7:0]=cif0
        dprio_val = (self.cif2_priority << 16) | (self.cif1_priority << 8) | self.cif0_priority

        self.sequencer.logger.info(
            f"  CIF0 priority = {self.cif0_priority} "
            f"(0x{self.cif0_priority:02X})"
        )
        self.sequencer.logger.info(
            f"  CIF1 priority = {self.cif1_priority} "
            f"(0x{self.cif1_priority:02X})"
        )
        self.sequencer.logger.info(
            f"  CIF2 priority = {self.cif2_priority} "
            f"(0x{self.cif2_priority:02X})"
        )

        status = await self.sequencer.reg_model.dprio_reg.write(
            dprio_val, self.bus_map, path_t.FRONTDOOR, check_t.NO_CHECK
        )

        if status == status_t.IS_OK:
            self.sequencer.logger.info(
                f" SUCCESS: Successfully wrote 0x{dprio_val:08X} to dprio_reg"
            )
        else:
            self.sequencer.logger.error("  FAILED: WRITE TO dprio_reg FAILED!")

        #######################
        # STEP 2: Read current ctrl_reg
        #######################
        self.sequencer.logger.info("\nSTEP 2: Reading current ctrl_reg")

        status, read_val = await self.sequencer.reg_model.ctrl_reg.read(
            self.bus_map, path_t.FRONTDOOR, check_t.NO_CHECK
        )

        if status == status_t.IS_OK:
            self.sequencer.logger.info(
                f"  Current ctrl_reg value = 0x{read_val:08X}"
            )
        else:
            self.sequencer.logger.error("  FAILED: READ FROM ctrl_reg FAILED!")

        #######################
        # STEP 3: Enable arbiter in DYNAMIC mode
        #######################
        self.sequencer.logger.info("\nSTEP 3: Enabling arbiter in DYNAMIC mode")

        # Set enable bit (bit 0) and dynamic mode bit (bit 1)
        write_val = read_val | self.start_mask | self.dynamic_prio_mask

        self.sequencer.logger.info(
            f"  Setting ctrl_reg = 0x{write_val:08X} "
            f"(enable=1, mode=1)"
        )

        status = await self.sequencer.reg_model.ctrl_reg.write(
            write_val, self.bus_map, path_t.FRONTDOOR, check_t.NO_CHECK
        )

        if status == status_t.IS_OK:
            self.sequencer.logger.info("  SUCCESS: Successfully enabled dynamic mode")
        else:
            self.sequencer.logger.error("  FAILURE: WRITE TO ctrl_reg FAILED!")

        #######################
        # STEP 4: Wait 6 cycles for priority update
        #######################
        self.sequencer.logger.info("\nSTEP 4: Waiting 6 clock cycles for priority update...")

        await ClockCycles(self.cfg.apb_cfg.vif.clk, 6)

        self.sequencer.logger.info("Priority update complete")
        self.sequencer.logger.info("=" * 70)
        self.sequencer.logger.info("DYNAMIC PRIORITY CONFIGURATION COMPLETE")
        self.sequencer.logger.info("=" * 70)