import numpy as np


class Runtime:
    def __init__(self, parent):
        self.parent = parent

    def read_register(self, module: str, register: str):
        register_runtime = self.parent.hvi_handle.sync_sequence.scopes[
            module
        ].registers[register]
        value = register_runtime.read()
        return value

    def write_register(self, module: str, register: str, value: int):
        """
        Writes <value> to module's FPGA register: <offset>, in <bank>.

        Parameters
        ----------
        module
            The name of the module that contains the HVI registers to be written to.
        register
            name of hvi register to be written to.
        value
            value to be written to the register

        """
        register_runtime = self.parent.hvi_handle.sync_sequence.scopes[
            module
        ].registers[register]
        register_runtime.write(np.uint32(value))

    def write_fpga_register_mem(self, module: str, bank: str, offset: int, value: int):
        """
        Writes <value> to module's FPGA register: <offset>, in <bank>.

        Parameters
        ----------
        module
            The name of the module that this instruction is to be used on.
        bank
            name of the FPGA register bank.
        offset
            Offset of register in bank lword addressed.
        value
            value to be written to the FPGA register.

        """
        register_runtime = (
            self.parent.hvi_handle.sync_sequence.engines[module]
            .fpga_sandboxes[0]
            .fpga_memory_maps[bank]
        )
        register_runtime.write(offset, np.uint32(value))
