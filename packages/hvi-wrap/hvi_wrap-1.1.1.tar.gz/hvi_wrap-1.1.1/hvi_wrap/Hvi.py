# -*- coding: utf-8 -*-

import os
import logging
from collections import deque
from typing import Tuple

import keysight_tse as kthvi

from .ModuleDescriptor import ModuleDescriptor

log = logging.getLogger(__name__)


class Hvi:
    """
    Holds everything to do with a HVI sequence. There cn be multiple sequences in a chassis,
    but any given module can only be involved in a single sequence. Also HVI sequencers
    rely on PXIe trigger bus to synchonise modules. Each sequencer needs dedicated access
    to some of these trigger lines, so be parsimonious with PXIe trigger assignment.
    If the modules and associated HVI sequence are in a seperate segment of the chassis,
    then they get  fresh set of PXIe trigger lines.
    """

    def __init__(
        self,
        name: str,
        modules: list[ModuleDescriptor],
        chassis_list: Tuple[int, ...] = (1,),
        pxi_triggers: Tuple[int, ...] | None = (
            0,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
        ),
        simulate: bool = False,
    ):
        """
        Parameters
        ---------

        name
            Name of the sequence to be created.
        modules
            A list of Module Descriptors for all the modules to be used in this
            HVI Sequence.
        chassis_list
            A list (tuple) of chassis numbers to be used. Typically this is just one chassis
            expessed by (1,); the default.
        pxi_triggers
            HVI uses pxi_trigger lines to synchronize between modules. This tuple defines
            the pxi_triggers that should be used. The default is to use all of them.
            If it is a single module HVI sequence and no synchronization is required use 'None'.
        simulate
            Used for debugging offline if there are no modules available.

        """
        # Inner classes that group commands into groups
        self.runtime = self.Runtime(self)
        self.sync = self.SyncBlock(self)
        self.hvi_register = self.HviRegister(self)
        self.fpga_register = self.FpgaRegister(self)
        self.triggers = self.Triggers(self)
        self.utils = self.Utils(self)

        self._modules = modules
        self._sequencer = None
        self._current_sync_sequence = deque()
        self._current_block = deque()
        self.hvi_handle = None
        self._system_definition = kthvi.SystemDefinition(name)
        for chassis in chassis_list:
            if simulate:
                self._system_definition.chassis.add_with_options(
                    chassis, "Simulate=True,DriverSetup=model=GenericChassis"
                )
            else:
                self._system_definition.chassis.add(chassis)

        # Add PXI trigger resources that we plan to use
        log.debug("Adding PXIe triggers to the HVI environment...")
        pxiTriggers = []
        for trigger in pxi_triggers:
            pxiTriggerName = "PXI_TRIGGER{}".format(trigger)
            log.debug(f"...adding: {pxiTriggerName}")
            pxiTrigger = getattr(kthvi.TriggerResourceId, pxiTriggerName)
            pxiTriggers.append(pxiTrigger)
        self._system_definition.sync_resources = pxiTriggers

        log.debug("Adding modules to the HVI environment...")
        for module in modules:
            log.debug(f"...adding: {module.name}")
            module._current_sequence = deque()
            self._system_definition.engines.add(
                module.handle.hvi.engines.main_engine, module.name
            )
            log.debug(f"...Declaring Input Triggers used by: {module.name}...")
            if module.input_triggers is not None:
                for trigger in module.input_triggers:
                    log.debug(f"...adding: {trigger}")
                    trigger_id = getattr(module.handle.hvi.triggers, trigger)
                    self._system_definition.engines[module.name].triggers.add(
                        trigger_id, trigger
                    )

            log.debug(f"...Declaring Output Triggers used by: {module.name}...")
            if module.output_triggers is not None:
                for trigger in module.output_triggers:
                    log.debug(f"...adding: {trigger}")
                    trigger_id = getattr(module.handle.hvi.triggers, trigger)
                    self._system_definition.engines[module.name].triggers.add(
                        trigger_id, trigger
                    )
                    self._system_definition.engines[module.name].triggers[
                        trigger
                    ].config.direction = kthvi.Direction.OUTPUT
                    self._system_definition.engines[module.name].triggers[
                        trigger
                    ].config.polarity = kthvi.Polarity.ACTIVE_HIGH
                    self._system_definition.engines[module.name].triggers[
                        trigger
                    ].config.sync_mode = kthvi.SyncMode.IMMEDIATE
                    self._system_definition.engines[module.name].triggers[
                        trigger
                    ].config.hw_routing_delay = 0
                    self._system_definition.engines[module.name].triggers[
                        trigger
                    ].config.trigger_mode = kthvi.TriggerMode.LEVEL

            log.debug(f"...Declaring actions used by: {module.name}...")
            if module.actions is not None:
                if len(module.actions) == 0:
                    actions = [
                        a
                        for a in dir(module.handle.hvi.actions)
                        if not a.startswith("_")
                    ]
                    module.actions = actions
                else:
                    actions = module.actions
                for action in actions:
                    log.debug(f"...adding: {action}")
                    action_id = getattr(module.handle.hvi.actions, action)
                    try:
                        self._system_definition.engines[module.name].actions.add(
                            action_id, action
                        )
                    except kthvi.Error:
                        log.warning(
                            f"Action {action} not found; could be licensing issue"
                        )
                        pass

            log.debug(f"...Declaring events used by: {module.name}...")
            if module.events is not None:
                if len(module.events) == 0:
                    events = [
                        e
                        for e in dir(module.handle.hvi.events)
                        if not e.startswith("_")
                    ]
                    module.events = events
                else:
                    events = module.events
                for event in events:
                    log.debug(f"...adding: {event}")
                    event_id = getattr(module.handle.hvi.events, event)
                    self._system_definition.engines[module.name].events.add(
                        event_id, event
                    )

            log.debug(f"...Mapping triggers to actions on: {module.name}...")
            if module.trigger_action_map is not None:
                for mapping in module.trigger_action_map.items():
                    log.debug(f"...connecting: {mapping[0]} -> (Action){mapping[1]}")
                    # Register trigger as an event so HVI knows about it
                    trigger_id = getattr(module.handle.hvi.triggers, mapping[0])
                    triggerEvent = self._system_definition.engines[
                        module.name
                    ].events.add(trigger_id, mapping[0])
                    # Set up the characteristics of the physical trigger
                    trigger = self._system_definition.engines[module.name].triggers[
                        mapping[0]
                    ]
                    trigger.config.direction = kthvi.Direction.INPUT
                    trigger.config.polarity = kthvi.Polarity.ACTIVE_HIGH
                    trigger.config.sync_mode = kthvi.SyncMode.IMMEDIATE
                    trigger.config.hw_routing_delay = 0
                    trigger.config.trigger_mode = kthvi.TriggerMode.PULSE
                    # Finally connect the trigger to the action input to the sandbox
                    action_id = getattr(module.handle.hvi.actions, mapping[1])
                    triggerAction = self._system_definition.engines[
                        module.name
                    ].actions[mapping[1]]
                    triggerAction.config.source = triggerEvent
                    triggerAction.config.sync_mode = kthvi.SyncMode.IMMEDIATE

            log.debug(f"...Mapping events to triggers on: {module.name}...")
            if module.event_trigger_map is not None:
                for mapping in module.event_trigger_map.items():
                    log.debug(f"...connecting: (Event){mapping[0]} -> {mapping[1]}")
                    # Set up the characteristics of the physical trigger
                    trigger_id = getattr(module.handle.hvi.triggers, mapping[1])
                    trigger = self._system_definition.engines[module.name].triggers[
                        mapping[1]
                    ]
                    trigger.config.direction = kthvi.Direction.OUTPUT
                    trigger.config.polarity = kthvi.Polarity.ACTIVE_HIGH
                    trigger.config.sync_mode = kthvi.SyncMode.IMMEDIATE
                    trigger.config.hw_routing_delay = 0
                    trigger.config.trigger_mode = kthvi.TriggerMode.LEVEL
                    # Connect the event output of the sandbox to the physical trigger
                    source_event = self._system_definition.engines[module.name].events[
                        mapping[0]
                    ]
                    trigger.config.source = source_event

            if module.fpga:
                log.debug(f"...Declaring FPGA Registers used by: {module.name}...")
                sandbox = self._system_definition.engines[module.name].fpga_sandboxes[0]
                try:
                    sandbox.load_from_k7z(os.getcwd() + "\\" + module.fpga)
                    log.debug(f"FDS ports: {sandbox.fds_ports.count}")
                    for register in (
                        self._system_definition.engines[module.name]
                        .fpga_sandboxes[0]
                        .fds_ports
                    ):
                        log.debug(f"...... {register.name}")
                    log.debug(f"Registers: {sandbox.fpga_registers.count}")
                    for register in (
                        self._system_definition.engines[module.name]
                        .fpga_sandboxes[0]
                        .fpga_registers
                    ):
                        log.debug(f"...... {register.name}")
                    log.debug(f"Memory Banks: {sandbox.fpga_memory_maps.count}")
                    for register in (
                        self._system_definition.engines[module.name]
                        .fpga_sandboxes[0]
                        .fpga_memory_maps
                    ):
                        log.debug(f"...... {register.name}")
                except Exception as err:
                    if err.args[0] == "No interface named 'MainEngine_Memory'":
                        log.debug("No HVI registers")
                    else:
                        raise err

        log.debug("Creating Main Sequencer Block...")
        self._sequencer = kthvi.Sequencer(f"{name}_Sequencer", self._system_definition)
        self._current_sync_sequence.append(self._sequencer.sync_sequence)

        log.debug("Declaring HVI registers...")
        scopes = self._sequencer.sync_sequence.scopes
        for module in modules:
            for register in module.hvi_registers:
                log.debug(
                    f"...Adding register: {register}, "
                    f"initial value: 0 to module: {module.name}"
                )
                registers = scopes[module.name].registers
                hviRegister = registers.add(register, kthvi.RegisterSize.SHORT)
                hviRegister.initial_value = 0
        log.debug("Finished Defining System")
        return

    # Helper Functions

    def _get_module(self, name):
        return [i for i in self._modules if i.name == name][0]

    def _get_current_sequence(self, module_name):
        return self._get_module(module_name)._current_sequence[-1]

    def _push_current_sequence(self, module_name, sequence):
        self._get_module(module_name)._current_sequence.append(sequence)

    def _pop_current_sequence(self, module_name):
        self._get_module(module_name)._current_sequence.pop()

    def _statement_name(self, sequence, name):
        statement_names = [
            s.name for s in sequence.statements if s.name.startswith(name)
        ]
        if len(statement_names) == 0:
            statement_name = name
        else:
            statement_name = f"{name}_{len(statement_names)}"
        return statement_name

    def _sync_statement_name(self, sequence, name):
        statement_names = [
            s.name for s in sequence.sync_statements if s.name.startswith(name)
        ]
        if len(statement_names) == 0:
            statement_name = name
        else:
            statement_name = f"{name}_{len(statement_names)}"
        return statement_name

    from ._sync_block import SyncBlock
    from ._hvi_register import HviRegister
    from ._fpga_register import FpgaRegister
    from ._triggers import Triggers
    from ._runtime import Runtime
    from ._utils import Utils

    def execute_actions(self, name, module, actions, delay=10):
        """
        Adds an instruction called <name> to sequence for <module> to the current block
        to execute all <actions>
        """
        sequence = self._get_current_sequence(module)
        statement_name = self._statement_name(sequence, name)
        log.debug(f"......{statement_name}")
        actionCmd = sequence.instruction_set.action_execute
        actionParams = [sequence.engine.actions[action] for action in actions]
        instruction = sequence.add_instruction(statement_name, delay, actionCmd.id)
        instruction.set_parameter(actionCmd.action.id, actionParams)

    def delay(self, name, module, delay=10):
        """
        Adds an instruction called <name> to sequence for <module> to the current block
        to delay for <delay> ns.
        """
        sequence = self._get_current_sequence(module)
        statement_name = self._statement_name(sequence, name)
        log.debug(f"......{statement_name}")
        sequence.add_delay(statement_name, delay)

    # AWG specific HVI Sequence Instructions

    def awg_set_amplitude(self, name, module, channel, value, delay=10):
        """
        Adds an instruction called <name> to <module>'s sequence to set amplitude
        of <channel> to <value>
        """
        module_name = module
        sequence = self._get_current_sequence(module)
        statement_name = self._statement_name(sequence, name)
        log.debug(f"......{name}")
        for module in self._modules:
            if module.name == module_name:
                break
        command = module.handle.hvi.instruction_set.set_amplitude
        instruction = sequence.add_instruction(statement_name, delay, command.id)
        instruction.set_parameter(command.channel.id, channel)
        instruction.set_parameter(command.value.id, value)
