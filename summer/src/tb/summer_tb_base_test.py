""" Saturation Filter base UVM Test.
"""

import os, warnings

# CocoTB and VSC
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ReadOnly
import vsc

# PyUVM
import pyuvm
from pyuvm import uvm_test, uvm_report_object, uvm_root, uvm_factory, ConfigDB


@pyuvm.test()
class summer_tb_base_test(uvm_test):
    """ Base test component for the Summer TB.
    """

    def __init__(self, name="summer_base_test", parent=None):
        # ----------------------------------------------------------------------

        super().__init__(name, parent)

        
    def build_phase(self):
        super().build_phase()

        
    def connect_phase(self):
        super().connect_phase()


    async def run_phase(self):
        self.raise_objection()

        await super().run_phase()


        self.drop_objection()
