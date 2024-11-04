import logging
from typing import List, Tuple
import keysight_tse as kthvi

log = logging.getLogger(__name__)


class Triggers:
    def __init__(self, parent):
        self.parent = parent

    def setup(
        self,
        module_name: str,
        triggers: List[str],
        direction: str,
        polarity: str | None,
        sync: str,
        hw_delay: int,
        mode: int = 0,
    ):
        """
        Sets up the physical triggers within the device. If an argument
        is type None then hardware is not changed for that argument

        Args
        ----
        direction
            "INPUT" or "OUTPUT".
        polarity
            "ACTIVE_HIGH" or "ACTIVE_LOW".
        sync
            "SYNCH' or "IMMEDIATE".
        hw_delay
            delay in ns before the output changes state.
        mode
        0 = LEVEL MODE, anything else = PULSE MODE with pulses width
        equal to the value in ns.
        """
        for trigger in triggers:
            if direction is None:
                pass
            elif direction.upper() == "OUTPUT":
                self.parent._system_definition.engines[module_name].triggers[
                    trigger
                ].config.direction = kthvi.Direction.OUTPUT
            elif direction.upper() == "INPUT":
                self.parent._system_definition.engines[module_name].triggers[
                    trigger
                ].config.direction = kthvi.Direction.INPUT
            else:
                raise ValueError(
                    "If specified, trigger direction should be 'INPUT' or 'OUTPUT'"
                )

            if polarity is None:
                pass
            elif polarity.upper() == "ACTIVE_HIGH":
                self.parent._system_definition.engines[module_name].triggers[
                    trigger
                ].config.polarity = kthvi.Polarity.ACTIVE_HIGH
            elif polarity.upper() == "ACTIVE_LOW":
                self.parent._system_definition.engines[module_name].triggers[
                    trigger
                ].config.polarity = kthvi.Polarity.ACTIVE_LOW
            else:
                raise ValueError(
                    "If specified, trigger polarity should be 'ACTIVE_HIGH' or 'ACTIVE_LOW'"
                )

            if sync is None:
                pass
            elif sync.upper() == "SYNC":
                self.parent._system_definition.engines[module_name].triggers[
                    trigger
                ].config.sync_mode = kthvi.SyncMode.SYNC
            elif sync.upper() == "IMMEDIATE":
                self.parent._system_definition.engines[module_name].triggers[
                    trigger
                ].config.sync_mode = kthvi.SyncMode.IMMEDIATE
            else:
                raise ValueError(
                    "If specified, trigger sync should be 'SYNC' or 'IMMEDIATE'"
                )

            if hw_delay is None:
                pass
            else:
                self.parent._system_definition.engines[module_name].triggers[
                    trigger
                ].config.hw_routing_delay = hw_delay

            if mode is None:
                pass
            elif mode == 0:
                self.parent._system_definition.engines[module_name].triggers[
                    trigger
                ].config.trigger_mode = kthvi.TriggerMode.LEVEL
            else:
                self.parent._system_definition.engines[module_name].triggers[
                    trigger
                ].config.trigger_mode = kthvi.TriggerMode.PULSE
                self.parent._system_definition.engines[module_name].triggers[
                    trigger
                ].config.pulse_length = mode

    def on(self, name, module, triggers, delay=10):
        """
        Adds an instruction called <name> to sequence for <module> to the current block
        to assert all <triggers>
        triggers can be pxi0..pxi7 (but only if not committed to HVI system), smb1..smb8
        """
        sequence = self.parent._get_current_sequence(module)
        statement_name = self.parent._statement_name(sequence, name)
        log.debug(f"......{statement_name}")
        triggerCmd = sequence.instruction_set.trigger_write
        triggerParams = [sequence.engine.triggers[trigger] for trigger in triggers]
        instruction = sequence.add_instruction(statement_name, delay, triggerCmd.id)
        instruction.set_parameter(triggerCmd.trigger.id, triggerParams)
        instruction.set_parameter(triggerCmd.sync_mode.id, kthvi.SyncMode.IMMEDIATE)
        instruction.set_parameter(triggerCmd.value.id, kthvi.TriggerValue.ON)

    def off(self, name, module, triggers, delay=10):
        """
        Adds an instruction called <name> to sequence for <module> to the current block
        to disassert all <triggers>
        triggers can be pxi0..pxi7 (but only if not committed to HVI system), smb1..smb8
        """
        sequence = self.parent._get_current_sequence(module)
        statement_name = self.parent._statement_name(sequence, name)
        log.debug(f"......{statement_name}")
        triggerCmd = sequence.instruction_set.trigger_write
        triggerParams = [sequence.engine.triggers[trigger] for trigger in triggers]
        instruction = sequence.add_instruction(statement_name, delay, triggerCmd.id)
        instruction.set_parameter(triggerCmd.trigger.id, triggerParams)
        instruction.set_parameter(triggerCmd.sync_mode.id, kthvi.SyncMode.IMMEDIATE)
        instruction.set_parameter(triggerCmd.value.id, kthvi.TriggerValue.OFF)

    def wait(self, name: str, module: str, trigger: str, delay: int = 10):
        """
        Waits for a trigger to occur. The trigger must from inactive to active whilst
        in this waiting state. If the trigger was already true on entry, then this state
        is only left one the trigger goes inactive and them back to active.
        Parameters
        ----------
        name
            title given to this instruction.
        delay
            The wait (in ns) before the instruction is started.
        module
            The name of module where the trigger is located. (from Module_description.name).
        trigger
            The name of the trigger e.g. 'smb1'.

        """
        sequence = self.parent._get_current_sequence(module)
        statement_name = self.parent._statement_name(sequence, name)
        log.debug(f"......{statement_name}")
        condition = kthvi.Condition.trigger(
            self.parent._system_definition.engines[0].triggers[trigger[0]]
        )
        instruction = sequence.add_wait(statement_name, delay, condition)
        instruction.set_mode(kthvi.WaitMode.TRANSITION, kthvi.SyncMode.IMMEDIATE)
        pass
