""" SDT interface asserations wrapper"""

import pyuvm
from pyuvm import *
from cocotb.triggers import RisingEdge, ReadOnly


class sdt_if_assertions():

    def __init__(self,
                 clk_signal=None,
                 rst_signal=None,
                 wr_signal=None,
                 wr_data_signal=None,
                 rd_signal=None,
                 rd_data_signal=None,
                 addr_signal=None,
                 ack_signal=None,
                 name="ssdt_if_assertions"):

        self.name = name

        self.clk = clk_signal
        self.rst = rst_signal

        self.wr = wr_signal
        self.wr_data = wr_data_signal

        self.rd = rd_signal
        self.rd_data = rd_data_signal

        self.addr = addr_signal
        self.ack = ack_signal

        # Set as false if any assertion fail
        self.passed = True

        # The data width interface
        self.DATA_WIDTH = None

    def set_width_values(self, DATA_WIDTH=1):
        self.DATA_WIDTH = DATA_WIDTH

    #Mem gets these outputs from our DUT
    def check_cons_assertions(self):
        cocotb.start_soon(self.reset_values(self.wr))
        cocotb.start_soon(self.data_validity(self.wr,self.wr_data))
        cocotb.start_soon(self.data_invalidity(self.wr,self.wr_data))
        cocotb.start_soon(self.read_and_write_invar(self.wr,self.rd))
        cocotb.start_soon(self.addr_not_x_invar(self.wr,self.rd,self.addr))
        cocotb.start_soon(self.wr_data_not_x_invar(self.wr,self.wr_data))


    #Clients gets these outputs from our DUT
    def check_prod_assertions(self):
        cocotb.start_soon(self.reset_values(self.ack))
        cocotb.start_soon(self.data_validity(self.ack,self.rd_data))
        cocotb.start_soon(self.data_invalidity(self.ack,self.rd_data))
        cocotb.start_soon(self.wr_data_not_x_invar(self.ack, self.rd_data))

    # Reset requirement (PR 1):
    # If RST = 1, then VALID cannot be 1
    async def reset_values(self, valid_sig):
        while True:
            await RisingEdge(self.clk)
            await ReadOnly()

            try:
                if self.rst.value.binstr == '1':
                    assert valid_sig.value.binstr != '1', \
                        f"When reset, valid was {valid_sig.value.binstr}"
            except AssertionError as msg:
                self.passed = False
                print(msg)

            # Wait 1 clk cycle
            await RisingEdge(self.clk)

    # Data valitidy requirement (PR 2):
    async def data_validity(self, valid_sig, data_sig):
        MAX = (2 ** self.DATA_WIDTH) - 1

        while True:
            # Wait 1 clk cycle
            await RisingEdge(self.clk)
            await ReadOnly()

            try:
                if valid_sig.value.binstr == '1':
                    # Assume valid data means within data width
                    assert 0 <= data_sig.value.integer <= MAX, \
                        f"When valid, data was {data_sig.value.binstr}"
            except AssertionError as msg:
                self.passed = False
                print(msg)

    # Data invalidity requirement (PR 3):
    async def data_invalidity(self, valid_sig, data_sig):
        while True:
            # Wait 1 clk cycle
            await RisingEdge(self.clk)
            await ReadOnly()

            try:
                if valid_sig.value.binstr == '0':
                    assert data_sig.value.integer == 0, \
                        f"When valid was low, data was {data_sig.value.binstr}"
            except AssertionError as msg:
                self.passed = False
                print(msg)

    #INVARIANTS:
    #Invariant 1: Asserting rd and wr at the same time is illegal
    async def read_and_write_invar(self,rd_sig,wr_sig):
        while True:
            await RisingEdge(self.clk)
            await ReadOnly()

            try:
                if rd_sig.value.binstr == '1':
                    assert wr_sig.value.binstr == '0', \
                        f"When rd was high, wr was {wr_sig.value.binstr}"
            except AssertionError as msg:
                self.passed = False
                print(msg)

    # Invariant 2: When rd or wr is asserted, addr must not be X
    async def addr_not_x_invar(self,addr_sig, rd_sig, wr_sig):
        while True:
            await RisingEdge(self.clk)
            await ReadOnly()

            try:
                if (rd_sig.value.binstr == '1') or (wr_sig.value.binstr == '1'):
                    assert 'x' not in addr_sig.value.binstr.lower(), \
                        f"When rd or wr was high, addr was {addr_sig.value.binstr}"
            except AssertionError as msg:
                self.passed = False
                print(msg)

    # Invariant 3: When wr is asserted, wr_data must not be X
    async def wr_data_not_x_invar(self,wr_sig,wr_data_sig):
        while True:
            await RisingEdge(self.clk)
            await ReadOnly()

            try:
                if wr_sig.value.binstr == '1':
                    assert 'x' not in wr_data_sig.value.binstr.lower(), \
                        f"When rd or wr was high, addr was {wr_data_sig.value.binstr}"          # Broken on purpose
            except AssertionError as msg:
                self.passed = False
                print(msg)