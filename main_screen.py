import sys
from PyQt6 import QtWidgets, QtCore, QtGui
import db_manager

#criar banco ao abrir a aplicação
db_manager.criar_banco()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1080, 568)

        # Criar o menu lateral retrátil
        self.sidebar = QtWidgets.QDockWidget()
        self.sidebar.setFeatures(QtWidgets.QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.sidebar.setWindowTitle('Menu')
        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, self.sidebar)

        # Criar o conteúdo do menu lateral
        self.sidebar_content = QtWidgets.QListWidget()
        self.sidebar_content.addItems([
            "Cadastro de áreas de atividade",
            "Incluir nova atividade",
            "Atividades em andamento",
            "Atividades concluídas",
            "Todas as atividades",
            "Emitir relatórios",
            "Gráficos de atividades"
        ])
        self.sidebar.setWidget(self.sidebar_content)

        # Obter o tamanho da fonte atual
        font = self.sidebar_content.font()
        font_metrics = QtGui.QFontMetrics(font)

        # Calcular o tamanho mínimo da barra lateral com base no tamanho do texto das opções
        # e adicionar algum espaçamento extra
        min_width = 0
        for i in range(self.sidebar_content.count()):
            min_width = max(min_width, font_metrics.horizontalAdvance(self.sidebar_content.item(i).text()) + 40)

        # Definir o tamanho mínimo da barra lateral
        self.sidebar.setFixedWidth(min_width)

        # Criar as telas da aplicação
        self.cadastro_area_screen = CadastroAreaScreen()
        self.incluir_nova_atividade_screen = IncluirNovaAtividadeScreen()
        self.atividades_em_andamento_screen = AtividadesEmAndamentoScreen()
        self.atividades_concluidas_screen = AtividadesConcluidasScreen()
        self.todas_as_atividades_screen = TodasAsAtividadesScreen()
        self.emitir_relatorios_screen = EmitirRelatoriosScreen()
        self.graficos_de_atividades_screen = GraficosDeAtividadesScreen()

        # Criar a tela principal
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_layout = QtWidgets.QStackedLayout()
        self.central_widget.setLayout(self.central_layout)
        self.label = QtWidgets.QLabel("Tela principal")
        self.central_layout.addWidget(self.label)

        # Ocultar todas as telas, exceto a tela inicial
        self.cadastro_area_screen.hide()
        self.incluir_nova_atividade_screen.hide()
        self.atividades_em_andamento_screen.hide()
        self.atividades_concluidas_screen.hide()
        self.todas_as_atividades_screen.hide()
        self.emitir_relatorios_screen.hide()
        self.graficos_de_atividades_screen.hide()

        # Adicionar as telas como widgets filhos do layout vertical
        self.central_layout.addWidget(self.cadastro_area_screen)
        self.central_layout.addWidget(self.incluir_nova_atividade_screen)
        self.central_layout.addWidget(self.atividades_em_andamento_screen)
        self.central_layout.addWidget(self.atividades_concluidas_screen)
        self.central_layout.addWidget(self.todas_as_atividades_screen)
        self.central_layout.addWidget(self.emitir_relatorios_screen)
        self.central_layout.addWidget(self.graficos_de_atividades_screen)

        # Conectar a ação de clique no menu lateral à mudança de tela
        self.sidebar_content.itemClicked.connect(self.change_screen)

    def change_screen(self, item):
        # Obter o índice da opção selecionada no menu lateral
        index = self.sidebar_content.row(item)

        # Ocultar todas as telas
        self.cadastro_area_screen.hide()
        self.incluir_nova_atividade_screen.hide()
        self.atividades_em_andamento_screen.hide()
        self.atividades_concluidas_screen.hide()
        self.todas_as_atividades_screen.hide()
        self.emitir_relatorios_screen.hide()
        self.graficos_de_atividades_screen.hide()

        # Exibir a tela correspondente à opção selecionada no menu lateral
        if index == 0:
            self.cadastro_area_screen.show()
            self.central_layout.setCurrentWidget(self.cadastro_area_screen)
        elif index == 1:
            self.incluir_nova_atividade_screen.show()
            self.central_layout.setCurrentWidget(self.incluir_nova_atividade_screen)
        elif index == 2:
            self.atividades_em_andamento_screen.show()
            self.central_layout.setCurrentWidget(self.atividades_em_andamento_screen)
        elif index == 3:
            self.atividades_concluidas_screen.show()
            self.central_layout.setCurrentWidget(self.atividades_concluidas_screen)
        elif index == 4:
            self.todas_as_atividades_screen.show()
            self.central_layout.setCurrentWidget(self.todas_as_atividades_screen)
        elif index == 5:
            self.emitir_relatorios_screen.show()
            self.central_layout.setCurrentWidget(self.emitir_relatorios_screen)
        elif index == 6:
            self.graficos_de_atividades_screen.show()
            self.central_layout.setCurrentWidget(self.graficos_de_atividades_screen)

        # Alterar o texto da tela principal para o título da opção selecionada no menu lateral
        self.label.setText(item.text())

        # atualizar telas
        self.atualiza_todas_atividades()

    def atualiza_todas_atividades(self):
        tela = self.todas_as_atividades_screen
        # consultar todas as atividades e adicionar ao modelo
        self.all_activities = db_manager.consultar_atividades()
        self.modelo = QtGui.QStandardItemModel()
        for atividade in self.all_activities:
            coluna_atividade = QtGui.QStandardItem(atividade[1])
            self.modelo.appendRow([
                coluna_atividade
            ])
            tela.screen_all_activities.reset()
        tela.screen_all_activities.setModel(self.modelo)

