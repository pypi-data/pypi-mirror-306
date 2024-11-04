from dataclasses import dataclass, field
from typing import List, Tuple


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
