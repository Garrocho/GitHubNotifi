import sys
from PyQt4 import QtGui, QtCore


class AboutWindow(QtGui.QLabel):

    def __init__(self, parent=None):
        QtGui.QLabel.__init__(self, parent=parent)
        self.setText("""
        Huge text goes here
        """)
    # Prevent the widget from closing the whole application, only hides it
    def closeEvent(self, event):
        event.ignore()
        self.hide()


class SystemTrayIcon(QtGui.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtGui.QMenu(parent)
        self.createMenuActions(menu)
        self.setContextMenu(menu)
        # I've tried using the same parent as QSystemTrayIcon, 
        # but the label is not shown.
        # self.aboutWindow = AboutWindow(parent=parent)
        self.aboutWindow = AboutWindow(parent=None)


    def createMenuActions(self, menu):
        exitAction = QtGui.QAction("Exit", menu)
        configureAppAction = QtGui.QAction("Configure Application", menu)
        aboutAction = QtGui.QAction("About", menu)

        self.connect(configureAppAction, QtCore.SIGNAL('triggered()'), self._configureApp)
        self.connect(aboutAction, QtCore.SIGNAL('triggered()'), self._showAbout)
        self.connect(exitAction, QtCore.SIGNAL('triggered()'), self._exitApp)

        self.addActionsToMenu(menu, configureAppAction, aboutAction, exitAction)

    def addActionsToMenu(self, menu, *args):
        for action in args:
            menu.addAction(action)

    def _configureApp(self): pass

    def _showAbout(self):
        self.aboutWindow.show()

    def _exitApp(self):
        sys.exit(0)

def main():
    app = QtGui.QApplication(sys.argv)
    widget = QtGui.QWidget()
    # I'm passing a widget parent to QSystemTrayIcon as pointed out in:
    # http://stackoverflow.com/questions/893984/pyqt-show-menu-in-a-system-tray-application
    trayIcon = SystemTrayIcon(QtGui.QIcon("../media/img/github-tray.png"), widget)
    trayIcon.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()