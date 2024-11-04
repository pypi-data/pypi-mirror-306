# -*- coding: utf-8 -*-
"""
This 'wraps' Keysight's PW Test Sync Executive functionlity to provide
a more usable interface. It simplifies creating the HVI sequencer.

A typical sequence is to:

- Define the resources available to HVI in the modules in the system
  by creating a 'ModuleDescriptor' dataclass instance for each module.

- Add the handle of the initilized driver instance to the 'ModuleDescriptor'.

- Define the resources available to HVI sequencer that is being created
  by calling 'define_system'.

- Define the actual sequence by adding HVI commands. These are actions
  that each module performs at defined times. For a multi-module system
  these are typically inside 'sync blocks'.

- Call the 'compile_load()' method to download the HVI sequence to
  the hardware.

- Call 'start()' to start the sequence.

- interact with the sequencer with 'read/write register_runtime()'
  calls.

- Call 'close()' to unload the sequence from HW and release all the resource.

Notes
-----

- Resources made available to HVI 'lock' them and the associated SW API
  calls will not be available. This is particularly true of 'actions'
  declared in module. e.g. 'awg1_trigger' stops the SW API being able to
  trigger that channel's awg queue.
"""

import os
import logging
from dataclasses import dataclass, field
from collections import deque
from typing import List, Tuple

import numpy as np

import keysight_tse as kthvi


log = logging.getLogger(__name__)

# Cached record of modules that are used in the HVI.
_modules = None
_system_definition = None
_sequencer = None
_current_sync_sequence = deque()
_current_block = deque()
hvi_handle = None


@dataclass
class ModuleDescriptor:
    """
    Defines all the resources that HVI is able to use for this module.
    The resources are generally lists of strings. If 'None' is supplied
    instead of the list, then no resources will be assigned for that group.
    If an empty list is supplied, then *all* available resources will be
    assigned.

    """

    name: str
    """
        The name given to the module. This can be anything that makes sense.
        It is used to identify which steps and actions are assigned to this
        module in the sequence definition.
    """
    handle: int = None
    """
        Used to hold the handle of the initialized driver for the module.
        This is to be supplied by the parent before declaring any HVI sequences.
    """
    fpga: str = None
    """
        path to the 'bitfile (.k7z)' for the loaded FPGA.
    """
    input_triggers: List[str] = field(default_factory=list)
    """
        Hardware triggers, e.g. PXIe triggers or SMB front panel triggers.
    """
    output_triggers: List[str] = field(default_factory=list)
    """
        Hardware triggers, e.g. PXIe triggers or SMB front panel triggers.
    """
    events: List[str] = field(default_factory=list)
    """
        internal things that HVI sequencer can test in order to make decisions.
        e.g. 'queue_empty' for the AWG.
    """
    actions: List[str] = field(default_factory=list)
    """
        internal things that the HVI sequencer can 'do' or control.
        e.g. 'enqueue_waveform' for the AWG.
    """
    hvi_registers: List[str] = field(default_factory=list)
    """
        List of register names that will be used for this module in the HVI
        sequence.
    """
    trigger_action_map: dict = field(default_factory=dict)
    """
    """
    event_trigger_map: dict = field(default_factory=dict)
    """
    """
    _current_sequence = None


