import sys
import db_manager
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QSessionManager

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.user_name = 'Faça login'


        #carrega a interface
        self.initUI()

    def initUI(self):
        #cria a janela e adiciona os componentes
        self.resize(300,400)
        self.setWindowTitle('Login')

        self.label_login = QLabel('Usuário', self)
        self.label_login.setGeometry(50, 50, 200, 50)
        self.label_login.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.text_input_login = QLineEdit(self)
        self.text_input_login.setGeometry(50, 100, 200, 25)

        self.label_pass = QLabel('Senha', self)
        self.label_pass.setGeometry(50, 150, 200, 50)
        self.label_pass.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.text_input_pass = QLineEdit(self)
        self.text_input_pass.setGeometry(50, 200, 200, 25)

        self.btn_login = QPushButton('Log In', self)
        self.btn_login.setGeometry(75, 300, 150, 50)
        self.btn_login.clicked.connect(self.logar_usuario)

        self.label_logged = QLabel(f'Usuário: {self.user_name}', self)
        self.label_logged.setGeometry(0, 375, 290, 50)
        self.label_logged.setAlignment(Qt.AlignmentFlag.AlignRight)

    #funções
    def logar_usuario(self):
        usuario = self.text_input_login.text()
        senha = self.text_input_pass.text()
        username = db_manager.validar_usuario(usuario, senha)
        if username:
            self.user_name = username[1]
            self.label_logged.setText(f'Usuário: {self.user_name}')
        else:
            self.label_logged.setText(f'Usuário e senha inválidos.')

#Criar a instância da classe LoginWindow
app = QApplication(sys.argv)
login_window = LoginWindow()
#mostra a janela
login_window.show()
app.exec()
