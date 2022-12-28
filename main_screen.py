import sys
from PyQt6 import QtWidgets, QtCore, QtGui
import db_manager
from PyQt6.QtWidgets import QAbstractItemView
from datetime import datetime, timedelta

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
        # nomear e preencher colunas
        self.modelo.setHorizontalHeaderLabels(["Título da atividade", "Status atual", "Data agendada", "Hora agendada", "Valor", 
        "Iniciada em", "Terminada em"])
        for atividade in self.all_activities:
            coluna_titulo = QtGui.QStandardItem(atividade[1])
            #coluna_usuario = QtGui.QStandardItem(atividade[2])
            coluna_status = QtGui.QStandardItem(atividade[3])
            coluna_data_agendada = QtGui.QStandardItem(atividade[4])
            coluna_hora_agendada = QtGui.QStandardItem(atividade[5])
            coluna_valor = QtGui.QStandardItem(f"R$ {atividade[6]:,.2f}")
            coluna_data_hora_iniciada = QtGui.QStandardItem(atividade[7])
            coluna_data_hora_terminada = QtGui.QStandardItem(atividade[8])
            #coluna_tempo_total = QtGui.QStandardItem(atividade[9])
            #coluna_descricao = QtGui.QStandardItem(atividade[10])
            self.modelo.appendRow([
                coluna_titulo, 
                #coluna_usuario, 
                coluna_status, 
                coluna_data_agendada, 
                coluna_hora_agendada, 
                coluna_valor,
                coluna_data_hora_iniciada, 
                coluna_data_hora_terminada 
                #coluna_tempo_total, 
                #coluna_descricao
            ])
            tela.screen_all_activities.reset()
        tela.screen_all_activities.setModel(self.modelo)
        # ocultar o índice lateral esquerdo
        tela.screen_all_activities.verticalHeader()#.hide()

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
        self.titulo_input = QtWidgets.QLineEdit()
        self.usuario_input = QtWidgets.QLineEdit()
        self.status_input = QtWidgets.QComboBox()
        self.status_input.addItems(["Agendada", "Iniciada"])
        self.data_agendada_input = QtWidgets.QDateEdit()
        self.hora_agendada_input = QtWidgets.QTimeEdit()
        self.valor_input = QtWidgets.QLineEdit()
        self.descricao_input = QtWidgets.QLineEdit()

        # Adicionar campos de entrada ao formulário
        self.form_layout.addRow("Título da atividade:", self.titulo_input)
        self.form_layout.addRow("Usuário:", self.usuario_input)
        self.form_layout.addRow("Status:", self.status_input)
        self.form_layout.addRow("Data agendada:", self.data_agendada_input)
        self.form_layout.addRow("Hora agendada:", self.hora_agendada_input)
        self.form_layout.addRow("Valor estimado:", self.valor_input)
        self.form_layout.addRow("Descrição:", self.descricao_input)

        # configura data e hora para atual
        self.data_agendada_input.setDate(QtCore.QDate.currentDate())
        self.hora_agendada_input.setTime(QtCore.QTime.currentTime())

        # Criar botão de cadastro
        self.cadastrar_button = QtWidgets.QPushButton("Cadastrar")
        self.cadastrar_button.clicked.connect(self.cadastrar)
        self.layout.addWidget(self.cadastrar_button)

        # Criar label de mensagem de sucesso/erro
        self.message_label = QtWidgets.QLabel()
        self.layout.addWidget(self.message_label)

    def cadastrar(self):
        # Coletar dados do formulário
        titulo = self.titulo_input.text()
        usuario = self.usuario_input.text()
        status = self.status_input.currentText()
        data_agendada = self.data_agendada_input.date().toPyDate()
        hora_agendada = self.hora_agendada_input.time().toPyTime()
        valor = self.valor_input.text()
        descricao = self.descricao_input.text()

        # Verificar se todos os campos foram preenchidos
        if not all([titulo, usuario, status, data_agendada, hora_agendada, valor, descricao]):
            self.message_label.setText("Preencha todos os campos!")
            return

        # Tentar converter o valor para float
        try:
            replace_valor = valor.replace(',', '.')
            valor = float(replace_valor)
        except ValueError:
            self.message_label.setText("O valor deve ser um número!")
            return

        # Verifica data e hora caso a atividade iniciar na hora cadastrada
        data_hora_base = datetime.strptime('01/01/0001 00:00:00', "%d/%m/%Y %H:%M:%S")
        if status == 'Iniciada':
            data_hora_iniciada = datetime.now()
        else:
            data_hora_iniciada = data_hora_base
        
        #definir data e hora terminada zero, definir tempo total zero
        data_hora_terminada = data_hora_base
        tempo_total = data_hora_base

        # Criar nova atividade com os dados fornecidos
        nova_atividade = Atividade(titulo, usuario, status, data_agendada, hora_agendada, valor, 
        data_hora_iniciada, data_hora_terminada, tempo_total, descricao)

        # Tentar adicionar a nova atividade ao banco de dados
        try:
            db_manager.adicionar_nova_atividade(nova_atividade)
        except Exception as e:
            self.message_label.setText(f"Erro ao adicionar atividade: {str(e)}")
            return
        
        # Limpar os campos de entrada
        self.titulo_input.clear()
        self.usuario_input.clear()
        self.status_input.setCurrentIndex(0)
        self.data_agendada_input.setDate(QtCore.QDate.currentDate())
        self.hora_agendada_input.setTime(QtCore.QTime.currentTime())
        self.valor_input.clear()
        self.descricao_input.clear()

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
        self.screen_all_activities = QtWidgets.QTableView()
        # aplicar estilo a tabela
        self.screen_all_activities.setStyleSheet(
            "border: 1px solid black;"
        )
        # altera o modo de seleção para clicar/selecionar linha
        self.screen_all_activities.setSelectionMode(QtWidgets.QTableView.SelectionMode(1))
        self.screen_all_activities.setSelectionBehavior(QtWidgets.QTableView.SelectionBehavior(1))

        # seleciona o header e configura para extender a ultima coluna
        self.header = self.screen_all_activities.horizontalHeader()
        #self.header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode(3)) #opção ResizeToContents
        self.header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode(1)) #opção Stretch
        #self.header.setStretchLastSection(True) #opção extender ultima coluna
        self.layout.addWidget(self.screen_all_activities)

        #criar botoes
        self.new_button = QtWidgets.QPushButton('Nova atividade')
        self.edit_button = QtWidgets.QPushButton('Editar atividade')
        self.delete_button = QtWidgets.QPushButton('Apagar atividade')
        
        #conectar funções
        #self.new_button.clicked.connect(self.nova_atividade)
        self.edit_button.clicked.connect(self.editar_atividade)
        #self.delete_button.clicked.connect(self.apagar_atividade)

        #adiciona botoes
        self.layout.addWidget(self.new_button)
        self.layout.addWidget(self.edit_button)
        self.layout.addWidget(self.delete_button)
        

    def editar_atividade(self):
        
        if len(self.screen_all_activities.selectionModel().selectedRows()) > 0:
            # Obter a linha selecionada na tabela
            selected_row = self.screen_all_activities.selectionModel().selectedRows()[0]
            # Obter o índice da linha selecionada
            row_index = selected_row.row()

            # Obter o modelo da tabela
            model = self.screen_all_activities.model()

            # Obter os dados da linha selecionada no banco de dados
            atividade_loc_titulo = model.data(model.index(row_index, 0))
            atividade_loc_status = model.data(model.index(row_index, 1))
            atividade = db_manager.consultar_atividades_titulo_usuario(atividade_loc_titulo, atividade_loc_status)
            atividade_id = atividade[0]
            atividade_titulo = atividade[1]
            atividade_usuario = atividade[2]
            atividade_status = atividade[3]
            atividade_data_agendada = atividade[4]
            atividade_hora_agendada = atividade[5]
            atividade_valor = atividade[6]
            atividade_data_hora_iniciada = atividade[7]
            atividade_data_hora_terminada = atividade[8]
            atividade_tempo_total = atividade[9]
            atividade_descricao = atividade[10]

            # Mostrar uma caixa de diálogo para editar os dados da tarefa
            atividade_titulo, ok = QtWidgets.QInputDialog.getText(self, "Editar atividade", "Título da atividade:", text=atividade_titulo)
            atividade_status, ok = QtWidgets.QInputDialog.getItem(self, "Editar atividade", "Status da atividade:", ["Agendada", "Iniciada", "Interrompida", "Concluída"], current=0, editable=False)
            if atividade_status != "Agendada":
                data_hora_atual = datetime.now()
                
                if atividade_status == "Iniciada":
                    if atividade_data_hora_iniciada == '01/01/0001 00:00:00':
                        atividade_data_hora_iniciada = datetime.now()
                    else:
                        self.mensagem('Atenção', 'Atividade já iniciada')
                elif atividade_status == "interrompida":
                    if atividade_data_hora_iniciada != '01/01/0001 00:00:00':
                        diferenca = atividade_data_hora_iniciada - data_hora_atual
                        time_objeto = datetime.strptime(diferenca, "%d/%m/%Y %H:%M:%S")
                        tempo_total_atual = datetime.strptime(atividade_tempo_total, "%d/%m/%Y %H:%M:%S")
                        resultado = tempo_total_atual + time_objeto
                        atividade_tempo_total = resultado
                        atividade_data_hora_iniciada = resultado    
                    else:
                        self.mensagem('Atenção', 'Somente selecione "Interrompida" caso a atividade ja esteja iniciada.')
                elif atividade_status == "Concluída":
                    if atividade_data_hora_iniciada != '01/01/0001 00:00:00':
                        atividade_data_hora_terminada = datetime.now()
                        resultado_termino = atividade_data_hora_terminada - atividade_data_hora_iniciada
                        atividade_tempo_total += resultado_termino
                    else:
                        self.mensagem('Atenção', 'Atividade não foi iniciada')
 
            atividade_data_agendada, ok = QtWidgets.QInputDialog.getText(self, "Editar atividade", "Data agendada da atividade:", text=atividade_data_agendada)
            atividade_hora_agendada, ok = QtWidgets.QInputDialog.getText(self, "Editar atividade", "Hora agendada da atividade:", text=atividade_hora_agendada)
            atividade_valor, ok = QtWidgets.QInputDialog.getText(self, "Editar atividade", "Valor da atividade:", text=str(atividade_valor))
            try:
                atividade_valor = float(atividade_valor)
            except:
                self.mensagem('Atenção', 'o valor deve ser no formato do exemplo: 12.30')
                return
            atividade_descricao, ok = QtWidgets.QInputDialog.getText(self, "Editar atividade", "Descrição da atividade:", text=atividade_descricao)

            # Atualizar os dados da tarefa no banco de dados
            atividade_editada = Atividade(atividade_titulo, atividade_usuario, atividade_status, atividade_data_agendada, atividade_hora_agendada, atividade_valor, 
            atividade_data_hora_iniciada, atividade_data_hora_terminada, atividade_tempo_total, atividade_descricao)
            #try:
            db_manager.editar_atividade(atividade_editada)
            #except Exception as e:
                #self.mensagem('Erro ao adicionar atividade', f'erro: {str(e)}')
                #return

            # Atualizar a tabela com os dados atualizados
            MainWindow.atualiza_todas_atividades
        else:
            self.mensagem('Atenção', 'Selecione a atividade na lista e clique em "Editar atividade".')

    def mensagem(self, title, msg):
        message_box = QtWidgets.QMessageBox(parent=self)
        message_box.setWindowTitle(title)
        message_box.setText(msg)
        message_box.setIcon(QtWidgets.QMessageBox.Icon.Information)
        message_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        return message_box.exec()

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
    def __init__(self, titulo, usuario, status, data_agendada, hora_agendada, valor, 
    data_hora_iniciada, data_hora_terminada, tempo_total, descricao):
        self.titulo = titulo
        self.usuario = usuario
        self.status = status
        self.data_agendada = data_agendada
        self.hora_agendada = hora_agendada
        self.valor = valor
        self.data_hora_iniciada = data_hora_iniciada
        self.data_hora_terminada = data_hora_terminada
        self.tempo_total = tempo_total
        self.descricao = descricao

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
