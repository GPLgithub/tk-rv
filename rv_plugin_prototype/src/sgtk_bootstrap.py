# Copyright (c) 2016 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import logging
import cgi
import sys
import os

from PySide import QtCore

from pymu import MuSymbol

import rv
import rv.rvtypes as rvt
import rv.commands as rvc
import rv.extra_commands as rve

class ToolkitBootstrap(rvt.MinorMode):
    """
    An RV mode that will handle bootstrapping SGTK and starting
    up the tk-rv engine. The mode expects an installation of
    tk-core to be present in the same directory underneath an
    "sgtk_core" subdirectory. Alternatively, an environment variable
    "TK_CORE" can be set to an alternate installation of tk-core
    to override the default behavior.
    """
    def __init__(self):
        """
        Initializes the RV mode. An environment variable "TK_RV_MODE_NAME"
        will be set to the name of this mode. That variable can then be
        used by other logic to generate menu items in RV associated with
        this mode.
        """
        super(ToolkitBootstrap, self).__init__()

        self._mode_name = "sgtk_bootstrap"
        self.init(self._mode_name, None,
                [
                    ("external-gma-play-entity", self.externalGMAPlayEntity, "")
                ],
                [("SG Review", [
                    ("HTTP Server", None, None, lambda: rvc.DisabledMenuState),
                    ("    Start Server", self.httpServerSetup, None, lambda: rvc.UncheckedMenuState),
                    ("    Test Certificate", self.testCert, None, lambda: rvc.UncheckedMenuState),
                    ("GMA WebView", self.gmaWebView, None, lambda: rvc.UncheckedMenuState),
                    ("_", None)],
                )])

        self.httpServerThread = None
        self.webview = None
        self.server_url = None

        # The menu generation code makes use of the TK_RV_MODE_NAME environment
        # variable. Each menu item that is created in RV is associated with a
        # mode identified by its name. We need to make a note of our name so we
        # can add menu items for this mode later.

        os.environ["TK_RV_MODE_NAME"] = self._mode_name

    def gmaWebView (self, event) :

        # rv.runtime.eval("require sgtk_webview_gma;", [])
        # MuSymbol("sgtk_webview_gma.makeOne")()

        import sgtk_webview_gma

        self.webview = sgtk_webview_gma.pyGMAWindow(self.server_url)

    def externalGMAPlayEntity(self, event):
        self.httpEventCallback(event.name(), event.contents())

    def httpEventCallback(self, name, contents) :
        log.debug("callback ---------------------------- current thread " + str(QtCore.QThread.currentThread()))
        rve.displayFeedback(name + " " + contents, 2.5)
        if (name == "external-gma-play-entity") :
            rvc.stop()
            log.debug("callback sendEvent %s '%s'" % (name, contents))
            rvc.sendInternalEvent("id_from_gma", contents)
            rvc.redraw()
            rvc.play()
        
    def httpServerSetup(self, event) :
        import sgtk_rvserver
        log.debug("\n\n")
        self.httpServerThread = sgtk_rvserver.RvServerThread(self.httpEventCallback)
        self.httpServerThread.start()
        log.debug("\n\n")

    def testCert(self, event) :

        # Start up server if it's not already going
        if (not self.httpServerThread) :
            self.httpServerSetup(None)

        # Get port number from server itself
        url = "https://localhost:" + str(self.httpServerThread.httpServer.server_address[1])
        log.debug("open url: '%s'" % url)
        rvc.openUrl(url)

    def activate(self):
        """
        Activates the RV mode and bootstraps SGTK.
        """
        rvt.MinorMode.activate(self)

        core = os.path.join(os.path.dirname(__file__), "sgtk_core")
        core = os.environ.get("TK_CORE") or core

        # append python path to get to the actual code
        core = os.path.join(core, "python")

        log.info("Looking for tk-core here: %s" % str(core))

        # now we can kick off sgtk
        sys.path.append(core)

        # import bootstrapper
        from tank_vendor import shotgun_base, shotgun_deploy, shotgun_authentication

        # import authentication code
        from sgtk_auth import get_toolkit_user

        # bind toolkit logging to our logger
        sgtk_root_logger = shotgun_base.get_sgtk_logger()
        sgtk_root_logger.setLevel(logging.WARNING)
        sgtk_root_logger.addHandler(log_handler)

        # Get an authenticated user object from rv's security architecture
        (user, url) = get_toolkit_user()
        self.server_url = url
        log.info("Will connect using %r" % user)

        # Now do the bootstrap!
        log.info("Ready for bootstrap!")
        mgr = shotgun_deploy.ToolkitManager(user)

        # Hint bootstrapper about our namespace so that we don't pick
        # the site config for Maya or Desktop.
        mgr.namespace = "rv"

        mgr.base_configuration = dict(
            # type="dev",
            # path=r"d:\repositories\tk-config-rv",
            path="git@github.com:shotgunsoftware/tk-config-rv.git",
            type="git_branch",
            branch="master",
            version="latest",
        )

        # Bootstrap the tk-rv engine into an empty context!
        mgr.bootstrap_engine("tk-rv")
        log.info("Bootstrapping process complete!")


    def deactivate(self):
        """
        Deactivates the mode and tears down the currently-running
        SGTK engine.
        """
        import sgtk
        rvt.MinorMode.deactivate(self)

        log.info("Shutting down engine...")

        if sgtk.platform.current_engine():
            sgtk.platform.current_engine().destroy()

        log.info("Engine is down.")


###############################################################################
# functions

def createMode():
    """
    Required to initialize the module. RV will call this function
    to create your mode.
    """
    return ToolkitBootstrap()


###############################################################################
# logging

log = logging.getLogger("sgtk_rv_bootstrap")
log.setLevel(logging.INFO)

class EscapedHtmlFormatter(logging.Formatter):
    def __init__(self, fmt, datefmt=None):
        logging.Formatter.__init__(self, fmt, datefmt)

    def format(self, record):
        result = logging.Formatter.format(self, record)
        return cgi.escape(result)

log_handler = logging.StreamHandler()
log_handler.setFormatter(
    EscapedHtmlFormatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
)
log.addHandler(log_handler)
