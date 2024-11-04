import logging

import keysight_tse as kthvi

log = logging.getLogger(__name__)


class Utils:
    def __init__(self, parent):
        self.parent = parent

    def compile_load(self):
        """
        Compile the HVI sequence and load into HW. Can take several seconds.

        This is best called, after the sequence has been defined, soon after the
        modules have been initialised. This allows multiple 'runs' of the sequence
        without reloading the HVI sequence.
        """
        log.info("Compiling HVI...")
        self.parent.hvi_handle = self.parent._sequencer.compile()
        log.info("Loading HVI to HW...")
        self.parent.hvi_handle.load_to_hw()

    def start(self):
        """Start the HVI sequence."""
        log.info("Starting HVI...")
        self.parent.hvi_handle.run(self.parent.hvi_handle.no_wait)
        return

    def close(self):
        """Close the HVI sequence, unload it from HW, and unlock any assigned hardware"""
        log.info("Releasing HVI...")
        self.parent.hvi_handle.release_hw()

    def show_sequencer(self):
        return self.parent._sequencer.sync_sequence.to_string(kthvi.OutputFormat.DEBUG)
