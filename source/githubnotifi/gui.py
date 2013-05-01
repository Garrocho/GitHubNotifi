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


class DialogoSobre(QtGui.QDialog):
    """
    Essa é a Interface gráfica do dialogo sobre, onde contém as informações de
    software. Nela é definido vários rótulos e uma imagem logo do software.
    """
    
    def __init__(self):
        """
        Realiza a contrucao da janela, chamando os metodos de construcao.
        """
        super(DialogoSobre, self).__init__()
        self.iniciar()
        self.adicionar()
        self.configurar()
        
    def iniciar(self):
        """
        Realiza a instancia de varios componentes da janela.
        """
        self.vbox = QtGui.QHBoxLayout()
        self.setLayout(self.vbox)
        self.foto_label = QtGui.QLabel()
        self.foto_label.setPixmap(QtGui.QPixmap('{0}/img/octocat.png'.format(settings.path_media)))
        self.label = QtGui.QLabel('<H3>Informacoes do software</H3> <b>Software: </b>GitHubNotifi<br> <b>Versao: </b> 1.0 <br> <b>Copyright: </b>Open Source<br> <H3>Desenvolvedor</H3> Charles Tim Batista Garrocho')
    
    def adicionar(self):
        """
        Adiciona todos os componentes na janela inicial.
        """
        self.vbox.addWidget(self.foto_label)
        self.vbox.addWidget(self.label)

    def configurar(self):
        """
        Configura todos os componentes da janela.
        """
        self.setModal(True)
        self.setWindowTitle('GitHubNotifi - Sobre o Software')
        self.setWindowIcon(QtGui.QIcon('{0}/img/github-tray.png'.format(settings.path_media)))
        self.setFixedSize(440, 215)
        self.screen = QtGui.QDesktopWidget().screenGeometry()
        self.size = self.geometry()
        self.move((self.screen.width() - self.size.width()) / 2, (self.screen.height() - self.size.height()) / 2)

    def closeEvent(self, event):
        event.ignore()
        self.hide()


class AtualizarNotificacoes(QtCore.QThread):
    """
    Processo responsavel Atualizar as Notificações.
    """
    notificacao_sistema = QtCore.pyqtSignal(str)
    conta = 'CharlesGarrocho'
    
    def run(self):
        """
        Inicia o processo de obter novas notificações.
        """
        while True:
            notificacoes = obter_notificacoes(self.conta)
            if notificacoes == None:
                self.notificacao_sistema.emit('{0} configurado com sucesso!'.format(self.conta))
            else:
                for i in notificacoes:
                    self.notificacao_sistema.emit(i.obter_notificacao())
            time.sleep(settings.PAUSE)


class IconeBandejaSistema(QtGui.QSystemTrayIcon):

    def __init__(self, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, parent)

        self.setIcon(QtGui.QIcon('{0}/img/github-tray.png'.format(settings.path_media)))
        QtGui.QSystemTrayIcon.show(self)

        self.menu = QtGui.QMenu(parent)

        #########################
        acaoAbout = QtGui.QAction(QtGui.QIcon.fromTheme('help-about'), '&About', self)
        acaoAbout.setShortcut('A')
        acaoAbout.setStatusTip('Sobre o GitHubNotifi')
        acaoAbout.triggered.connect(self.dialogoShow)
        self.menu.addAction(acaoAbout)

        acaoSignOut = QtGui.QAction(QtGui.QIcon.fromTheme('system-log-out'), '&Sign Out', self)
        acaoSignOut.setShortcut('S')
        acaoSignOut.setStatusTip('Trocar Conta')
        #acaoSignOut.triggered.connect(QtGui.qApp.quit)
        self.menu.addAction(acaoSignOut)

        acaoExit = QtGui.QAction(QtGui.QIcon.fromTheme('system-shutdown'), '&Exit', self)
        acaoExit.setShortcut('E')
        acaoExit.setStatusTip('Sair do GitHubNotifi')
        acaoExit.triggered.connect(QtGui.qApp.quit)
        self.menu.addAction(acaoExit)
        ###############################

        self.exSobre = DialogoSobre()
        self.setContextMenu(self.menu)

        # Conectando a varável notificação do sistema do processo a função show mensagem.
        self.AtuaNoti = AtualizarNotificacoes()
        self.AtuaNoti.notificacao_sistema.connect(self.show_mensagem)
        self.AtuaNoti.start()

    def showff(self):
        self.aboutdialog = QtGui.QWidget()
        reply = QtGui.QMessageBox.information(self.aboutdialog, self.tr("About Tunarium"), self.tr("Your text here."), QtGui.QMessageBox.Close)
        if reply == QtGui.QMessageBox.Close:
            print 'sim'
            self.aboutdialog.hide()

    def dialogoShow(self):
        """
        Chama o dialogo Sobre.
        """
        self.exSobre.exec_()

    def show_mensagem(self, mensagem):
        self.showMessage('GitHubNotifi', mensagem)


if __name__ == "__main__":
    app = QtGui.QApplication([])
    icone = IconeBandejaSistema()
    icone.show()
    app.exec_()