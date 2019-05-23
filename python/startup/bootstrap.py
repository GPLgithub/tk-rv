# Copyright (c) 2016 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import os
import sys


def bootstrap(engine_name, context, app_path, app_args, extra_args):
    """
    Prepares for the bootstrapping process that will run during startup of
    Nuke, Hiero, and Nuke Studio.
    .. NOTE:: For detailed documentation of the bootstrap process for Nuke,
              Hiero, and Nuke Studio, see the engine documentation in
              `tk-nuke/engine.py`.
    """
    import sgtk
    engine = sgtk.platform.current_engine()

    startup_path = os.path.normpath(
        os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "startup.py"
        ) # tk-rv/startup
    )

    os.environ["RV_SHOTGUN_NO_SG_REVIEW_MENU"] = "1"
    os.environ["RV_TK_LOG_DEBUG"] = "1"

#    file_to_open = os.environ.get("TANK_FILE_TO_OPEN")
#
#    if file_to_open:
#        if app_args:
#            app_args = "%s %s" % (file_to_open, app_args)
#        else:
#            app_args = file_to_open
    app_args = "-pyeval 'import runpy; runpy.run_path(\"%s\");'" % (
        startup_path
    )
    return (app_path, app_args)
