import logging

log = logging.getLogger(__name__)


class FpgaRegister:

    def __init__(self, parent):
        self.parent = parent

    def write_mem(
        self,
        name: str,
        module: str,
        bank: str,
        offset: int,
        value: int | str,
        delay=10,
    ):
        """
        Writes <value> to module's FPGA register: <offset>, in <bank>.

        Parameters
        ----------
        name
            title given to this instruction.
        module
            The name of the module that this instruction is to be used on.
        bank
            name of the FPGA register bank.
        offset
            Offset of register in bank lword addressed.
        hvi_register
            name of hvi register to be read from the FPGA register.
        value
            | if int, value to be written to the FPGA register
            | if str, name of HVI register to be written to the FPGA register
        delay
            The wait (in ns) before the instruction is started.

        """
        sequence = self.parent._get_current_sequence(module)
        statement_name = self.parent._statement_name(sequence, name)
        bank_id = sequence.engine.fpga_sandboxes[0].fpga_memory_maps[bank]
        log.debug(f"......{statement_name}")
        cmd = sequence.instruction_set.fpga_array_write
        instruction = sequence.add_instruction(statement_name, delay, cmd.id)
        instruction.set_parameter(cmd.fpga_memory_map.id, bank_id)
        instruction.set_parameter(cmd.fpga_memory_map_offset.id, offset)
        if type(value) is str:
            value = sequence.scope.registers[value]
        instruction.set_parameter(cmd.value.id, value)
        return

    def read_mem(
        self,
        name: str,
        module: str,
        bank: str,
        offset: int,
        hvi_register: str,
        delay: int = 10,
    ):
        """
        Reads from module's FPGA register, <register> into HVI register <hvi_register.

        Parameters
        ----------
        name
            title given to this instruction.
        module
            The name of the module that this instruction is to be used on.
        bank
            name of the FPGA register bank.
        offset
            Offset of register in bank lword addressed.
        hvi_register
            name of hvi register to be read from the FPGA register.
        delay
            The wait (in ns) before the instruction is started.
        """
        sequence = self.parent._get_current_sequence(module)
        statement_name = self.parent._statement_name(sequence, name)
        bank_id = sequence.engine.fpga_sandboxes[0].fpga_memory_maps[bank]
        log.debug(f"......{statement_name}")
        cmd = sequence.instruction_set.fpga_array_read
        instruction = sequence.add_instruction(statement_name, delay, cmd.id)
        instruction.set_parameter(cmd.fpga_memory_map.id, bank_id)
        instruction.set_parameter(cmd.fpga_memory_map_offset.id, offset)
        dest_register = sequence.scope.registers[hvi_register]
        instruction.set_parameter(cmd.destination.id, dest_register)
        return

    def write(
        self,
        name: str,
        module: str,
        register: str,
        value: int | str,
        delay: int = 10,
    ):
        """
        Writes <value> to module's FPGA register: <register>.

        Parameters
        ----------
        name
            title given to this instruction.
        module
            The name of the module that this instruction is to be used on.
        register
            name of the FPGA register
        value
            | if int, value to be written to the FPGA register
            | if str, name of HVI register to be written to the FPGA register
        delay
            The wait (in ns) before the instruction is started.
        """
        sequence = self.parent._get_current_sequence(module)
        statement_name = self.parent._statement_name(sequence, name)
        register_id = sequence.engine.fpga_sandboxes[0].fpga_registers[register]
        log.debug(f"......{statement_name}")
        reg_cmd = sequence.instruction_set.fpga_register_write
        instruction = sequence.add_instruction(statement_name, delay, reg_cmd.id)
        instruction.set_parameter(reg_cmd.fpga_register.id, register_id)
        if type(value) is str:
            value = sequence.scope.registers[value]
        instruction.set_parameter(reg_cmd.value.id, value)
        return

    def read(
        self,
        name: str,
        module: str,
        fpga_register: str,
        hvi_register: str,
        delay=10,
    ):
        """
        Reads from module's FPGA register, <register> into HVI register <hvi_register.

        Parameters
        ----------
        name
            title given to this instruction.
        module
            The name of the module that this instruction is to be used on.
        fpga_register
            name of the FPGA register to be written to.
        hvi_register
            name of HVI register to be written to the FPGA register.
        delay
            The wait (in ns) before the instruction is started.
        """
        sequence = self.parent._get_current_sequence(module)
        statement_name = self.parent._statement_name(sequence, name)
        register_id = sequence.engine.fpga_sandboxes[0].fpga_registers[fpga_register]
        log.debug(f"......{statement_name}")
        reg_cmd = sequence.instruction_set.fpga_register_read
        instruction = sequence.add_instruction(statement_name, delay, reg_cmd.id)
        instruction.set_parameter(reg_cmd.fpga_register.id, register_id)
        dest_register = sequence.scope.registers[hvi_register]
        instruction.set_parameter(reg_cmd.destination.id, dest_register)
        return
