from PySide.QtCore import QFile
from PySide import QtGui, QtCore

import types
import os
import math
import rv
import rv.qtutils
import tank

shotgun_view = tank.platform.import_framework("tk-framework-qtwidgets", "views")
shotgun_model = tank.platform.import_framework("tk-framework-shotgunutils", "shotgun_model")

from .version_list_delegate import RvVersionListDelegate
from .shot_info_delegate import RvShotInfoDelegate
from .tray_delegate import RvTrayDelegate

def groupMemberOfType(node, memberType):
    for n in rv.commands.nodesInGroup(node):
        if rv.commands.nodeType(n) == memberType:
            return n
    return None

class RvActivityMode(rv.rvtypes.MinorMode):


        # def sourceSetup (self, event):
        #         print "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& sourceSetup"
        #         print event.contents()

        #         #
        #         #  event.reject() is done to allow other functions bound to
        #         #  this event to get a chance to modify the state as well. If
        #         #  its not rejected, the event will be eaten and no other call
        #         #  backs will occur.
        #         #

        #         event.reject()
 
        #         args         = event.contents().split(";;")
        #         group        = args[0]
        #         fileSource   = groupMemberOfType(group, "RVFileSource")
        #         imageSource  = groupMemberOfType(group, "RVImageSource")
        #         source       = fileSource if imageSource == None else imageSource
        #         typeName     = rv.commands.nodeType(source)
        #         fileNames    = rv.commands.getStringProperty("%s.media.movie" % source, 0, 1000)
        #         fileName     = fileNames[0]
        #         ext          = fileName.split('.')[-1].upper()
        #         mInfo        = rv.commands.sourceMediaInfo(source, None)
        #         print "group: %s fileSource: %s fileName: %s" % (group, fileSource, fileName)
        #         propName = "%s.%s" % (fileSource, "tracking.info")
                
        #         self.propName = propName
        #         self.group = group
        #         try:
        #                 tl = rv.commands.getStringProperty(propName)
        #                 print tl
        #                 #import ast
        #                 #tl = ast.literal_eval(tracking_str)
        #                 self._tracking_info= {}
                        
        #                 for i in range(0,len(tl)-1, 2):
        #                         self._tracking_info[tl[i]] = tl[i+1]
        #                 print self._tracking_info

        #                 # make an entity
        #                 entity = {}
        #                 entity["type"] = "Version"
        #                 entity["id"] = int(self._tracking_info['id'])
        #                 print entity
        #                 self.load_data(entity)
        #                 self.version_activity_stream.ui.shot_info_widget.load_data_rv(self._tracking_info)

        #         except Exception as e:
        #                 print "OH NO %r" % e

        def beforeSessionRead (self, event):
                print "################### beforeSessionRead"
                event.reject()

                self._readingSession = True

        def afterSessionRead (self, event):
                print "################### afterSessionRead"
                event.reject()

                self._readingSession = False

        def inputsChanged(self, event):
                pass
                print "################### inputsChanged %r" % event
                print event.contents()
                event.reject()
                try:
                        fileSource   = rv.commands.nodesOfType("#RVSource")
                        self.propName =  "%s.%s" % (fileSource[0], "tracking.info")
                        tl = rv.commands.getStringProperty(self.propName)
 
                        self._tracking_info= {}
                        
                        for i in range(0,len(tl)-1, 2):
                                self._tracking_info[tl[i]] = tl[i+1]
 
                        # make an entity
                        entity = {}
                        entity["type"] = "Version"
                        entity["id"] = int(self._tracking_info['id'])
                        if event.contents() == "viewGroup":
                                self.load_data(entity)
                                #self.version_activity_stream.ui.shot_info_widget.load_data_rv(self._tracking_info)

                except Exception as e:
                        pass
                        # print "OH NO %r" % e

        def viewChange(self, event):
                pass
                print "################### viewChange %r" % event
                print event.contents()
                event.reject()

        def frameChanged(self, event):
                # print "################### frameChanged %r" % event
                # print event.contents()
                event.reject()
                # try:
                #         tl = rv.commands.getStringProperty(self.propName)

                #         # self._tracking_info= {}
                        
                #         # for i in range(0,len(tl)-1, 2):
                #         #         self._tracking_info[tl[i]] = tl[i+1]
                #         # print self._tracking_info

                #         # make an entity
                #         entity = {}
                #         entity["type"] = "Version"
                #         entity["id"] = int(self._tracking_info['id'])
                        
                #         self.load_data(entity)
                        
                #         #self.version_activity_stream.ui.shot_info_widget.load_data_rv(self._tracking_info)

                # except Exception as e:
                #         pass
                        # print "OH NO %r" % e

        def sourcePath(self, event):
                pass
                print "################### sourcePath %r" % event
                print event.contents()
                event.reject()

        def graphStateChange(self, event):
                pass
                print "################### graphStateChange %r" % event
                print event.contents()
                event.reject()
                if "tracking.info" in event.contents():
                        try:
                                tl = rv.commands.getStringProperty(event.contents())
                                if "infoStatus" not in event.contents():
                                        self._tracking_info= {}
                                        
                                        for i in range(0,len(tl)-1, 2):
                                                self._tracking_info[tl[i]] = tl[i+1]
                                        
                                        # make an entity
                                        entity = {}
                                        entity["type"] = "Version"
                                        entity["id"] = int(self._tracking_info['id'])
                                        
                                        self.load_data(entity)
                                        # self.version_activity_stream.ui.shot_info_widget.load_data_rv(self._tracking_info)

                                        s = self._tracking_info['shot']
                                        (s_id, s_name, s_type) = s.split('|')
                                        (n, shot_id) = s_id.split('_')
                
                                        # display VERSION info not parent shot info
                                        # shot_filters = [ ['id','is', entity['id']] ]
                                        # self.shot_info_model.load_data(entity_type="Version", filters=shot_filters)

                                        # version_filters = [ ['project','is', {'type':'Project','id':71}],
                                        #     ['entity','is',{'type':'Shot','id': int(shot_id) }] ]
                                        version_filters = [ ['entity','is',{'type':'Shot','id': int(shot_id) }] ]
                                        
                                        self.version_model.load_data(entity_type="Version", filters=version_filters)

                                        
                        except Exception as e:
                                pass
                                #print "TRACKING ERROR: %r" % e

        def sourceGroupComplete(self, event):
                print "################### sourceGroupComplete %r" % event
                print event.contents()
                event.reject()
                args         = event.contents().split(";;")
                group        = args[0]
                fileSource   = groupMemberOfType(group, "RVFileSource")
                imageSource  = groupMemberOfType(group, "RVImageSource")
                source       = fileSource if imageSource == None else imageSource
                typeName     = rv.commands.nodeType(source)
                fileNames    = rv.commands.getStringProperty("%s.media.movie" % source, 0, 1000)
                fileName     = fileNames[0]
                ext          = fileName.split('.')[-1].upper()
                mInfo        = rv.commands.sourceMediaInfo(source, None)
                # print "group: %s fileSource: %s fileName: %s" % (group, fileSource, fileName)
                propName = "%s.%s" % (fileSource, "tracking.info")
                
                self.propName = propName
                self.group = group
                try:
                        tl = rv.commands.getStringProperty(propName)
                        self._tracking_info= {}
                        
                        for i in range(0,len(tl)-1, 2):
                                self._tracking_info[tl[i]] = tl[i+1]
                        
                        # make an entity
                        entity = {}
                        entity["type"] = "Version"
                        entity["id"] = int(self._tracking_info['id'])
                        
                        s = self._tracking_info['shot']
                        (s_id, s_name, s_type) = s.split('|')
                        (n, shot_id) = s_id.split('_')

                        self.load_data(entity)
                        
                        # shot_filters = [ ['id','is', int(shot_id)] ]
                        # self.shot_info_model.load_data(entity_type="Shot", filters=shot_filters)

                        #self.version_activity_stream.ui.shot_info_widget.load_data_rv(self._tracking_info)
                        version_filters = [ ['project','is', {'type':'Project','id':71}],
                            ['entity','is',{'type':'Shot','id': int(shot_id)}] ]
                        self.version_model.load_data(entity_type="Version", filters=version_filters)

                except Exception as e:
                        pass
                        # print "OH NO %r" % e

        def __init__(self):
                rv.rvtypes.MinorMode.__init__(self)
                self.note_dock = None
                self.tray_dock = None
                self.tab_widget = None
                self.mini_cut = False

                self._tracking_info= {}

                self.init("RvActivityMode", None,
                        [ 
                                ("after-session-read", self.afterSessionRead, ""),
                                ("before-session-read", self.beforeSessionRead, ""),
                                # ("source-group-complete", self.sourceSetup, ""),
                                ("after-graph-view-change", self.viewChange, ""),
                                ("frame-changed", self.frameChanged, ""),
                                # ("graph-node-inputs-changed", self.inputsChanged, ""),
                                ("incoming-source-path", self.sourcePath, ""),
                                ("source-group-complete", self.sourceGroupComplete, ""),
                                ("graph-state-change", self.graphStateChange, "")
                        ],
                        None,
                        None);

                rv.extra_commands.toggleFullScreen()
                

        def load_data(self, entity):
                # our session property is called tracking
                #tracking_str = rv.commands.getStringProperty('sourceGroup000001_source.tracking.info ')
                #print tracking_str
                # print "ACTIVITY NODE @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
                self.version_activity_stream.load_data(entity)
                shot_filters = [ ['id','is', entity['id']] ]
                self.shot_info_model.load_data(entity_type="Version", filters=shot_filters)
 
        # parent is note_dock here...
        def init_ui(self, note_dock, tray_dock):
                self.note_dock = note_dock
                self.tray_dock = tray_dock
 
                # setup Tab widget with notes and versions, then setup tray 
                self.tab_widget = QtGui.QTabWidget()

                self.tab_widget.setFocusPolicy(QtCore.Qt.NoFocus)
                self.tab_widget.setObjectName("tab_widget")
                
                activity_stream = tank.platform.import_framework("tk-framework-qtwidgets", "activity_stream")

                self.activity_tab_frame = QtGui.QWidget(self.note_dock)
                
                self.notes_container_frame = QtGui.QFrame(self.activity_tab_frame)
                self.cf_verticalLayout = QtGui.QVBoxLayout()
                self.cf_verticalLayout.setObjectName("cf_verticalLayout")
                self.notes_container_frame.setLayout(self.cf_verticalLayout)

                self.shot_info = QtGui.QListView()
                self.cf_verticalLayout.addWidget(self.shot_info)
                # self.version_activity_stream.ui.verticalLayout.addWidget(self.shot_info)
                
                self.shot_info_model = shotgun_model.SimpleShotgunModel(self.activity_tab_frame)
                self.shot_info.setModel(self.shot_info_model)

                self.shot_info_delegate = RvShotInfoDelegate(self.shot_info)
                self.shot_info.setItemDelegate(self.shot_info_delegate)

                self.shot_info.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
                self.shot_info.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
                self.shot_info.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
                self.shot_info.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
                self.shot_info.setUniformItemSizes(True)
                self.shot_info.setObjectName("shot_info")

                from .shot_info_widget import ShotInfoWidget
                self.shot_info.setMinimumSize(ShotInfoWidget.calculate_size())
                si_size = ShotInfoWidget.calculate_size()
                self.shot_info.setMaximumSize(QtCore.QSize(si_size.width() + 10, si_size.height() + 10))
                
                shot_filters = [ ['id','is', 1161] ]
                self.shot_info_model.load_data(entity_type="Shot", filters=shot_filters, fields=["code", "link"])



                self.version_activity_stream = activity_stream.ActivityStreamWidget(self.notes_container_frame)
                self.cf_verticalLayout.addWidget(self.version_activity_stream)

                self.tab_widget.setStyleSheet("QWidget { font-family: Proxima Nova; font-size: 16px; background: rgb(36,38,41); color: rgb(126,127,129); border-color: rgb(36,38,41);}\
                    QTabWidget::tab-bar { alignment: center; border: 2px solid rgb(236,38,41); } \
                    QTabBar::tab { border: 2px solid rgb(36,38,41); alignment: center; background: rgb(36,38,41); margin: 4px; color: rgb(126,127,129); }\
                    QTabBar::tab:selected { color: rgb(40,136,175)} \
                    QTabWidget::pane { border-top: 2px solid rgb(66,67,69); }")


                task_manager = tank.platform.import_framework("tk-framework-shotgunutils", "task_manager")
                self._task_manager = task_manager.BackgroundTaskManager(parent=self.version_activity_stream,
                                                                        start_processing=True,
                                                                        max_threads=2)
                
                shotgun_globals = tank.platform.import_framework("tk-framework-shotgunutils", "shotgun_globals")
                shotgun_globals.register_bg_task_manager(self._task_manager)
                
                self.version_activity_stream.set_bg_task_manager(self._task_manager)
                

                self.entity_version_tab = QtGui.QWidget()
                self.entity_version_tab.setObjectName("entity_version_tab")
                
                self.verticalLayout_3 = QtGui.QVBoxLayout(self.entity_version_tab)
                self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
                self.verticalLayout_3.setObjectName("verticalLayout_3")
                
                self.entity_version_view = QtGui.QListView(self.entity_version_tab)
                self.entity_version_view.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
                self.entity_version_view.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
                self.entity_version_view.setUniformItemSizes(True)
                self.entity_version_view.setObjectName("entity_version_view")

                self.version_delegate  = RvVersionListDelegate(self.entity_version_view)
                self.version_model = shotgun_model.SimpleShotgunModel(self.entity_version_tab)

                # Tell the view to pull data from the model
                self.entity_version_view.setModel(self.version_model)
                self.entity_version_view.setItemDelegate(self.version_delegate)

                # load all assets from Shotgun 
                # REMOVE THIS LATER 
                # version_filters = [ 
                #                     ['project','is', {'type':'Project','id':65}],
                #                     ['entity','is',{'type':'Shot','id': 861}] 
                #                 ]
                # self.version_model.load_data(entity_type="Version", filters=version_filters)
                
                self.verticalLayout_3.addWidget(self.entity_version_view)

                self.version_activity_tab = QtGui.QWidget()
                self.version_activity_tab.setObjectName("version_activity_tab")
                
                self.version_activity_stream.setObjectName("version_activity_stream")
                
                self.tools_tab = QtGui.QWidget()
                self.tools_tab.setObjectName("tools_tab")

                self.tab_widget.addTab(self.notes_container_frame, "NOTES")                
                self.tab_widget.addTab(self.entity_version_tab, "VERSIONS")
                self.tab_widget.addTab(self.tools_tab, "TOOLS")

                self.note_dock.setWidget(self.tab_widget)

                # setup lower tray
                self.tray_dock.setMinimumSize(QtCore.QSize(1200,160))
                
                self.tray_frame = QtGui.QFrame(self.tray_dock)
                self.tray_frame.setMinimumSize(QtCore.QSize(1200,130))
                self.tray_frame_vlayout = QtGui.QVBoxLayout(self.tray_frame)


                sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
                sizePolicy.setHorizontalPolicy(QtGui.QSizePolicy.Expanding)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                self.tray_frame.setSizePolicy(sizePolicy)

                # tray button bar
                self.tray_button_bar = QtGui.QFrame(self.tray_dock)
                self.tray_button_bar.setMinimumSize(QtCore.QSize(1000,25))
                # self.tray_button_bar.setStyleSheet('QFrame { border: 1px solid #ff0000; padding: 1px; } QPushButton { margin: 0px; }')
                sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
                sizePolicy.setHorizontalPolicy(QtGui.QSizePolicy.Expanding)
                sizePolicy.setHorizontalStretch(1)
                sizePolicy.setVerticalStretch(0)
                self.tray_button_bar.setSizePolicy(sizePolicy)

                self.tray_button_bar_hlayout = QtGui.QHBoxLayout(self.tray_button_bar)
                self.tray_button_bar_hlayout.setContentsMargins(0, 0, 0, 0)
                
                self.tray_button_one = QtGui.QPushButton()
                self.tray_button_one.setStyleSheet('QPushButton { border: 1px solid #00ff00; margin: 0px;}')
                self.tray_button_bar_hlayout.addWidget(self.tray_button_one)

                self.tray_button_two = QtGui.QPushButton()
                self.tray_button_two.setStyleSheet('QPushButton { border: 1px solid #00fff0; }')
                self.tray_button_bar_hlayout.addWidget(self.tray_button_two)

                self.tray_button_bar_hlayout.addStretch(1)

                self.tray_button_entire_cut = QtGui.QPushButton()
                self.tray_button_entire_cut.setText('Entire Cut')
                #self.tray_button_three.setStyleSheet('QPushButton { border: 1px solid #000ff0; }')
                self.tray_button_bar_hlayout.addWidget(self.tray_button_entire_cut)
                self.tray_button_entire_cut.clicked.connect(self.on_entire_cut)

                self.tray_button_mini_cut = QtGui.QPushButton()
                self.tray_button_mini_cut.setText('Mini Cut')
                #self.tray_button_four.setStyleSheet('QPushButton { border: 1px solid #f00ff0; }')
                self.tray_button_bar_hlayout.addWidget(self.tray_button_mini_cut)
                self.tray_button_mini_cut.clicked.connect(self.on_mini_cut)

                self.tray_button_bar_hlayout.addStretch(1)

                self.tray_button_five = QtGui.QPushButton()
                self.tray_button_five.setStyleSheet('QPushButton { border: 1px solid #f0f000; }')
                self.tray_button_bar_hlayout.addWidget(self.tray_button_five)

                self.tray_frame_vlayout.addWidget(self.tray_button_bar)

                self.tray_list = QtGui.QListView()
                self.tray_frame_vlayout.addWidget(self.tray_list)
                
                from .tray_model import TrayModel
                self.tray_model = TrayModel(self.tray_list)
                from .tray_sort_filter import TraySortFilter
                self.tray_proxyModel =  TraySortFilter(self.tray_list)
                self.tray_proxyModel.setSourceModel(self.tray_model)

                self.tray_list.setModel(self.tray_proxyModel)

                self.tray_delegate = RvTrayDelegate(self.tray_list)
                self.tray_list.setItemDelegate(self.tray_delegate)

                self.tray_list.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
                self.tray_list.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
                self.tray_list.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
                self.tray_list.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
                self.tray_list.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
                self.tray_list.setFlow(QtGui.QListView.LeftToRight)
                self.tray_list.setUniformItemSizes(True)
                #self.tray_list.setMinimumSize(QtCore.QSize(1000,80))
                self.tray_list.setObjectName("tray_list")

                tray_filters = [ ['sg_cut','is', {'type':'CustomEntity10', 'id': 8}] ]
                tray_fields= ["sg_cut_in", "sg_cut_out", "sg_cut_order", 
                        "sg_version.Version.sg_path_to_frames", "sg_version.Version.id",
                        "sg_version.Version.sg_first_frame", "sg_version.Version.sg_last_frame"]

                orders = [{'field_name':'sg_cut_order','direction':'asc'}]
                self.tray_model.load_data(entity_type="CustomEntity11", filters=tray_filters, fields=tray_fields, order=orders)
                
                self.tray_model.data_refreshed.connect(self.on_data_refreshed)
                self.tray_model.cache_loaded.connect(self.on_cache_loaded)

                self.tray_list.clicked.connect(self.tray_clicked)
                self.tray_list.activated.connect(self.tray_activated)
                self.tray_list.doubleClicked.connect(self.tray_double_clicked)

                # st = "QListWidget::item { border: 2px solid #00ff00;} \n\
                # QListWidget::item:selected { background-color: red;} \
                # QListView::item:hover { background: #f000f0;}"
                # self.tray_dock.setStyleSheet(st)

        def on_entire_cut(self):
                print "ON ENTIRE CUT"
                self.mini_cut = False
 
                e_ids = self.tray_model.entity_ids
                e_type = self.tray_model.get_entity_type()
                
                rv.commands.setIntProperty('%s.edl.source' % self.cut_seq_name, self.rv_source_nums, True)
                rv.commands.setIntProperty('%s.edl.frame' % self.cut_seq_name, self.rv_frames, True)
                rv.commands.setIntProperty('%s.edl.in' % self.cut_seq_name, self.rv_ins, True)
                rv.commands.setIntProperty('%s.edl.out' % self.cut_seq_name, self.rv_outs, True)
                
                # rv.commands.setIntProperty("%s.mode.autoEDL" % self.cut_seq_name, [0])
                # rv.commands.setIntProperty("%s.mode.useCutInfo" % self.cut_seq_name, [0])

                sources = rv.commands.nodesOfType("RVSourceGroup")
                rv.commands.setNodeInputs(self.cut_seq, sources)
                rv.commands.setViewNode(self.cut_seq)

        def on_mini_cut(self):
                print "ON MINI CUT"
                print "current selection: %r" % self.tray_list.currentIndex()
                self.mini_cut = True
                # get current selection
                cur_index = self.tray_list.currentIndex()
                # get cut info from somewhere... model? sg_data
                # get prev and next from current... selRange
                # get shots on either side
                # tear down graph, build new one

        def on_cache_loaded(self, stuff):
                print "CACHE LOADED %r" % stuff

        def on_data_refreshed(self, was_refreshed):
                print "DATA_REFRESHED: %r" % was_refreshed

                self.tray_proxyModel.sort(0, QtCore.Qt.AscendingOrder)

                ids = self.tray_model.entity_ids
                our_type =  self.tray_model.get_entity_type()

                #print "ITEM: %r" % self.tray_model.index_from_entity(our_type, ids[0])

                #       sourceNode = rve.nodesInGroupOfType (sources[i], "RVFileSource")[0]
                #       (realMedia,frame) = rvc.sequenceOfFile (shot.file)
                #           seq = rvc.newNode ("RVSequenceGroup")
                        # rve.setUIName (seq, self._playlist.name)
                        # rvc.setNodeInputs (seq, newSources)
                        # rvc.setViewNode (seq)

                #                         self._state = "loading media"
                # self._preSources = rvc.nodesOfType("RVSourceGroup")
                # deb ("calling addSources, media = %s" % media)
                # rvc.addSources(media)

                self.rv_source_nums = []
                self.rv_frames = []
                self.rv_ins = []
                self.rv_outs = []
                n = 0
                t = 1
                
                for i in ids:
                        item = self.tray_model.index_from_entity(our_type, i)
                        sg_item = shotgun_model.get_sg_data(item)
                        print "ODR: %r" % sg_item
                        f = sg_item['sg_version.Version.sg_path_to_frames']
                        rv.commands.addSource(f)
                        self.rv_source_nums.append(n)
                        n = n + 1
                        self.rv_ins.append( sg_item['sg_cut_in'] )
                        self.rv_outs.append( sg_item['sg_cut_out'] )
                        self.rv_frames.append(t)
                        t = sg_item['sg_cut_out'] - sg_item['sg_cut_in'] + 1 + t
                
                self.rv_source_nums.append(0)
                self.rv_ins.append(0)
                self.rv_outs.append(0)
                self.rv_frames.append(t)

                self.cut_seq = rv.commands.newNode("RVSequenceGroup")
                
                # need to get the name into the query...
                rv.extra_commands.setUIName(self.cut_seq, "CUTZ cut")
                self.cut_seq_name = rv.extra_commands.nodesInGroupOfType(self.cut_seq, 'RVSequence')[0]

                k = "%s.mode.autoEDL" % str(self.cut_seq_name)
                print "ADDING %s" % k
                if not rv.commands.propertyExists(k):
                        rv.commands.newProperty(k, rv.commands.IntType, 1)
                
                
                rv.commands.setIntProperty('%s.edl.source' % self.cut_seq_name, self.rv_source_nums, True)
                rv.commands.setIntProperty('%s.edl.frame' % self.cut_seq_name, self.rv_frames, True)
                rv.commands.setIntProperty('%s.edl.in' % self.cut_seq_name, self.rv_ins, True)
                rv.commands.setIntProperty('%s.edl.out' % self.cut_seq_name, self.rv_outs, True)
                
                rv.commands.setIntProperty("%s.mode.autoEDL" % self.cut_seq_name, [0])
                rv.commands.setIntProperty("%s.mode.useCutInfo" % self.cut_seq_name, [0])

                sources = rv.commands.nodesOfType("RVSourceGroup")
                rv.commands.setNodeInputs(self.cut_seq, sources)
                rv.commands.setViewNode(self.cut_seq)
                

        def on_item_changed(curr, prev):
                print "item changed"
                print curr, prev

        def tray_double_clicked(self, index):
                print "DOUBLE CLICK %r" % index
                sg_item = shotgun_model.get_sg_data(index)
                print sg_item

        def tray_activated(self, index):
                print "Tray Activated! %r" % index


        def tray_clicked(self, index):
                print "MODE_TRAY_CLICKED %r" % index.row()
                if self.mini_cut:
                        e_ids = self.tray_model.entity_ids
                        e_type = self.tray_model.get_entity_type()

                        mini_sources = []
                        mini_frames = []
                        mini_ins = []
                        mini_outs = []
                        t = 1
                        for x in range(index.row()-2, index.row()+2):
                                m_item = self.tray_model.item_from_entity(e_type, e_ids[x])
                                sg = shotgun_model.get_sg_data(m_item)
                                print "%d %r" % (x, sg['sg_version.Version.sg_path_to_frames'])
                                mini_sources.append(x)
                                mini_ins.append( sg['sg_cut_in'] )
                                mini_outs.append( sg['sg_cut_out'] )
                                mini_frames.append(t)
                                t = sg['sg_cut_out'] - sg['sg_cut_in'] + 1 + t
                        mini_sources.append(0)
                        mini_ins.append(0)
                        mini_outs.append(0)
                        mini_frames.append(t)
                        
                        rv.commands.setIntProperty('%s.edl.source' % self.cut_seq_name, mini_sources, True)
                        rv.commands.setIntProperty('%s.edl.frame' % self.cut_seq_name, mini_frames, True)
                        rv.commands.setIntProperty('%s.edl.in' % self.cut_seq_name, mini_ins, True)
                        rv.commands.setIntProperty('%s.edl.out' % self.cut_seq_name, mini_outs, True)
                        
                        # rv.commands.setIntProperty("%s.mode.autoEDL" % self.cut_seq_name, [0])
                        # rv.commands.setIntProperty("%s.mode.useCutInfo" % self.cut_seq_name, [0])

                        sources = rv.commands.nodesOfType("RVSourceGroup")
                        rv.commands.setNodeInputs(self.cut_seq, sources)
                        rv.commands.setViewNode(self.cut_seq)

                sg_item = shotgun_model.get_sg_data(index)  

                entity = {}
                entity["type"] = "Version"
                entity["id"] = sg_item['sg_version.Version.id']

                # s = self._tracking_info['shot']
                # (s_id, s_name, s_type) = s.split('|')
                # (n, shot_id) = s_id.split('_')

                self.load_data(entity)

                # self.tray_list.selectionModel().clear()
                
                # version_filters = [ ['project','is', {'type':'Project','id':71}],
                #     ['entity','is',{'type':'Shot','id': int(shot_id)}] ]
                # self.version_model.load_data(entity_type="Version", filters=version_filters)

        def activate(self):
                rv.rvtypes.MinorMode.activate(self)

        def deactivate(self):
                rv.rvtypes.MinorMode.deactivate(self)



