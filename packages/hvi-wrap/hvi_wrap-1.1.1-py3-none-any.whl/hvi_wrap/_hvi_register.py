import logging
import keysight_tse as kthvi

log = logging.getLogger(__name__)


class HviRegister:

    def __init__(self, parent):
        self.parent = parent

    def set(self, name: str, module: str, register: str, value: int, delay: int = 10):
        """
        Sets <register> in <module> to <value>

        Parameters
        ----------
        name
            title given to this instruction.
        module
            The name of the module that this instruction is to be used on.
        register
            name of the destination HVI register.
        value
            value to be written to the FPGA register
        delay
            The wait (in ns) before the instruction is started.

        """
        sequence = self.parent._get_current_sequence(module)
        statement_name = self.parent._statement_name(sequence, name)
        register_id = sequence.scope.registers[register]
        log.debug(f"......{statement_name}")
        instruction = sequence.add_instruction(
            statement_name, delay, sequence.instruction_set.assign.id
        )
        instruction.set_parameter(
            sequence.instruction_set.assign.destination.id, register_id
        )
        instruction.set_parameter(sequence.instruction_set.assign.source.id, value)

    def increment(self, name: str, module: str, register: str, delay: int = 10):
        """
        Increments <register> in <module>

        Parameters
        ----------
        name
            title given to this instruction.
        module
            The name of the module that this instruction is to be used on.
        register
            name of hvi register to be read from the FPGA register.
        delay
            The wait (in ns) before the instruction is started.

        """
        self.add(name, module, register, 1, delay)

    def add(self, name: str, module: str, register: str, value: int, delay: int = 10):
        """
        Adds <value> to <register> in <module>

        Parameters
        ----------
        name
            title given to this instruction.
        module
            The name of the module that this instruction is to be used on.
        register
            name of the destination HVI register.
        value
            value to be written to the FPGA register
        delay
            The wait (in ns) before the instruction is started.

        """
        sequence = self.parent._get_current_sequence(module)
        statement_name = self.parent._statement_name(sequence, name)
        register_id = sequence.scope.registers[register]
        log.debug(f"......{statement_name}")
        instruction = sequence.add_instruction(
            statement_name, delay, sequence.instruction_set.add.id
        )
        instruction.set_parameter(
            sequence.instruction_set.add.destination.id, register_id
        )
        instruction.set_parameter(
            sequence.instruction_set.add.left_operand.id, register_id
        )
        instruction.set_parameter(sequence.instruction_set.add.right_operand.id, value)

    def start_if(self, name, module, register, comparison, value, delay=10):
        """
        Inserts an 'if' statement in the flow following instructions
        are only executed if condition evalutes to True.
        This should be terminated with 'end_if()' statement.

        """
        sequence = self.parent._get_current_sequence(module)
        statement_name = self.parent._statement_name(sequence, name)
        comparison_operator = getattr(kthvi.ComparisonOperator, comparison)
        if_condition = kthvi.Condition.register_comparison(
            register, comparison_operator, value
        )
        enable_matching_branches = True
        if_statement = sequence.add_if(
            statement_name, delay, if_condition, enable_matching_branches
        )
        self.parent._push_current_sequence(module, if_statement.if_branch.sequence)

    def end_if(self, module):
        self.parent._pop_current_sequence(module)
