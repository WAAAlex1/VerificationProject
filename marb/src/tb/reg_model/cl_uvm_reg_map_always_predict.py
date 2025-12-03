from pyuvm.s21_uvm_reg_map import *

# Extention to the uvm_reg_map class that reoved the enable_auto_predict to always call the prediction

class uvm_reg_map_always_predict(uvm_reg_map):
    def __init__(self,name="uvm_reg_map"):
        super().__init__(name)

    # process_read_operation
    async def process_read_operation(self, reg_address, path: path_t,
                                     check: check_t):
        # Get the sequencer and the adapter
        local_adapter = self.get_adapter()
        # Build a local reg_item
        # TODO: this should come as input of the main process operation
        item = uvm_reg_item()
        item.set_kind(access_e.UVM_WRITE)
        item.set_door(path)
        item.set_map(self)
        item.set_parent_sequence(None)
        # check if we pass this point we are ready to go
        self.check_process_integrity(local_adapter, item)
        local_sequencer = self.get_sequencer()
        # check if the Path is set to BACKDOOR, FRONTDOOR or USER_FRONTDOOR
        if (path is path_t.BACKDOOR):
            uvm_not_implemeneted(self.header, "BACKDOOR not implemented")
        elif (path is path_t.USER_FRONTDOOR):
            uvm_not_implemeneted(self.header, "USER_FRONTDOOR not implemented")
        elif (path is path_t.FRONTDOOR):
            # Populate internal Item
            local_bus_op = uvm_reg_bus_op()
            local_bus_op.kind = access_e.UVM_READ
            local_bus_op.addr = reg_address
            local_bus_op.n_bits = self._regs[reg_address].get_reg_size()
            local_bus_op.byte_en = local_adapter.get_byte_en()
            # Parse the local bus operation with the adapter
            # give the ITEM once to the adpater so it can
            # eventually fecth the extension element
            local_adapter.set_item(item)
            bus_req = local_adapter.reg2bus(local_bus_op)
            local_adapter.set_item(None)
            # Get the sequence and start
            local_sequence = local_adapter.get_parent_sequence()
            # set the sequencer to the local sequence
            local_sequence.sequencer = local_sequencer
            # Start the sequence on local sequencer
            await local_sequence.start_item(bus_req)
            await local_sequence.finish_item(bus_req)
            # Get the sequence item from the local sequence
            # Assign the response and read data back
            local_adapter.bus2reg(bus_req, local_bus_op)
            # Invoke the prediction
            local_predictor = self.get_predictor()
            local_predictor.predict(local_bus_op, check)
            return local_bus_op.status, local_bus_op.data

    # process_write_operation
    async def process_write_operation(self, reg_address, data_to_be_written,
                                      path: path_t, check: check_t):
        # Get the sequencer and the adapter
        local_adapter = self.get_adapter()
        # Build a local reg_item
        # TODO: this should come as input of the main process operation
        item = uvm_reg_item()
        item.set_kind(access_e.UVM_WRITE)
        item.set_value(data_to_be_written)
        item.set_door(path)
        item.set_map(self)
        item.set_parent_sequence(None)
        # check if we pass this point we are ready to go
        self.check_process_integrity(local_adapter, item)
        local_sequencer = self.get_sequencer()
        # check if the Path is set to BACKDOOR, FRONTDOOR or USER_FRONTDOOR
        if (path is path_t.BACKDOOR):
            uvm_not_implemeneted(self.header, "BACKDOOR not implemented")
        elif (path is path_t.USER_FRONTDOOR):
            uvm_not_implemeneted(self.header, "USER_FRONTDOOR not implemented")
        elif (path is path_t.FRONTDOOR):
            # Populate internal Item
            local_bus_op = uvm_reg_bus_op()
            local_bus_op.kind = access_e.UVM_WRITE
            local_bus_op.addr = reg_address
            local_bus_op.n_bits = self._regs[reg_address].get_reg_size()
            local_bus_op.byte_en = local_adapter.get_byte_en()
            local_bus_op.data = data_to_be_written
            # Parse the local bus operation with the adapter
            # give the ITEM once to the adpater so it can
            # eventually fecth the extension element
            local_adapter.set_item(item)
            bus_req = local_adapter.reg2bus(local_bus_op)
            local_adapter.set_item(None)
            # Get the sequence and start
            local_sequence = local_adapter.get_parent_sequence()
            # set the sequencer to the local sequence
            local_sequence.sequencer = local_sequencer
            # Start the sequence on local sequencer
            await local_sequence.start_item(bus_req)
            await local_sequence.finish_item(bus_req)
            # Get the sequence item from the local sequence
            # Assign the response and read data back
            local_adapter.bus2reg(bus_req, local_bus_op)
            # Invoke the prediction
            local_predictor = self.get_predictor()
            local_predictor.predict(local_bus_op, check)
            # assign status
            return local_bus_op.status

    # get_predictor
    def get_predictor(self):
        if (self.predictor is None):
            # TODO: this should be only a warning since depends
            # on the prediction type
            uvm_error(self.header, "predictor Not set")
        else:
            return self.predictor

