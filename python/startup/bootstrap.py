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
    RV.
    """
    import sgtk
    engine = sgtk.platform.current_engine()

    # Startup script
    startup_path = os.path.normpath(
        os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "startup.py"
        ) # tk-rv/startup
    )
    # Disable standard integration which ships with RV
    os.environ["RV_SHOTGUN_NO_SG_REVIEW_MENU"] = "1"
    # Enable debug.
    os.environ["RV_TK_LOG_DEBUG"] = "1"
    # TODO: have a clean way to clean up the path
    os.environ["PATH"] = "/usr/bin:/bin:/usr/sbin:/sbin"

    # Tell RV to run the startup script.
    app_args = "-pyeval 'import runpy; runpy.run_path(\"%s\");'" % (
        startup_path
    )
    return (app_path, app_args)
