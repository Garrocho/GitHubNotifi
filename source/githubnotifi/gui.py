# coding: utf-8
# @author: Charles Tim Batista Garrocho
# @contact: charles.garrocho@gmail.com
# @copyright: (C) 2012-2013 Python Software Open Source

"""
Modulo responsável pelas interfaces gráficas utilizadas no software.
"""

import time
import settings
from PyQt4 import QtGui, QtCore
from gitHubRequest import obter_notificacoes


class AtualizarNotificacoes(QtCore.QThread):
    """
    Processo responsavel Atualizar as Notificações.
    """
    notificacao_sistema = QtCore.pyqtSignal(str)
    
    def run(self):
        """
        Inicia o processo de obter novas notificações.
        """
        while True:
            notificacoes = obter_notificacoes('CharlesGarrocho')
            for i in notificacoes:
                self.notificacao_sistema.emit(i.obter_notificacao())
            time.sleep(settings.PAUSE)


class Menu(QtGui.QMenu):
    def __init__(self, parent=None):
        QtGui.QMenu.__init__(self, "Edit", parent)

        acaoAbout = QtGui.QAction(QtGui.QIcon.fromTheme('help-about'), '&About', self)
        acaoAbout.setShortcut('Ctrl+A')
        acaoAbout.setStatusTip('Sobre o GitHubNotifi')
        acaoAbout.triggered.connect(self.about)
        self.addAction(acaoAbout)

        acaoSignOut = QtGui.QAction(QtGui.QIcon.fromTheme('system-log-out'), '&Sign Out', self)
        acaoSignOut.setShortcut('Ctrl+S')
        acaoSignOut.setStatusTip('Trocar Conta')
        #acaoSignOut.triggered.connect(QtGui.qApp.quit)
        self.addAction(acaoSignOut)

        acaoExit = QtGui.QAction(QtGui.QIcon.fromTheme('system-shutdown'), '&Exit', self)
        acaoExit.setShortcut('Ctrl+E')
        acaoExit.setStatusTip('Sair do GitHubNotifi')
        acaoExit.triggered.connect(QtGui.qApp.quit)
        self.addAction(acaoExit)

    def about(self):
        w = QtGui.QWidget()
        msg = QtGui.QMessageBox
        msg.information(w, 'About', "Octopy Multi-Clipboard Manager\n Developed by mRt.")


class IconeBandejaSistema(QtGui.QSystemTrayIcon):

    def __init__(self, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, parent)

        self.setIcon(QtGui.QIcon('{0}/img/github-tray.png'.format(settings.path_media)))
        QtGui.QSystemTrayIcon.show(self)

        self.menu = Menu()
        self.setContextMenu(self.menu)

        # Conectando a varável notificação do sistema do processo a função show mensagem.
        self.AtuaNoti = AtualizarNotificacoes()
        self.AtuaNoti.notificacao_sistema.connect(self.show_mensagem)
        self.AtuaNoti.start()

    def show_mensagem(self, mensagem):
        self.showMessage('GitHubNotifi', mensagem)

    def sair_menu(self):
        #self.sair = True
        print dir(self)


if __name__ == "__main__":
    app = QtGui.QApplication([])
    icone = IconeBandejaSistema()
    icone.show()
    app.exec_()