# CRIAR CLASSES DE JANELAS
class CadastroAreaScreen(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # criar o layout principal
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        self.label = QtWidgets.QLabel("Tela de cadastro de atividades")
        self.layout.addWidget(self.label)

class IncluirNovaAtividadeScreen(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # criar o layout principal
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        #criar formulário de inclusão de nova atividade
        self.form_layout = QtWidgets.QFormLayout()
        self.layout.addLayout(self.form_layout)

        # Criar campos de entrada
        self.user_input = QtWidgets.QLineEdit()
        self.status_input = QtWidgets.QComboBox()
        self.status_input.addItems(["Agendada", "Em andamento", "Concluída"])
        self.date_input = QtWidgets.QDateEdit()
        self.time_input = QtWidgets.QTimeEdit()
        self.value_input = QtWidgets.QLineEdit()
        self.description_input = QtWidgets.QLineEdit()

        # Adicionar campos de entrada ao formulário
        self.form_layout.addRow("Usuário:", self.user_input)
        self.form_layout.addRow("Status:", self.status_input)
        self.form_layout.addRow("Data agendada:", self.date_input)
        self.form_layout.addRow("Hora agendada:", self.time_input)
        self.form_layout.addRow("Valor estimado:", self.value_input)
        self.form_layout.addRow("Descrição:", self.description_input)

        # configura data e hora para atual
        self.date_input.setDate(QtCore.QDate.currentDate())
        self.time_input.setTime(QtCore.QTime.currentTime())

        # Criar botão de cadastro
        self.cadastrar_button = QtWidgets.QPushButton("Cadastrar")
        self.cadastrar_button.clicked.connect(self.cadastrar)
        self.layout.addWidget(self.cadastrar_button)

        # Criar label de mensagem de sucesso/erro
        self.message_label = QtWidgets.QLabel()
        self.layout.addWidget(self.message_label)

    def cadastrar(self):
        # Coletar dados do formulário
        user = self.user_input.text()
        status = self.status_input.currentText()
        date = self.date_input.date().toPyDate()
        time = self.time_input.time().toPyTime()
        value = self.value_input.text()
        description = self.description_input.text()

        # Verificar se todos os campos foram preenchidos
        if not all([user, status, date, time, value, description]):
            self.message_label.setText("Preencha todos os campos!")
            return

        # Tentar converter o valor para float
        try:
            value = float(value.replace(',', '.'))
        except ValueError:
            self.message_label.setText("O valor deve ser um número!")
            return

        # Criar nova atividade com os dados fornecidos
        nova_atividade = Atividade(user, status, date, time, value, description)

        # Tentar adicionar a nova atividade ao banco de dados
        try:
            db_manager.adicionar_nova_atividade(nova_atividade)
        except Exception as e:
            self.message_label.setText(f"Erro ao adicionar atividade: {str(e)}")
            return
        
        # Limpar os campos de entrada
        self.user_input.clear()
        self.status_input.setCurrentIndex(0)
        self.date_input.setDate(QtCore.QDate.currentDate())
        self.time_input.setTime(QtCore.QTime.currentTime())
        self.value_input.clear()
        self.description_input.clear()

        # Mostrar mensagem de sucesso
        self.message_label.setText("Atividade adicionada com sucesso!")

class AtividadesEmAndamentoScreen(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        self.label = QtWidgets.QLabel("Tela de atividades em andamento")
        self.layout.addWidget(self.label)

class AtividadesConcluidasScreen(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        self.label = QtWidgets.QLabel("Tela de atividades concluídas")
        self.layout.addWidget(self.label)

class TodasAsAtividadesScreen(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # criar o layout principal
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        # criar uma label de titulo
        self.label_title = QtWidgets.QLabel("Tela de todas as atividades")
        self.layout.addWidget(self.label_title)

        # cria uma janela de resultados
        self.screen_all_activities = QtWidgets.QListView()
        self.layout.addWidget(self.screen_all_activities)

class EmitirRelatoriosScreen(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        self.label = QtWidgets.QLabel("Tela de emitir relatórios")
        self.layout.addWidget(self.label)

class GraficosDeAtividadesScreen(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        self.label = QtWidgets.QLabel("Tela de gráficos de atividades")
        self.layout.addWidget(self.label)

# criar classe 'Atividade'
class Atividade:
    def __init__(self, user, status, date, time, value, description):
        self.user = user
        self.status = status
        self.date = date
        self.time = time
        self.value = value
        self.description = description

# criar classe 'Area'
class Area:
    def __init__(self, area, description):
        self.area = area
        self.description = description

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
