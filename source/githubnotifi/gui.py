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
from gitHubRequest import obter_notificacoes, verifica_diretorio, verifica_usuario


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
            erros = []
            if verifica_diretorio('{0}/login'.format(settings.path_media)) == True:
                erros.append('Login')
            if verifica_diretorio('{0}/cache'.format(settings.path_media)) == True:
                erros.append('Cache')
            if len(erros) == 1:
                self.notificacao_sistema.emit('Diretorio {0} criado com sucesso!'.format(erros[0]))
            elif len(erros) == 2:
                self.notificacao_sistema.emit('Diretorios {0} e {1} criado com sucesso!'.format(erros[0], erros[1]))
            
            usuario = verifica_usuario()
            if usuario == None:
                self.notificacao_sistema.emit('CONTA')
            else:
                notificacoes = obter_notificacoes(usuario)
                if notificacoes == None:
                    self.notificacao_sistema.emit('Sem Conexao Com a Internet...')
                else:
                    a = True
                    try:
                        erros.index('Cache')
                        a = True
                    except:
                        a = False
                    if a == True:
                        for i in notificacoes:
                            self.notificacao_sistema.emit(i.obter_notificacao())
            time.sleep(settings.PAUSE)


class IconeBandejaSistema(QtGui.QSystemTrayIcon):

    def __init__(self, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, parent)

        self.setIcon(QtGui.QIcon('{0}/img/TRAY.png'.format(settings.path_media)))
        QtGui.QSystemTrayIcon.show(self)

        self.menu = QtGui.QMenu(parent)

        user = verifica_usuario()
        self.acaoUser = None
        if user == None:
            self.show_mensagem('CONTA')
            self.acaoUser = QtGui.QAction(QtGui.QIcon('{0}/img/USUARIO.png'.format(settings.path_media)), '&Sign In', self)
            self.acaoUser.setStatusTip('Logar Conta')
        else:
            self.acaoUser = QtGui.QAction(QtGui.QIcon('{0}/img/SIGN_OUT.png'.format(settings.path_media)), '&Sign Out - {0}'.format(user), self)
            self.acaoUser.setShortcut('S')
        
        self.acaoUser.triggered.connect(self.showDialogoAddAcount)
        self.menu.addAction(self.acaoUser)

        acaoAbout = QtGui.QAction(QtGui.QIcon('{0}/img/AJUDA.png'.format(settings.path_media)), '&Help', self)
        acaoAbout.setShortcut('H')
        acaoAbout.setStatusTip('Sobre o GitHubNotifi')
        acaoAbout.triggered.connect(self.showDialogoSobre)
        self.menu.addAction(acaoAbout)

        acaoExit = QtGui.QAction(QtGui.QIcon('{0}/img/SAIR.png'.format(settings.path_media)), '&Exit', self)
        acaoExit.setShortcut('E')
        acaoExit.setStatusTip('Sair do GitHubNotifi')
        acaoExit.triggered.connect(QtGui.qApp.quit)
        self.menu.addAction(acaoExit)

        self.dialogoSobre = DialogoSobre()
        self.dialogoAddAcount = DialogoAddAcount()
        self.setContextMenu(self.menu)

        # Conectando a varável notificação do sistema do processo a função show mensagem.
        self.AtuaNoti = AtualizarNotificacoes()
        self.AtuaNoti.notificacao_sistema.connect(self.show_mensagem)
        self.AtuaNoti.start()

    def showDialogoSobre(self):
        """
        Chama o dialogo Sobre.
        """
        self.dialogoSobre.exec_()

    def showDialogoAddAcount(self):
        """
        Chama o dialogo Add acount.
        """
        self.dialogoAddAcount.exec_()

    def show_mensagem(self, mensagem):
        if mensagem == 'CONTA':
            self.showMessage('GitHubNotifi', 'Nenhuma Conta Configurada...')
        else:
            self.showMessage('GitHubNotifi', mensagem)


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
        self.foto_label.setPixmap(QtGui.QPixmap('{0}/img/LOGO.png'.format(settings.path_media)))
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
        self.setWindowIcon(QtGui.QIcon('{0}/img/TRAY.png'.format(settings.path_media)))
        self.setFixedSize(440, 215)
        self.screen = QtGui.QDesktopWidget().screenGeometry()
        self.size = self.geometry()
        self.move((self.screen.width() - self.size.width()) / 2, (self.screen.height() - self.size.height()) / 2)

    def closeEvent(self, event):
        event.ignore()
        self.hide()


class DialogoAddAcount(QtGui.QDialog):
    """
    Essa é a Interface gráfica do dialogo de adicionar conta
    onde o usuário pode realizar o login de uma conta.
    """
    
    def __init__(self):
        """
        Realiza a contrucao da janela, chamando os metodos de construcao.
        """
        super(DialogoAddAcount, self).__init__()
        self.iniciar()
        self.adicionar()
        self.configurar()
        
    def iniciar(self):
        """
        Realiza a instancia de varios componentes da janela.
        """
        self.boxRotuloCampo = QtGui.QHBoxLayout()
        self.boxBotoes = QtGui.QHBoxLayout()
        self.boxTotal = QtGui.QVBoxLayout()

        self.setLayout(self.boxTotal)

        self.rotuloUsername = QtGui.QLabel('<H3>Username</H3>')
        self.campoTextoUsername = QtGui.QLineEdit()

        self.botaoGravar = QtGui.QPushButton(QtGui.QIcon('{0}/img/GRAVAR.png'.format(settings.path_media)), 'Gravar')
        self.botaoGravar.setIconSize(QtCore.QSize(30,30));
        self.botaoGravar.clicked.connect(self.close)
        
        self.botaoCancelar = QtGui.QPushButton(QtGui.QIcon('{0}/img/CANCELAR.png'.format(settings.path_media)), 'Cancelar')
        self.botaoCancelar.setIconSize(QtCore.QSize(30,30));
        self.botaoCancelar.clicked.connect(self.close)

    def adicionar(self):
        """
        Adiciona todos os componentes na janela inicial.
        """
        self.boxRotuloCampo.addWidget(self.rotuloUsername)
        self.boxRotuloCampo.addWidget(self.campoTextoUsername)

        self.boxBotoes.addWidget(self.botaoCancelar)
        self.boxBotoes.addWidget(self.botaoGravar)

        self.boxTotal.addLayout(self.boxRotuloCampo)
        self.boxTotal.addLayout(self.boxBotoes)

    def configurar(self):
        """
        Configura todos os componentes da janela.
        """
        self.setModal(True)
        self.setWindowTitle('GitHubNotifi - Login')
        self.setWindowIcon(QtGui.QIcon('{0}/img/TRAY.png'.format(settings.path_media)))
        self.setFixedSize(270, 100)
        self.screen = QtGui.QDesktopWidget().screenGeometry()
        self.size = self.geometry()
        self.move((self.screen.width() - self.size.width()) / 2, (self.screen.height() - self.size.height()) / 2)

    def closeEvent(self, event):
        event.ignore()
        self.hide()


if __name__ == "__main__":
    app = QtGui.QApplication([])
    icone = IconeBandejaSistema()
    icone.show()
    app.exec_()