# coding: utf-8
# @author: Charles Tim Batista Garrocho
# @contact: charles.garrocho@gmail.com
# @copyright: (C) 2012-2013 Python Software Open Source

"""
Modulo responsável pelas interfaces gráficas utilizadas no software.
"""

from PyQt4 import QtGui, QtCore
from gitHubRequest import obter_notificacoes


class IconeBandejaSistema(QtGui.QSystemTrayIcon):

    def __init__(self, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, parent)

        self.setIcon(QtGui.QIcon('../media/github-tray.png'))
        QtGui.QSystemTrayIcon.show(self)

        QtCore.QTimer.singleShot(100, self.mensagem)

    def click_trap(self, value):
        if value == self.Trigger:
            self.left_menu.exec_(QtGui.QCursor.pos())

    def show_mensagem(self, titulo):
        notificacoes = obter_notificacoes('CharlesGarrocho')
        for i in notificacoes:
            self.showMessage(titulo, i.obter_notificacao())

    def mensagem(self):
    	self.show_mensagem('GitHubNotifi')


if __name__ == "__main__":
    app = QtGui.QApplication([])
    icone = IconeBandejaSistema()
    icone.show()
    app.exec_()
