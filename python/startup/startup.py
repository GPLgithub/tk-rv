
import sgtk
import os
from rv import rvtypes
from rv import commands as rvcommands

class ShotgunToolkitMode(rvtypes.MinorMode):
    """
    """
    _TK_RV_MODE_NAME = "Shotgun"
    def __init__(self):
        super(ShotgunToolkitMode, self).__init__()
        # INITIALIZE mode
        self.init(self._TK_RV_MODE_NAME, [], None, [("Shotgun", None)])

def start_toolkit():
    """
    Bootstrapping routine.
    """
    sg_tk_mode = ShotgunToolkitMode()
    sg_tk_mode.activate()
    context = sgtk.context.deserialize(os.environ.get("TANK_CONTEXT"))
    sgtk.platform.start_engine("tk-rv", context.sgtk, context)

    # Clean up temp env vars.
    # We don't clean up the TANK_CONTEXT or TANK_ENGINE a these get reset with the current context
    # and used if a new Nuke session is spawned from this one.
    if "TANK_FILE_TO_OPEN" in os.environ:
        del os.environ["TANK_FILE_TO_OPEN"]

start_toolkit()