def define_system(
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
    global _modules, _system_definition, _sequencer, _current_sync_sequence

    _modules = modules

    _system_definition = kthvi.SystemDefinition(name)
    for chassis in chassis_list:
        if simulate:
            _system_definition.chassis.add_with_options(
                chassis, "Simulate=True,DriverSetup=model=GenericChassis"
            )
        else:
            _system_definition.chassis.add(chassis)

    # Add PXI trigger resources that we plan to use
    log.debug("Adding PXIe triggers to the HVI environment...")
    pxiTriggers = []
    for trigger in pxi_triggers:
        pxiTriggerName = "PXI_TRIGGER{}".format(trigger)
        log.debug(f"...adding: {pxiTriggerName}")
        pxiTrigger = getattr(kthvi.TriggerResourceId, pxiTriggerName)
        pxiTriggers.append(pxiTrigger)
    _system_definition.sync_resources = pxiTriggers

    log.debug("Adding modules to the HVI environment...")
    for module in modules:
        log.debug(f"...adding: {module.name}")
        module._current_sequence = deque()
        _system_definition.engines.add(
            module.handle.hvi.engines.main_engine, module.name
        )
        log.debug(f"...Declaring Input Triggers used by: {module.name}...")
        if module.input_triggers is not None:
            for trigger in module.input_triggers:
                log.debug(f"...adding: {trigger}")
                trigger_id = getattr(module.handle.hvi.triggers, trigger)
                _system_definition.engines[module.name].triggers.add(
                    trigger_id, trigger
                )

        log.debug(f"...Declaring Output Triggers used by: {module.name}...")
        if module.output_triggers is not None:
            for trigger in module.output_triggers:
                log.debug(f"...adding: {trigger}")
                trigger_id = getattr(module.handle.hvi.triggers, trigger)
                _system_definition.engines[module.name].triggers.add(
                    trigger_id, trigger
                )
                _system_definition.engines[module.name].triggers[
                    trigger
                ].config.direction = kthvi.Direction.OUTPUT
                _system_definition.engines[module.name].triggers[
                    trigger
                ].config.polarity = kthvi.Polarity.ACTIVE_HIGH
                _system_definition.engines[module.name].triggers[
                    trigger
                ].config.sync_mode = kthvi.SyncMode.IMMEDIATE
                _system_definition.engines[module.name].triggers[
                    trigger
                ].config.hw_routing_delay = 0
                _system_definition.engines[module.name].triggers[
                    trigger
                ].config.trigger_mode = kthvi.TriggerMode.LEVEL

        log.debug(f"...Declaring actions used by: {module.name}...")
        if module.actions is not None:
            if len(module.actions) == 0:
                actions = [
                    a for a in dir(module.handle.hvi.actions) if not a.startswith("_")
                ]
                module.actions = actions
            else:
                actions = module.actions
            for action in actions:
                log.debug(f"...adding: {action}")
                action_id = getattr(module.handle.hvi.actions, action)
                try:
                    _system_definition.engines[module.name].actions.add(
                        action_id, action
                    )
                except kthvi.Error:
                    log.warning(f"Action {action} not found; could be licensing issue")
                    pass

        log.debug(f"...Declaring events used by: {module.name}...")
        if module.events is not None:
            if len(module.events) == 0:
                events = [
                    e for e in dir(module.handle.hvi.events) if not e.startswith("_")
                ]
                module.events = events
            else:
                events = module.events
            for event in events:
                log.debug(f"...adding: {event}")
                event_id = getattr(module.handle.hvi.events, event)
                _system_definition.engines[module.name].events.add(event_id, event)

        log.debug(f"...Mapping triggers to actions on: {module.name}...")
        if module.trigger_action_map is not None:
            for mapping in module.trigger_action_map.items():
                log.debug(f"...connecting: {mapping[0]} -> (Action){mapping[1]}")
                # Register trigger as an event so HVI knows about it
                trigger_id = getattr(module.handle.hvi.triggers, mapping[0])
                triggerEvent = _system_definition.engines[module.name].events.add(
                    trigger_id, mapping[0]
                )
                # Set up the characteristics of the physical trigger
                trigger = _system_definition.engines[module.name].triggers[mapping[0]]
                trigger.config.direction = kthvi.Direction.INPUT
                trigger.config.polarity = kthvi.Polarity.ACTIVE_HIGH
                trigger.config.sync_mode = kthvi.SyncMode.IMMEDIATE
                trigger.config.hw_routing_delay = 0
                trigger.config.trigger_mode = kthvi.TriggerMode.PULSE
                # Finally connect the trigger to the action input to the sandbox
                action_id = getattr(module.handle.hvi.actions, mapping[1])
                triggerAction = _system_definition.engines[module.name].actions[
                    mapping[1]
                ]
                triggerAction.config.source = triggerEvent
                triggerAction.config.sync_mode = kthvi.SyncMode.IMMEDIATE

        log.debug(f"...Mapping events to triggers on: {module.name}...")
        if module.event_trigger_map is not None:
            for mapping in module.event_trigger_map.items():
                log.debug(f"...connecting: (Event){mapping[0]} -> {mapping[1]}")
                # Set up the characteristics of the physical trigger
                trigger_id = getattr(module.handle.hvi.triggers, mapping[1])
                trigger = _system_definition.engines[module.name].triggers[mapping[1]]
                trigger.config.direction = kthvi.Direction.OUTPUT
                trigger.config.polarity = kthvi.Polarity.ACTIVE_HIGH
                trigger.config.sync_mode = kthvi.SyncMode.IMMEDIATE
                trigger.config.hw_routing_delay = 0
                trigger.config.trigger_mode = kthvi.TriggerMode.LEVEL
                # Connect the event output of the sandbox to the physical trigger
                source_event = _system_definition.engines[module.name].events[
                    mapping[0]
                ]
                trigger.config.source = source_event

        if module.fpga:
            log.debug(f"...Declaring FPGA Registers used by: {module.name}...")
            sandbox = _system_definition.engines[module.name].fpga_sandboxes[0]
            try:
                sandbox.load_from_k7z(os.getcwd() + "\\" + module.fpga)
                log.debug(f"FDS ports: {sandbox.fds_ports.count}")
                for register in (
                    _system_definition.engines[module.name].fpga_sandboxes[0].fds_ports
                ):
                    log.debug(f"...... {register.name}")
                log.debug(f"Registers: {sandbox.fpga_registers.count}")
                for register in (
                    _system_definition.engines[module.name]
                    .fpga_sandboxes[0]
                    .fpga_registers
                ):
                    log.debug(f"...... {register.name}")
                log.debug(f"Memory Banks: {sandbox.fpga_memory_maps.count}")
                for register in (
                    _system_definition.engines[module.name]
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
    _sequencer = kthvi.Sequencer(f"{name}_Sequencer", _system_definition)
    _current_sync_sequence.append(_sequencer.sync_sequence)

    log.debug("Declaring HVI registers...")
    scopes = _sequencer.sync_sequence.scopes
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


def compile_load():
    """
    Compile the HVI sequence and load into HW. Can take several seconds.

    This is best called, after the sequence has been defined, soon after the
    modules have been initialised. This allows multiple 'runs' of the sequence
    without reloading the HVI sequence.
    """
    global hvi_handle
    log.info("Compiling HVI...")
    hvi_handle = _sequencer.compile()
    log.info("Loading HVI to HW...")
    hvi_handle.load_to_hw()


def start():
    """Start the HVI sequence."""
    log.info("Starting HVI...")
    hvi_handle.run(hvi_handle.no_wait)
    return


def close():
    """Close the HVI sequence, unload it from HW, and unlock any assigned hardware"""
    log.info("Releasing HVI...")
    hvi_handle.release_hw()


def show_sequencer():
    return _sequencer.sync_sequence.to_string(kthvi.OutputFormat.DEBUG)


# Helper Functions


def _get_module(name):
    return [i for i in _modules if i.name == name][0]


def _get_current_sequence(module_name):
    return _get_module(module_name)._current_sequence[-1]


def _push_current_sequence(module_name, sequence):
    _get_module(module_name)._current_sequence.append(sequence)


def _pop_current_sequence(module_name):
    _get_module(module_name)._current_sequence.pop()


def _statement_name(sequence, name):
    statement_names = [s.name for s in sequence.statements if s.name.startswith(name)]
    if len(statement_names) == 0:
        statement_name = name
    else:
        statement_name = f"{name}_{len(statement_names)}"
    return statement_name


def _sync_statement_name(sequence, name):
    statement_names = [
        s.name for s in sequence.sync_statements if s.name.startswith(name)
    ]
    if len(statement_names) == 0:
        statement_name = name
    else:
        statement_name = f"{name}_{len(statement_names)}"
    return statement_name


# Setup resources Statements


def setup_triggers(
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
            _system_definition.engines[module_name].triggers[
                trigger
            ].config.direction = kthvi.Direction.OUTPUT
        elif direction.upper() == "INPUT":
            _system_definition.engines[module_name].triggers[
                trigger
            ].config.direction = kthvi.Direction.INPUT
        else:
            raise ValueError(
                "If specified, trigger direction should be 'INPUT' or 'OUTPUT'"
            )

        if polarity is None:
            pass
        elif polarity.upper() == "ACTIVE_HIGH":
            _system_definition.engines[module_name].triggers[
                trigger
            ].config.polarity = kthvi.Polarity.ACTIVE_HIGH
        elif polarity.upper() == "ACTIVE_LOW":
            _system_definition.engines[module_name].triggers[
                trigger
            ].config.polarity = kthvi.Polarity.ACTIVE_LOW
        else:
            raise ValueError(
                "If specified, trigger polarity should be 'ACTIVE_HIGH' or 'ACTIVE_LOW'"
            )

        if sync is None:
            pass
        elif sync.upper() == "SYNC":
            _system_definition.engines[module_name].triggers[
                trigger
            ].config.sync_mode = kthvi.SyncMode.SYNC
        elif sync.upper() == "IMMEDIATE":
            _system_definition.engines[module_name].triggers[
                trigger
            ].config.sync_mode = kthvi.SyncMode.IMMEDIATE
        else:
            raise ValueError(
                "If specified, trigger sync should be 'SYNC' or 'IMMEDIATE'"
            )

        if hw_delay is None:
            pass
        else:
            _system_definition.engines[module_name].triggers[
                trigger
            ].config.hw_routing_delay = hw_delay

        if mode is None:
            pass
        elif mode == 0:
            _system_definition.engines[module_name].triggers[
                trigger
            ].config.trigger_mode = kthvi.TriggerMode.LEVEL
        else:
            _system_definition.engines[module_name].triggers[
                trigger
            ].config.trigger_mode = kthvi.TriggerMode.PULSE
            _system_definition.engines[module_name].triggers[
                trigger
            ].config.pulse_length = mode


# Synchronous Block Statements


def start_syncWhile_register(
    name: str, engine: str, register: str, comparison: str, value: int, delay: int = 70
):
    """
    | Synchronous (across all modules) while loop. Compares <register> (hosted by module <engine>) with <value>
      using <comparison>.
    | Must be closed with 'end_syncWhile()'.
    | Typically this will have a 'sync multi sequence block' within the while loop.

    Parameters
    ----------
    name
        title given to this instruction.
    engine
        name of module hosting the comparison register. (from Module_description.name)
    register
        name of register used for comparison (the 'comparison register').
    comparison
        the comparison operator:

        - 'EQUAL_TO'
        - 'GREATER_THAN'
        - 'GREATER_THEN_OR_EQUAL_TO'
        - 'LESS_THAN'
        - 'LESS_THAN_OR_EQUAL_TO'
        - 'NOT_EQUAL_TO'
    value
        value for the <register> to be compared to.
    """
    global _current_sync_sequence
    sequence = _current_sync_sequence[-1]
    statement_name = _sync_statement_name(sequence, name)
    whileRegister = _sequencer.sync_sequence.scopes[engine].registers[register]
    comparison_operator = getattr(kthvi.ComparisonOperator, comparison)

    log.debug(f"Creating Synchronized While loop, {value} iterations...")
    condition = kthvi.Condition.register_comparison(
        whileRegister, comparison_operator, value
    )
    while_sequence = sequence.add_sync_while(statement_name, delay, condition)
    _current_sync_sequence.append(while_sequence.sync_sequence)
    return


def end_syncWhile():
    global _current_sync_sequence
    _current_sync_sequence.pop()
    return


def start_sync_multi_sequence_block(name: str, delay: int = 30):
    global _current_block, _modules
    sequence = _current_sync_sequence[-1]
    statement_name = _sync_statement_name(sequence, name)
    block = sequence.add_sync_multi_sequence_block(statement_name, delay)
    _current_block.append(block)
    for module in _modules:
        module._current_sequence.append(block.sequences[module.name])
    return


def end_sync_multi_sequence_block():
    global _current_block
    _current_block.pop()
    for module in _modules:
        module._current_sequence.pop()


# Native HVI Sequence Instructions


def wait_trigger(name: str, module: str, trigger: str, delay: int = 10):
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
    sequence = _get_current_sequence(module)
    statement_name = _statement_name(sequence, name)
    log.debug(f"......{statement_name}")
    condition = kthvi.Condition.trigger(
        _system_definition.engines[module].triggers[trigger]
    )
    instruction = sequence.add_wait(statement_name, delay, condition)
    instruction.set_mode(kthvi.WaitMode.TRANSITION, kthvi.SyncMode.IMMEDIATE)


def if_register_comparison(name, module, register, comparison, value, delay=10):
    """
    Inserts an 'if' statement in the flow following instructions
    are only executed if condition evalutes to True. This should be terminated
    with 'end_if()' statement.
    """
    sequence = _get_current_sequence(module)
    statement_name = _statement_name(sequence, name)
    comparison_operator = getattr(kthvi.ComparisonOperator, comparison)
    if_condition = kthvi.Condition.register_comparison(
        register, comparison_operator, value
    )
    enable_matching_branches = True
    if_statement = sequence.add_if(
        statement_name, delay, if_condition, enable_matching_branches
    )
    _push_current_sequence(module, if_statement.if_branch.sequence)


def end_if(module):
    _pop_current_sequence(module)


def set_register(name: str, module: str, register: str, value: int, delay: int = 10):
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
    sequence = _get_current_sequence(module)
    statement_name = _statement_name(sequence, name)
    register_id = sequence.scope.registers[register]
    log.debug(f"......{statement_name}")
    instruction = sequence.add_instruction(
        statement_name, delay, sequence.instruction_set.assign.id
    )
    instruction.set_parameter(
        sequence.instruction_set.assign.destination.id, register_id
    )
    instruction.set_parameter(sequence.instruction_set.assign.source.id, value)


def incrementRegister(name: str, module: str, register: str, delay: int = 10):
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
    addToRegister(name, module, register, 1, delay)


def addToRegister(name: str, module: str, register: str, value: int, delay: int = 10):
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
    sequence = _get_current_sequence(module)
    statement_name = _statement_name(sequence, name)
    register_id = sequence.scope.registers[register]
    log.debug(f"......{statement_name}")
    instruction = sequence.add_instruction(
        statement_name, delay, sequence.instruction_set.add.id
    )
    instruction.set_parameter(sequence.instruction_set.add.destination.id, register_id)
    instruction.set_parameter(sequence.instruction_set.add.left_operand.id, register_id)
    instruction.set_parameter(sequence.instruction_set.add.right_operand.id, value)


def writeFpgaMemRegister(
    name: str, module: str, bank: str, offset: int, value: int | str, delay=10
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
    sequence = _get_current_sequence(module)
    statement_name = _statement_name(sequence, name)
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


def readFpgaMemRegister(
    name: str, module: str, bank: str, offset: int, hvi_register: str, delay: int = 10
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
    sequence = _get_current_sequence(module)
    statement_name = _statement_name(sequence, name)
    bank_id = sequence.engine.fpga_sandboxes[0].fpga_memory_maps[bank]
    log.debug(f"......{statement_name}")
    cmd = sequence.instruction_set.fpga_array_read
    instruction = sequence.add_instruction(statement_name, delay, cmd.id)
    instruction.set_parameter(cmd.fpga_memory_map.id, bank_id)
    instruction.set_parameter(cmd.fpga_memory_map_offset.id, offset)
    dest_register = sequence.scope.registers[hvi_register]
    instruction.set_parameter(cmd.destination.id, dest_register)
    return


def writeFpgaRegister(
    name: str, module: str, register: str, value: int | str, delay: int = 10
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
    sequence = _get_current_sequence(module)
    statement_name = _statement_name(sequence, name)
    register_id = sequence.engine.fpga_sandboxes[0].fpga_registers[register]
    log.debug(f"......{statement_name}")
    reg_cmd = sequence.instruction_set.fpga_register_write
    instruction = sequence.add_instruction(statement_name, delay, reg_cmd.id)
    instruction.set_parameter(reg_cmd.fpga_register.id, register_id)
    if type(value) is str:
        value = sequence.scope.registers[value]
    instruction.set_parameter(reg_cmd.value.id, value)
    return


def readFpgaRegister(
    name: str, module: str, fpga_register: str, hvi_register: str, delay=10
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
    sequence = _get_current_sequence(module)
    statement_name = _statement_name(sequence, name)
    register_id = sequence.engine.fpga_sandboxes[0].fpga_registers[fpga_register]
    log.debug(f"......{statement_name}")
    reg_cmd = sequence.instruction_set.fpga_register_read
    instruction = sequence.add_instruction(statement_name, delay, reg_cmd.id)
    instruction.set_parameter(reg_cmd.fpga_register.id, register_id)
    dest_register = sequence.scope.registers[hvi_register]
    instruction.set_parameter(reg_cmd.destination.id, dest_register)
    return


def execute_actions(name, module, actions, delay=10):
    """
    Adds an instruction called <name> to sequence for <module> to the current block
    to execute all <actions>
    """
    sequence = _get_current_sequence(module)
    statement_name = _statement_name(sequence, name)
    log.debug(f"......{statement_name}")
    actionCmd = sequence.instruction_set.action_execute
    actionParams = [sequence.engine.actions[action] for action in actions]
    instruction = sequence.add_instruction(statement_name, delay, actionCmd.id)
    instruction.set_parameter(actionCmd.action.id, actionParams)


def assert_triggers(name, module, triggers, delay=10):
    """
    Adds an instruction called <name> to sequence for <module> to the current block
    to assert all <triggers>
    triggers can be pxi0..pxi7 (but only if not committed to HVI system), smb1..smb8
    """
    sequence = _get_current_sequence(module)
    statement_name = _statement_name(sequence, name)
    log.debug(f"......{statement_name}")
    triggerCmd = sequence.instruction_set.trigger_write
    triggerParams = [sequence.engine.triggers[trigger] for trigger in triggers]
    instruction = sequence.add_instruction(statement_name, delay, triggerCmd.id)
    instruction.set_parameter(triggerCmd.trigger.id, triggerParams)
    instruction.set_parameter(triggerCmd.sync_mode.id, kthvi.SyncMode.IMMEDIATE)
    instruction.set_parameter(triggerCmd.value.id, kthvi.TriggerValue.ON)


def disassert_triggers(name, module, triggers, delay=10):
    """
    Adds an instruction called <name> to sequence for <module> to the current block
    to disassert all <triggers>
    triggers can be pxi0..pxi7 (but only if not committed to HVI system), smb1..smb8
    """
    sequence = _get_current_sequence(module)
    statement_name = _statement_name(sequence, name)
    log.debug(f"......{statement_name}")
    triggerCmd = sequence.instruction_set.trigger_write
    triggerParams = [sequence.engine.triggers[trigger] for trigger in triggers]
    instruction = sequence.add_instruction(statement_name, delay, triggerCmd.id)
    instruction.set_parameter(triggerCmd.trigger.id, triggerParams)
    instruction.set_parameter(triggerCmd.sync_mode.id, kthvi.SyncMode.IMMEDIATE)
    instruction.set_parameter(triggerCmd.value.id, kthvi.TriggerValue.OFF)


def delay(name, module, delay=10):
    """
    Adds an instruction called <name> to sequence for <module> to the current block
    to delay for <delay> ns.
    """
    sequence = _get_current_sequence(module)
    statement_name = _statement_name(sequence, name)
    log.debug(f"......{statement_name}")
    sequence.add_delay(statement_name, delay)


# AWG specific HVI Sequence Instructions


def awg_set_amplitude(name, module, channel, value, delay=10):
    """
    Adds an instruction called <name> to <module>'s sequence to set amplitude
    of <channel> to <value>
    """
    module_name = module
    sequence = _get_current_sequence(module)
    statement_name = _statement_name(sequence, name)
    log.debug(f"......{name}")
    for module in _modules:
        if module.name == module_name:
            break
    command = module.handle.hvi.instruction_set.set_amplitude
    instruction = sequence.add_instruction(statement_name, delay, command.id)
    instruction.set_parameter(command.channel.id, channel)
    instruction.set_parameter(command.value.id, value)


# Runtime commands. These can be executed by the host to interact with the HVI sequencer
def read_register_runtime(module, register):
    register_runtime = hvi_handle.sync_sequence.scopes[module].registers[register]
    value = register_runtime.read()
    return value


def write_register_runtime(module, register, value):
    register_runtime = hvi_handle.sync_sequence.scopes[module].registers[register]
    register_runtime.write(value)
    return value


def write_fpga_register_mem_runtime(
    module: str, bank: str, offset: int, value: int
) -> None:
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
        hvi_handle.sync_sequence.engines[module]
        .fpga_sandboxes[0]
        .fpga_memory_maps[bank]
    )
    register_runtime.write(offset, np.uint32(value))
