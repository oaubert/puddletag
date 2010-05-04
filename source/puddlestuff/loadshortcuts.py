from puddleobjects import PuddleConfig
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys, pdb, resource,os
from constants import SAVEDIR, DATADIR
import StringIO
from util import open_resourcefile

files = [open_resourcefile(filename)
            for filename in [':/caseconversion.action', ':/standard.action']]

SEPARATOR = 'separator'
ALWAYS = 'always'
menu_path = os.path.join(SAVEDIR, 'menus')
shortcut_path = os.path.join(SAVEDIR, 'shortcuts')

def create_files():
    if not os.path.exists(menu_path):
        text = open_resourcefile(':/menus').read()
        f = open(menu_path, 'w')
        f.write(text)
        f.close()

    if not os.path.exists(shortcut_path):
        text = open_resourcefile(':/shortcuts').read()
        f = open(shortcut_path, 'w')
        f.write(text)
        f.close()

def get_menus(section, filepath=None):
    cparser = PuddleConfig()
    if not filepath:
        filepath = menu_path
    cparser.filename = filepath
    menus = []
    settings = cparser.settings
    temp = settings[section]
    menus = [(z, temp[z]) for z in settings[section + 'attrs']['order']]
    return menus

def menubar(menus, actions):
    texts = [unicode(action.text()) for action in actions]
    menubar = QMenuBar()
    winmenu = None
    for title, actionlist in menus:
        menu = menubar.addMenu(title)
        if title == u'&Windows':
            winmenu = menu
        for action in actionlist:
            if action in texts:
                menu.addAction(actions[texts.index(action)])
            elif action == SEPARATOR:
                menu.addSeparator()
    return menubar, winmenu

def context_menu(section, actions, filepath=None):
    cparser = PuddleConfig(filepath)
    if not filepath:
        filepath = menu_path
        cparser.filename = filepath
    order = cparser.get(section, 'order', [])
    if not order:
        return
    texts = [unicode(action.text()) for action in actions]
    menu = QMenu()
    for action in order:
        if action in texts:
            menu.addAction(actions[texts.index(action)])
        elif action == SEPARATOR:
            menu.addSeparator()
    return menu

def toolbar(groups, actions, controls=None):
    texts = [unicode(action.text()) for action in actions]
    if controls:
        controls = dict([('widget-' + z, v) for z,v in controls.items()])
    toolbar = QToolBar('Toolbar')
    for name, actionlist in groups:
        #toolbar = QToolBar(name)
        #toolbar.setObjectName(name)
        for action in actionlist:
            if action in texts:
                toolbar.addAction(actions[texts.index(action)])
            elif action in controls:
                toolbar.addWidget(controls[action])
        toolbar.addSeparator()
    return toolbar

def create_action(win, name, control, command, icon = None, enabled=ALWAYS,
                    tooltip=None, shortcut=None, checked=None, status=None):
    if icon:
        action = QAction(QIcon(icon), name, win)
    else:
        action = QAction(name, win)
    action.setEnabled(False)

    if shortcut:
        try:
            action.setShortcut(shortcut)
        except TypeError:
            action.setShortcuts(shortcut)

    if tooltip:
        action.setToolTip(tooltip)

    if checked:
        action.setCheckState(True)

    action.enabled = enabled
    action.command = command
    action.control = control
    action.status = status

    return action

def get_actions(parent, filepath=None):
    cparser = PuddleConfig()
    if not filepath:
        filepath = shortcut_path
    cparser.filename = filepath
    setting = cparser.settings
    actions = []
    for section in cparser.sections():
        values = dict([(str(k), v) for k,v in  setting[section].items()])
        actions.append(create_action(parent, **values))
    return actions

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.toolbar = win.addToolBar('toolbar')
    loadShortCuts()
    win.show()
    app.exec_()
