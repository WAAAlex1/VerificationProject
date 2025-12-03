""" SSDT interface asserations wrapper"""

import pyuvm
from pyuvm import *
from cocotb.triggers import RisingEdge, ReadOnly


class ssdt_if_assertions():

    def __init__(self, clk_signal=None, rst_signal=None, valid_signal=None, data_signal=None,
                 name="ssdt_if_assertions"):

        self.name = name

        self.clk = clk_signal
        self.rst = rst_signal

        self.valid = valid_signal
        self.data = data_signal

        # Set as false if any assertion fail
        self.passed = True

        # The data width interface
        self.DATA_WIDTH = None

    def _set_width_values(self, DATA_WIDTH=1):
        self.DATA_WIDTH = DATA_WIDTH

    def check_assertions(self):
        cocotb.start_soon(self.reset_values())
        cocotb.start_soon(self.data_validity())
        cocotb.start_soon(self.data_invalidity())

    # Reset requirement (PR 1):
    # If RST = 1, then VALID cannot be 1
    async def reset_values(self):
        while True:
            await RisingEdge(self.clk)
            await ReadOnly()

            try:
                if self.rst.value.binstr == '1':
                    assert self.valid.value.binstr != '1', \
                        f"When reset, valid was {self.valid.value.binstr}"
            except AssertionError as msg:
                self.passed = False
                print(msg)

            # Wait 1 clk cycle
            await RisingEdge(self.clk)

    # Data valitidy requirement (PR 2):
    async def data_validity(self):
        MAX = (2 ** self.DATA_WIDTH) - 1

        while True:
            # Wait 1 clk cycle
            await RisingEdge(self.clk)
            await ReadOnly()

            try:
                if self.valid.value.binstr == '1':
                    # Assume valid data means within data width
                    assert 0 <= self.data.value.integer <= MAX, \
                        f"When valid, data was {self.data.value.binstr}"
            except AssertionError as msg:
                self.passed = False
                print(msg)

    # Data invalidity requirement (PR 3):
    async def data_invalidity(self):
        while True:
            # Wait 1 clk cycle
            await RisingEdge(self.clk)
            await ReadOnly()

            try:
                if self.valid.value.binstr == '0':
                    assert self.data.value.integer == 0, \
                        f"When valid was low, data was {self.data.value.binstr}"
            except AssertionError as msg:
                self.passed = False
                print(msg)