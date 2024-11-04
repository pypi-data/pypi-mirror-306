import logging
from typing import Tuple

import keysight_tse as kthvi

log = logging.getLogger(__name__)


class SyncBlock:
    """
    This subclass includes all the commands to control synchronous behaviour across all modules
    assigned to the HVI sequence.
    """

    def __init__(self, parent):
        self.parent = parent

    def start_while_register(
        self,
        name: str,
        engine: str,
        register: str,
        operator: str,
        value: int | str,
        delay: int = 70,
    ):
        """
        | Synchronous (across all modules) while loop. Compares <register> (hosted by module <engine>) with <value>
            using <comparison>.
        | Must be closed with 'end_while()'.
        | Typically this will have a 'sync multi sequence block' within the while loop.

        Parameters
        ----------
        name
            title given to this instruction.
        engine
            name of module hosting the comparison register. (from Module_description.name)
        register
            name of register used for comparison (the 'comparison register').
        operator
            the comparison operator:

            - 'EQUAL_TO'
            - 'GREATER_THAN'
            - 'GREATER_THEN_OR_EQUAL_TO'
            - 'LESS_THAN'
            - 'LESS_THAN_OR_EQUAL_TO'
            - 'NOT_EQUAL_TO'

        value
            | if int, value to be compared to
            | if str, name of HVI register to be compared to
        delay
            The wait (in ns) before the instruction is started.

        """
        sequence = self.parent._current_sync_sequence[-1]
        statement_name = self.parent._sync_statement_name(sequence, name)
        whileRegister = self.parent._sequencer.sync_sequence.scopes[engine].registers[
            register
        ]
        comparison_operator = getattr(kthvi.ComparisonOperator, operator)
        if type(value) is str:
            value = sequence.scope.registers[value]
        log.debug(f"Creating Synchronized While loop, {value} iterations...")
        condition = kthvi.Condition.register_comparison(
            whileRegister, comparison_operator, value
        )
        while_sequence = sequence.add_sync_while(statement_name, delay, condition)
        self.parent._current_sync_sequence.append(while_sequence.sync_sequence)
        return

    def end_while(self):
        """
        Marks the end of a 'while_register' loop block. Each 'start_while_xxx()' must
        be terminated with this call.
        """
        self.parent._current_sync_sequence.pop()
        return

    def start_multi_sequence_block(self, name: str, delay: int = 30):
        """
        | Synchronous (across all modules) block. This encapsulates instructions for individual
          modules. If the modules have different execution times, this block only exits when all
          the modules have finished. Thus keeping all modules in sync.
        | Must be closed with 'end_multi_sequence_block()'.

        Parameters
        ----------
        name
            title given to this instruction.
        delay
            The wait (in ns) before the instruction is started.

        """
        sequence = self.parent._current_sync_sequence[-1]
        statement_name = self.parent._sync_statement_name(sequence, name)
        block = sequence.add_sync_multi_sequence_block(statement_name, delay)
        self.parent._current_block.append(block)
        for module in self.parent._modules:
            module._current_sequence.append(block.sequences[module.name])
        return

    def end_multi_sequence_block(self):
        """
        Marks the end of a 'multi_sequence_block' loop block. Each start_multi_sequence_block()
        must be terminated with this call.
        """
        self.parent._current_block.pop()
        for module in self.parent._modules:
            module._current_sequence.pop()
