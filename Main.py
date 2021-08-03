import sys
import sqlite3
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QLineEdit, QPushButton, QLabel, QGridLayout, QRadioButton, QComboBox, QTableWidgetItem, QTableWidget
import Function as Funcao
import shelve

class Janela_Principal(QMainWindow): #Janela Principal
	def __init__(self):
		super().__init__()

		Db = Funcao.SQDB()
		Lista = Db.cursor.execute("SELECT * FROM Usuarios")
		if len(Lista.fetchall()) == 0:
			self.CentralWidget = Window_CadasterADM((1, 'PRIMEIRO LOGIN', 111111, 11111, 11111, '0', '0', '0', 'Adm'))
		else:
			self.CentralWidget = LoginWindow()
		self.setCentralWidget(self.CentralWidget)

		
		Db.connection.close()

		setStyle(self)
		self.show()

class LoginWindow(QWidget): #janela de Login
	def __init__(self):
		super().__init__()

		self.Layout = QGridLayout()
		
		#Widgets
		self.Name = QLineEdit(self)
		self.Senha = QLineEdit(self)
		self.Button_Login = QPushButton('Logar', self)
		self.Text = QLabel(self)

		#Configurando widgets
		self.Name.setPlaceholderText('Nome')
		self.Name.returnPressed.connect(lambda :self.Senha.setFocus())
		self.Senha.setPlaceholderText('Senha')
		self.Senha.setEchoMode(QLineEdit.Password)
		self.Senha.returnPressed.connect(self.Logar)
		self.Button_Login.clicked.connect(self.Logar)

		#Inserindo widgets no layout
		self.Layout.addWidget(self.Name)
		self.Layout.addWidget(self.Senha)
		self.Layout.addWidget(self.Button_Login)
		self.Layout.addWidget(self.Text)

		self.setLayout(self.Layout)
	
	def Logar(self): #Verifica se tudo esta ok e loga usuario
		Verify = Funcao.VerifyDatas().VerifyCampos([self.Name.text(), self.Senha.text()]) #verifica se os campos estao preenchidos
		if Verify == True:
			db = Funcao.SQDB().GetUsers(self.Name.text()) #Pega os dados do usuario no banco de dados
			if len(db) != 0:
				if db[2] == self.Name.text() and db[3] == self.Senha.text(): #Verifica se a senha esta certa
					if db[8] == 'Adm':
						Janela.CentralWidget = Window_Adm(db)
						Janela.setCentralWidget(Janela.CentralWidget)
					if db[8] == 'User':
						Janela.CentralWidget = Window_User(db)
						Janela.setCentralWidget(Janela.CentralWidget)

				else: self.Text.setText('Verifique se os campos estão preenchidos corretamente.')

			else: self.Text.setText('Verifique se os campos estão preenchidos corretamente.')

		else: self.Text.setText('Verifique se os campos estão preenchidos corretamente.')
		

class Window_Adm(QWidget):
	def __init__(self, User):
		super().__init__()

		self.Layout = QGridLayout()
		self.User_Data = User

		#Widgets
		self.UserLabel = QLabel(f'Cod: {User[0]} \t\t Nome: {User[1]}', self)
		self.CadasterAdm_Button = QPushButton('Cadastrar ADM', self)
		self.CadasterUser_Button = QPushButton('Cadastrar USUARIO', self)
		self.SearchUSer_Button = QPushButton('Procurar Adm ou Usuario', self)
		self.DellUser_Button = QPushButton("Deletar um User ou Adm", self)
		self.AddObejects_Entrega = QPushButton("Adicionar Objetos para entrega", self)
		self.TabelaObjetos = QPushButton("Tabela de Objetos a serem entregues", self)
		self.TabelaAdm = QPushButton("Tabela de Adm", self)
		self.TabelaUsers = QPushButton("Tabela de Users", self)
		self.DellObjeto_Entrega = QPushButton("Deletar Objeto de Entrega", self)
		self.UserEntregas = QPushButton("Suas Entregas", self)
		self.UserEntregasEmAberto = QPushButton("Suas Entregas em Aberto", self)
		self.UserEntregasJustificadas = QPushButton("Suas Entregas Justificadas", self)

		Deslogar = QPushButton("Deslogar", self)
		
		#Configurando Widgets
		self.CadasterAdm_Button.clicked.connect(self.InitWindow_CadasterAdm)
		self.CadasterUser_Button.clicked.connect(self.InitWindow_CadasterUser)
		self.SearchUSer_Button.clicked.connect(self.InitWindow_SearchUsers)
		self.DellUser_Button.clicked.connect(self.InitWindow_DellUsers)
		Deslogar.clicked.connect(self.Deslogar)
		self.AddObejects_Entrega.clicked.connect(self.InitWindow_AddObjectsEntrega)
		self.TabelaObjetos.clicked.connect(self.InitWindow_TabelaObjetos)
		self.TabelaAdm.clicked.connect(self.InitWindow_TabelaAdm)
		self.TabelaUsers.clicked.connect(self.InitWindow_TabelaUsers)
		self.DellObjeto_Entrega.clicked.connect(self.InitWindow_DellObjetoEntrega)
		self.UserEntregas.clicked.connect(self.InitWindow_UserEntregas)
		self.UserEntregasEmAberto.clicked.connect(self.InitWindow_UserEntregasEmAberto)
		self.UserEntregasJustificadas.clicked.connect(self.InitWindow_UserEntregasJustificadas)

		#Inserindo Widgets no layout
		self.Layout.addWidget(self.UserLabel)
		self.Layout.addWidget(self.CadasterAdm_Button)
		self.Layout.addWidget(self.CadasterUser_Button)
		self.Layout.addWidget(self.SearchUSer_Button)
		self.Layout.addWidget(self.DellUser_Button)
		self.Layout.addWidget(self.AddObejects_Entrega)
		self.Layout.addWidget(self.TabelaObjetos)
		self.Layout.addWidget(self.TabelaAdm)
		self.Layout.addWidget(self.TabelaUsers)
		self.Layout.addWidget(self.DellObjeto_Entrega)
		self.Layout.addWidget(self.UserEntregas)
		self.Layout.addWidget(self.UserEntregasEmAberto)
		self.Layout.addWidget(self.UserEntregasJustificadas)
		self.Layout.addWidget(Deslogar)

		self.setLayout(self.Layout)
	
	def Deslogar(self):
		Janela.setCentralWidget(LoginWindow())

	def InitWindow_CadasterAdm(self):
		try: self.Window.close()
		except: pass
		self.Window = Window_CadasterADM(self.User_Data)
	def InitWindow_CadasterUser(self):
		try: self.Window.close()
		except: pass
		self.Window = Window_CadasterUser(self.User_Data)

	def InitWindow_SearchUsers(self):
		try: self.Window.close()
		except: pass
		self.Window = Window_SearchUsers(self.User_Data)
	
	def InitWindow_DellUsers(self):
		try: self.Window.close()
		except: pass
		self.Window = Window_DellUsers(self.User_Data)

	def InitWindow_AddObjectsEntrega(self):
		try: self.Window.close()
		except: pass
		self.Window = AddObjeto_Entrega(self.User_Data)

	def InitWindow_TabelaObjetos(self):
		try: self.Window.close()
		except: pass
		self.Window = Tabela(self.User_Data)

	def InitWindow_TabelaAdm(self):
		try: self.Window.close()
		except: pass
		self.Window = Tabela(self.User_Data, 'Adm')

	def InitWindow_TabelaUsers(self):
		try: self.Window.close()
		except: pass
		self.Window = Tabela(self.User_Data, 'User')

	def InitWindow_DellObjetoEntrega(self):
		try: self.Window.close()
		except: pass
		self.Window = DellObjeto_Entrega(self.User_Data)
	
	def InitWindow_UserEntregas(self):
		try: self.Window.close()
		except: pass
		self.Window = Tabela(self.User_Data, 'UserEntregas')

	def InitWindow_UserEntregasEmAberto(self):
		try: self.Window.close()
		except: pass
		self.Window = Tabela(self.User_Data, 'UserEntregas', "Em Aberto")

	def InitWindow_UserEntregasJustificadas(self):
		try: self.Window.close()
		except: pass
		self.Window = Tabela(self.User_Data, 'UserEntregas', "Endereço não encontrado")
	

class Window_User(QMainWindow):
	def __init__(self, data):
		super().__init__()
		self.Permisseds = Funcao.SQDB().GetPermissions(data[0])
		self.User = data

		self.Wd = QWidget()
		self.Layout = QGridLayout()

		self.Layout.addWidget(QLabel(f"Cod: {data[0]} \t Nome: {data[1]}", self))
		self.setOptions(self.Layout)
		Deslogar = QPushButton("Deslogar" ,self)
		self.Layout.addWidget(Deslogar)
		Deslogar.clicked.connect(self.Deslogar)

		self.Wd.setLayout(self.Layout)
		setStyle(self)
		self.setCentralWidget(self.Wd)
		self.show()
	
	def Deslogar(self):
		Janela.setCentralWidget(LoginWindow())
	
	def setOptions(self, Layout):
		permissoes = []
		for Valor in self.Permisseds:
			if Valor.isnumeric() == True:
				permissoes.append(int(Valor))
		try:
			if permissoes[0] == 1:
				self.Cadaster_Adm = QPushButton('Cadastrar Adm', self)
				self.Cadaster_Adm.clicked.connect(self.InitWindow_CadasterAdm)
				self.Layout.addWidget(self.Cadaster_Adm)
		except: pass
		try:
			if permissoes[1] == 1:
				self.Cadaster_User = QPushButton('Cadastrar Usuario',self)
				self.Cadaster_User.clicked.connect(self.InitWindow_CadasterUser)
				self.Layout.addWidget(self.Cadaster_User)
		except: pass
		try:
			if permissoes[2] == 1:
				self.SearchUsers = QPushButton('Pesquisar User ou Adm', self)
				self.SearchUsers.clicked.connect(self.InitWindow_SearchUsers)
				self.Layout.addWidget(self.SearchUsers)
		except: pass
		try:
			if permissoes[3] == 1:
				self.DellUsers = QPushButton('Deletar User ou Adm', self)
				self.Layout.addWidget(self.DellUsers)
				self.DellUsers.clicked.connect(self.InitWindow_DellUsers)
		except: pass
		try:
			if permissoes[4] == 1:
				self.AddObjects_Entrega = QPushButton('Adicionar Objetos para entrega', self)
				self.Layout.addWidget(self.AddObjects_Entrega)
				self.AddObjects_Entrega.clicked.connect(self.InitWindow_AddObjectsEntrega)
		except: pass
		try:
			if permissoes[5] == 1:
				self.TabelaEntregas = QPushButton('Tabela de Entregas', self)
				self.Layout.addWidget(self.TabelaEntregas)
				self.TabelaEntregas.clicked.connect(self.InitWindow_TabelaEntregas)
		except: pass
		try:
			if permissoes[6] == 1:
				self.TabelaAdms = QPushButton('Tabela de Adm', self)
				self.Layout.addWidget(self.TabelaAdms)
				self.TabelaAdms.clicked.connect(self.InitWindow_TabelaAdms)
		except: pass
		try:
			if permissoes[7] == 1:
				self.TabelaUsers = QPushButton('Tabela de Users', self)
				self.Layout.addWidget(self.TabelaUsers)
				self.TabelaUsers.clicked.connect(self.InitWindow_TabelaUsers)
		except: pass
		try:
			if permissoes[8] == 1:
				self.DellObjetoEntrega = QPushButton('Deletar Objeto de Entrega', self)
				self.Layout.addWidget(self.DellObjetoEntrega)
				self.DellObjetoEntrega.clicked.connect(self.InitWindow_DellObjetoEntrega)
		except: pass
		self.UserEntregas = QPushButton('Suas Entregas', self)
		self.Layout.addWidget(self.UserEntregas)
		self.UserEntregas.clicked.connect(self.InitWindow_UserEntregas)

		self.UserEntregasEmAberto = QPushButton('Suas Entregas em aberto', self)
		self.Layout.addWidget(self.UserEntregasEmAberto)
		self.UserEntregasEmAberto.clicked.connect(self.InitWindow_UserEntregasEmAberto)

		self.UserEntregasJustificadas = QPushButton('Suas Entregas Justificadas', self)
		self.Layout.addWidget(self.UserEntregasJustificadas)
		self.UserEntregasJustificadas.clicked.connect(self.InitWindow_UserEntregasJustificadas)
	
	def InitWindow_CadasterAdm(self):
		try: self.Window.close()
		except: pass
		self.Window = Window_CadasterADM(self.User)
	def InitWindow_CadasterUser(self):
		try: self.Window.close()
		except: pass
		self.Window = Window_CadasterUser(self.User)

	def InitWindow_SearchUsers(self):
		try: self.Window.close()
		except: pass
		self.Window = Window_SearchUsers(self.User)
	
	def InitWindow_DellUsers(self):
		try: self.Window.close()
		except: pass
		self.Window = Window_DellUsers(self.User)

	def InitWindow_AddObjectsEntrega(self):
		try: self.Window.close()
		except: pass
		self.Window = AddObjeto_Entrega(self.User)

	def InitWindow_TabelaEntregas(self):
		try: self.Window.close()
		except: pass
		self.Window = Tabela(self.User)

	def InitWindow_TabelaAdms(self):
		try: self.Window.close()
		except: pass
		self.Window = Tabela(self.User, "Adm")

	def InitWindow_TabelaUsers(self):
		try: self.Window.close()
		except: pass
		self.Window = Tabela(self.User, "User")

	def InitWindow_DellObjetoEntrega(self):
		try: self.Window.close()
		except: pass
		self.Window = DellObjeto_Entrega(self.User)

	def InitWindow_UserEntregas(self):
		try: self.Window.close()
		except: pass
		self.Window = Tabela(self.User, "UserEntregas")
	
	def InitWindow_UserEntregasEmAberto(self):
		try: self.Window.close()
		except: pass
		self.Window = Tabela(self.User, "UserEntregas", "Em Aberto")
	
	def InitWindow_UserEntregasJustificadas(self):
		try: self.Window.close()
		except: pass
		self.Window = Tabela(self.User, "UserEntregas", 'Endereço não encontrado')

class Window_CadasterADM(QWidget):
	def __init__(self, User):
		super().__init__()
		
		self.User = User
		self.Layout = QGridLayout()

		#Widgets
		self.Nome = QLineEdit(self)
		self.Senha = QLineEdit(self)
		self.Login = QLineEdit(self)
		self.Cpf = QLineEdit(self)
		self.Rg = QLineEdit(self)
		self.Email = QLineEdit(self)
		self.Tel = QLineEdit(self)
		self.ButtonCadaster = QPushButton('Cadastrar', self)
		self.Status = QLabel(self)
		self.ButtonVoltar = QPushButton("Voltar", self)

		#Configurando Widgets
		self.Nome.returnPressed.connect(lambda : self.Login.setFocus())
		self.Login.returnPressed.connect(lambda : self.Senha.setFocus())
		self.Senha.returnPressed.connect(lambda : self.Cpf.setFocus())
		self.Cpf.returnPressed.connect(lambda : self.Rg.setFocus())
		self.Rg.returnPressed.connect(lambda : self.Email.setFocus())
		self.Email.returnPressed.connect(lambda : self.Tel.setFocus())
		self.Tel.returnPressed.connect(self.Cadastrar)
		self.ButtonCadaster.clicked.connect(self.Cadastrar)
		if self.User[0] > 1:
		    self.ButtonVoltar.clicked.connect(self.Voltar)
		else:
		    self.ButtonVoltar.setText("")


		self.Nome.setPlaceholderText("Nome Completo")
		self.Senha.setPlaceholderText('Senha')
		self.Login.setPlaceholderText("Login")
		self.Cpf.setPlaceholderText("CPF Ex: 000.000.000.00")
		self.Rg.setPlaceholderText("RG Ex: 0.000.000")
		self.Email.setPlaceholderText("Email")
		self.Tel.setPlaceholderText("Telefone/Celular")

		#inserindo Widgets no layout
		self.Layout.addWidget(self.Nome, 0, 0, 1,2)
		self.Layout.addWidget(self.Login, 1, 0, 1, 2)
		self.Layout.addWidget(self.Senha,2, 0, 1,2)
		self.Layout.addWidget(self.Cpf, 3, 0, 1, 2)
		self.Layout.addWidget(self.Rg, 4, 0, 1, 2)
		self.Layout.addWidget(self.Email, 5, 0, 1, 2)
		self.Layout.addWidget(self.Tel, 6, 0, 1, 2)
		self.Layout.addWidget(self.ButtonCadaster,7, 0, 1, 2)
		self.Layout.addWidget(self.Status, 8, 0, 1, 2)
		self.Layout.addWidget(self.ButtonVoltar, 9, 0, 1, 2)

		self.setLayout(self.Layout)
		try:
		    Janela.setCentralWidget(self)
		except: pass
		setStyle(self)

	def Voltar(self):
		if self.User[8] == 'Adm':
			Janela.setCentralWidget(Window_Adm(self.User))
		if self.User[8] == "User":
			Janela.setCentralWidget(Window_User(self.User))

	def Cadastrar(self):
		if self.Tel.text().isnumeric() == True:
			data = [self.Nome.text(), self.Login.text(), self.Senha.text(), self.Cpf.text(), self.Rg.text(), self.Email.text(), int(self.Tel.text())]
			Verify = Funcao.VerifyDatas().VerifyCampos(data, Type="Cadaster") #Verifica se os campos estao preenchidos
			if Verify == True:
				Funcao.SQDB().InsertUsers(data, Type="Adm") #Cadasta no Banco de dados
				self.Status.setText(f'Usuario {self.Nome.text()} Cadastrado!')

				self.Nome.setText('')
				self.Senha.setText('')
				self.Login.setText('')
				self.Cpf.setText('')
				self.Rg.setText('')
				self.Email.setText('')
				self.Tel.setText('')
			else:
				self.Status.setText('Não foi possivel fazer o Cadastro. \nCampos em branco ou nome já utilizado.')
		else: self.Status.setText('Telefone/Celular deve conter valores numericos.')

class Window_CadasterUser(QWidget):
	def __init__(self, User):
		super().__init__()
		self.User = User
		self.Layout = QGridLayout()

		#Widgets
		self.Nome = QLineEdit(self)
		self.Senha = QLineEdit(self)
		self.CadasterButton = QPushButton('Cadastrar', self)
		self.Status = QLabel(self)
		self.Login = QLineEdit(self)
		self.Cpf = QLineEdit(self)
		self.Rg = QLineEdit(self)
		self.Email = QLineEdit(self)
		self.Tel = QLineEdit(self)
		self.Permissoes = QPushButton("Permissoes", self)
		self.ButtonVoltar = QPushButton("Voltar", self)


		#Configurando widgets
		self.Nome.returnPressed.connect(lambda : self.Login.setFocus())
		self.Login.returnPressed.connect(lambda : self.Senha.setFocus())
		self.Senha.returnPressed.connect(lambda : self.Cpf.setFocus())
		self.Cpf.returnPressed.connect(lambda : self.Rg.setFocus())
		self.Rg.returnPressed.connect(lambda : self.Email.setFocus())
		self.Email.returnPressed.connect(lambda : self.Tel.setFocus())
		self.Tel.returnPressed.connect(self.Verify)
		self.ButtonVoltar.clicked.connect(self.Voltar)
		self.Permissoes.clicked.connect(self.InitWindow_Permissoes)

		
		self.Nome.setPlaceholderText("Nome Completo")
		self.Senha.setPlaceholderText('Senha')
		self.Login.setPlaceholderText("Login")
		self.Cpf.setPlaceholderText("CPF Ex: 000.000.000.00")
		self.Rg.setPlaceholderText("RG Ex: 0.000.000")
		self.Email.setPlaceholderText("Email")
		self.Tel.setPlaceholderText("Telefone/Celular")
		
		self.CadasterButton.clicked.connect(self.Verify)

		#Inserindo widgets no Layout
		self.Layout.addWidget(self.Nome)
		self.Layout.addWidget(self.Login)
		self.Layout.addWidget(self.Senha)
		self.Layout.addWidget(self.Cpf)
		self.Layout.addWidget(self.Rg)
		self.Layout.addWidget(self.Email)
		self.Layout.addWidget(self.Tel)
		self.Layout.addWidget(self.CadasterButton)
		self.Layout.addWidget(self.Status)
		self.Layout.addWidget(self.Permissoes)
		self.Layout.addWidget(self.ButtonVoltar)
		

		self.setLayout(self.Layout)
		Janela.setCentralWidget(self)
		setStyle(self)
	
	def Voltar(self):
		if self.User[8] == 'Adm':
			Janela.setCentralWidget(Window_Adm(self.User))
		if self.User[8] == "User":
			Janela.setCentralWidget(Window_User(self.User))

	def Verify(self):
		if self.Tel.text().isnumeric() == True:
			data = [self.Nome.text(), self.Login.text(), self.Senha.text(), self.Cpf.text(), self.Rg.text(), self.Email.text(), int(self.Tel.text())]
			Verify = Funcao.VerifyDatas().VerifyCampos(data, Type='Cadaster')
			if Verify == True:

				shelFile = shelve.open('GestionAPP')
				self.Permissions = shelFile['Permissoes']
				Funcao.SQDB().InsertUsers(data, str(self.Permissions), "User")
				shelFile.close()

				self.Status.setText(f'{self.Nome.text()} Cadastrado com sucesso!')

				self.Nome.setText('')
				self.Senha.setText('')
				self.Login.setText('')
				self.Cpf.setText('')
				self.Rg.setText('')
				self.Email.setText('')
				self.Tel.setText('')
			else:
				self.Status.setText('Não foi possivel fazer o Cadastro. \nCampos em branco ou nome já utilizado.')
		else: self.Status.setText('Telefone/Celular deve conter valores numericos.')
	
	def InitWindow_Permissoes(self):
		self.Window = Permissoes(self.User)

class Window_SearchUsers(QWidget):
	def __init__(self, User):
		super().__init__()

		self.Layout = QGridLayout(self)
		self.Tipo_Pesquisa = "Nome"
		self.User = User

		#Widgets
		self.Campo = QLineEdit(self)
		self.SerachButton = QPushButton('Procurar', self)
		self.Adm_Box = QRadioButton('Adm', self)
		self.User_Box = QRadioButton('User', self)
		self.User_Default = QRadioButton('Default', self)
		self.Nome_orCod = QComboBox(self)
		self.Status = QLabel(self)
		self.ButtonVoltar = QPushButton("Voltar", self)
		self.Button_AlterarPermissions = QPushButton("Alterar permissões", self)

		#Configurando Widgets
		self.Campo.returnPressed.connect(self.Search)
		self.SerachButton.clicked.connect(self.Search)
		self.Campo.setPlaceholderText('Insira o Nome')
		self.Adm_Box.setChecked(True)
		self.Nome_orCod.insertItem(0, "Nome")
		self.Nome_orCod.insertItem(1, "Cod")
		self.Nome_orCod.activated[str].connect(self.DefinirTextoComboBox)
		self.ButtonVoltar.clicked.connect(self.Voltar)
		self.Button_AlterarPermissions.setDisabled(True)

		#Inserindo Widgets lo Layout
		self.Layout.addWidget(self.Campo, 0, 0, 1, 3)
		self.Layout.addWidget(self.SerachButton, 1, 0, 1, 4)
		self.Layout.addWidget(self.Adm_Box, 2, 0)
		self.Layout.addWidget(self.User_Box, 2, 1)
		self.Layout.addWidget(self.User_Default, 2, 2)
		self.Layout.addWidget(self.Status, 3, 0, 1, 4)
		self.Layout.addWidget(self.Nome_orCod, 0, 3, 1, 1)
		self.Layout.addWidget(self.Button_AlterarPermissions, 4, 0, 1, 4)
		self.Layout.addWidget(self.ButtonVoltar, 5, 0, 1, 4)

		self.setLayout(self.Layout)
		Janela.setCentralWidget(self)
		setStyle(self)
	
	def Voltar(self):
		if self.User[8] == 'Adm':
			Janela.setCentralWidget(Window_Adm(self.User))
		if self.User[8] == "User":
			Janela.setCentralWidget(Window_User(self.User))

	def DefinirTextoComboBox(self, text):
		self.Tipo_Pesquisa = text
		self.Campo.setPlaceholderText(("Insira o Nome" if text == "Nome" else 'Insira o Cod'))

	def Search(self):
		Verify = Funcao.VerifyDatas().VerifyCampos([self.Campo.text()])
		if Verify == True:
			
			#Procurar adm
			if self.Adm_Box.isChecked() == True:
				try:
					self.db = Funcao.SQDB().GetUsers(self.Campo.text(), "Adm", self.Tipo_Pesquisa)
					self.Status.setText(f'Cod: {self.db[0]} \nNome: {self.db[1]} \nStatus: {self.db[8]}')
				except IndexError:
					self.Status.setText('Adm não encontrado.')

			#Procurar User
			elif self.User_Box.isChecked() == True:
				try:
					self.db = Funcao.SQDB().GetUsers(self.Campo.text(), "User", self.Tipo_Pesquisa)
					self.Status.setText(f'Cod: {self.db[0]} \nNome: {self.db[1]} \nStatus: {self.db[8]}')
					self.GetPermissions(self.db[0])
				except IndexError:
					self.Status.setText("User não encontrado.")

			#Procurar User ou Adm
			elif self.User_Default.isChecked() == True:
				try:
					self.db = Funcao.SQDB().GetUsers(self.Campo.text(), Cod_Name=self.Tipo_Pesquisa)
					self.Status.setText(f'Cod: {self.db[0]} \nNome: {self.db[1]} \nStatus: {self.db[8]}')
					if self.db[3] == 'User':
						self.GetPermissions(self.db[0])
						self.Liberar_Bot
				except IndexError:
					self.Status.setText("Nada encontrado.")
		else:
			self.Status.setText('Por favor! Insira os dados corretamente.')
		try:
			if self.User[8] == 'User' and self.db[8] != "Adm":
				Permissoes_User = Funcao.SQDB().GetPermissions(self.User[0])
				permi = []
				for num in Permissoes_User:
					if num.isnumeric() == True:
						permi.append(int(num))
				if permi[9] == 1:
					self.Button_AlterarPermissions.setEnabled(True)
					self.Button_AlterarPermissions.clicked.connect(self.Window_AlterarPermissoes)
			elif self.db[8] != "Adm":
				self.Button_AlterarPermissions.setEnabled(True)
				self.Button_AlterarPermissions.clicked.connect(self.Window_AlterarPermissoes)
			else:
				self.Button_AlterarPermissions.setEnabled(False)
			
		except: pass
	
	def Window_AlterarPermissoes(self):
		self.Window = Permissoes(self.User)
		self.Window.definir.clicked.connect(self.AlterarPermisooes)

	def AlterarPermisooes(self):
		shelvFile = shelve.open('GestionAPP')

		bd = Funcao.SQDB()
		bd.cursor.execute('UPDATE Permisseds SET Permisseds = ? WHERE Cod = ?', (str(shelvFile['Permissoes']), self.db[0]))
		bd.connection.commit()
		bd.connection.close()

		shelvFile.close()

	def GetPermissions(self, cod):
		Status = self.Status.text()
		Status += '\n \t\t Permissoes \t\t\n'
		Permisseds = Funcao.SQDB().GetPermissions(cod)

		permissoes = []
		for Valor in Permisseds:
			if Valor.isnumeric() == True:
				permissoes.append(int(Valor))
		if permissoes[0] == 1:
			Status += 'Cadastrar Adm\n'
		if permissoes[1] == 1:
			Status += 'Cadastrar Usuario\n'
		if permissoes[2] == 1:
			Status += 'Pesquisar User ou Adm\n'
		if permissoes[3] == 1:
			Status += 'Deletar User ou Adm\n'
		if permissoes[4] == 1:
			Status += 'Adicionar Objeto de entrega\n'
		if permissoes[5] == 1:
			Status += 'Tabela de Entregas\n'
		if permissoes[6] == 1:
			Status += 'Tabela de Adm\n'
		if permissoes[7] == 1:
			Status += 'Tabela de Users\n'
		if permissoes[8] == 1:
			Status += 'Deletar Objeto de Entrega\n'
		if permissoes[9] == 1:
			Status += 'Alterar permissoes\n'
		if permissoes[10] == 1:
			Status += "Alterar Status das Entregas\n"
		self.Status.setText(Status)

class Window_DellUsers(QWidget):
	def __init__(self, UserData):
		super().__init__()
		self.UserData = UserData

		self.Layout = QGridLayout()
		self.Tipo_Pesquisa = 'Nome'

		#Widgets
		self.Input = QLineEdit(self)
		self.Type_Adm = QRadioButton('Adm', self)
		self.Type_Users = QRadioButton('User', self)
		self.Type_Default = QRadioButton('Default', self)
		self.Type_Search = QComboBox(self)
		self.Search_Button = QPushButton("Pesquisar", self)
		self.Status = QLabel(self)
		self.Button_DellUsers = QPushButton('Deletar' ,self)
		self.ButtonVoltar = QPushButton("Voltar", self)

		#Configurando Widgets
		self.Type_Search.insertItem(0, "Nome")
		self.Type_Search.insertItem(1, "Cod")
		self.Type_Search.activated[str].connect(self.DefinirTipoPesquisa)
		self.Input.setPlaceholderText(self.Tipo_Pesquisa)
		self.Type_Adm.setChecked(True)
		self.Search_Button.clicked.connect(self.Verify)
		self.Input.returnPressed.connect(self.Verify)
		self.Button_DellUsers.clicked.connect(self.DellUser)
		self.ButtonVoltar.clicked.connect(self.Voltar)

		#Inserindo Widgets no Layout
		self.Layout.addWidget(self.Input, 0, 0, 1, 2)
		self.Layout.addWidget(self.Type_Adm, 1,0)
		self.Layout.addWidget(self.Type_Users, 1, 1)
		self.Layout.addWidget(self.Type_Default, 1, 2)
		self.Layout.addWidget(self.Type_Search, 0, 2)
		self.Layout.addWidget(self.Search_Button, 2, 0, 1, 2)
		self.Layout.addWidget(self.Button_DellUsers, 2, 2)
		self.Layout.addWidget(self.Status, 3, 0, 1, 3)
		self.Layout.addWidget(self.ButtonVoltar, 4, 0, 1, 3)
		
		setStyle(self)
		self.setLayout(self.Layout)
		Janela.setCentralWidget(self)
	
	def Voltar(self):
		if self.UserData[8] == 'Adm':
			Janela.setCentralWidget(Window_Adm(self.UserData))
		if self.UserData[8] == "User":
			Janela.setCentralWidget(Window_User(self.UserData))
	
	def DefinirTipoPesquisa(self, text):
		self.Tipo_Pesquisa = text
		self.Input.setPlaceholderText(self.Tipo_Pesquisa)
	
	def Verify(self):
		Verify = Funcao.VerifyDatas().VerifyCampos([self.Input.text()])
		if Verify == True:
			
			#Procurar adm
			if self.Type_Adm.isChecked() == True:
				try:
					db = Funcao.SQDB().GetUsers(self.Input.text(), "Adm", self.Tipo_Pesquisa)
					self.Status.setText(f'Cod: {db[0]} \nNome: {db[1]} \nStatus: {db[8]}')
				except IndexError:
					self.Status.setText('Adm não encontrado.')

			#Procurar User
			elif self.Type_Users.isChecked() == True:
				try:
					db = Funcao.SQDB().GetUsers(self.Input.text(), "User", self.Tipo_Pesquisa)
					self.Status.setText(f'Cod: {db[0]} \nNome: {db[1]} \nStatus: {db[8]}')
				except IndexError:
					self.Status.setText("User não encontrado.")

			#Procurar User ou Adm
			elif self.Type_Default.isChecked() == True:
				try:
					db = Funcao.SQDB().GetUsers(self.Input.text(), Cod_Name=self.Tipo_Pesquisa)
					self.Status.setText(f'Cod: {db[0]} \nNome: {db[1]} \nStatus: {db[8]}')
				except IndexError:
					self.Status.setText("Nada encontrado.")
		else:
			self.Status.setText('Por favor! Insira os dados corretamente.')
		
	def DellUser(self):
		if self.Input.text().isnumeric() == True and self.Tipo_Pesquisa == "Cod":
			try:
				db = Funcao.SQDB().GetUsers(self.Input.text(), Cod_Name=self.Tipo_Pesquisa)
				self.Status.setText(f"Usuario de Cod: {self.Input.text()} Nome: {db[1]} deletado dos registros!")
				Funcao.SQDB().DellUsers(int(self.Input.text()))
				
			except IndexError:
				self.Status.setText("Usuario não encontrado.")
		elif self.Tipo_Pesquisa == "Nome":
			try:
				db = Funcao.SQDB().GetUsers(self.Input.text(), Cod_Name="Nome")
				Funcao.SQDB().DellUsers(db[0])
				self.Status.setText(f"Usuario {db[1]} deletado dos registros!")
			except IndexError:
				self.Status.setText("Usuario não encontrado.")
			
class AddObjeto_Entrega(QWidget):
	def __init__(self, UserData):
		super().__init__()
		self.UserData = UserData
		self.Layout = QGridLayout()

		#Widgets
		self.Nome = QLineEdit(self)
		self.Rg = QLineEdit(self)
		self.Cpf = QLineEdit(self)
		self.End = QLineEdit(self)
		self.Cep = QLineEdit(self)
		self.CodClient = QLineEdit(self)
		self.Entregador = QLineEdit(self)
		self.Registrar = QPushButton("Registrar", self)
		self.Status = QLabel(self)
		self.Voltar = QPushButton("Voltar", self)

		#Configurando Widgets
		self.Voltar.clicked.connect(self.VoltarWindow)
		self.Nome.setPlaceholderText("Nome do Cliente")
		self.Nome.returnPressed.connect(lambda : self.Rg.setFocus())
		self.Rg.setPlaceholderText("RG do Cliente")
		self.Rg.returnPressed.connect(lambda : self.Cpf.setFocus())
		self.Cpf.setPlaceholderText("CPF do Cliente")
		self.Cpf.returnPressed.connect(lambda : self.End.setFocus())
		self.End.setPlaceholderText("Endereco do Cliente")
		self.End.returnPressed.connect(lambda : self.Cep.setFocus())
		self.Cep.setPlaceholderText("Cep do Cliente")
		self.Cep.returnPressed.connect(lambda : self.CodClient.setFocus())
		self.CodClient.setPlaceholderText("Codigo do Cliente")
		self.CodClient.returnPressed.connect(lambda : self.Entregador.setFocus())
		self.Entregador.setPlaceholderText("Nome ou Cod do Entregador")
		self.Entregador.returnPressed.connect(self.Cadastrar)
		self.Registrar.clicked.connect(self.Cadastrar)

		#Inserindo Widgets no Layout
		self.Layout.addWidget(self.Nome)
		self.Layout.addWidget(self.Rg)
		self.Layout.addWidget(self.Cpf)
		self.Layout.addWidget(self.End)
		self.Layout.addWidget(self.Cep)
		self.Layout.addWidget(self.CodClient)
		self.Layout.addWidget(self.Entregador)
		self.Layout.addWidget(self.Registrar)
		self.Layout.addWidget(self.Status)
		self.Layout.addWidget(self.Voltar)


		self.setLayout(self.Layout)
		Janela.setCentralWidget(self)
		setStyle(self)

	def VoltarWindow(self):
		if self.UserData[8] == 'Adm':
			Janela.setCentralWidget(Window_Adm(self.UserData))
		if self.UserData[8] == "User":
			Janela.setCentralWidget(Window_User(self.UserData))
	
	def Cadastrar(self):
		data = [self.Nome.text(), self.Rg.text(), self.Cpf.text(), self.End.text(), self.Cep.text(), self.CodClient.text(), self.Entregador.text()]
		Verify = Funcao.VerifyDatas().VerifyCampos(data, 'Login')
		if Verify == True:
			try:
				Verify = Funcao.SQDB().GetUsers(int(self.Entregador.text()), Cod_Name='Cod')
				self.Status.setText(f'Entrega em {self.End.text()} devera ser feita por {Verify[1]}')
				Funcao.SQDB().InsertObject_Entrega(data)
				self.Nome.setText(), self.Rg.setText(), self.Cpf.setText(), self.End.setText(), self.Cep.setText(), self.CodClient.setText(), self.Entregador.setText()
			except:
				try:
					Verify = Funcao.SQDB().GetUsers(self.Entregador.text(), Cod_Name='Nome')
					self.Status.setText(f'Entrega em {self.End.text()} devera ser feita por {Verify[1]}')
					Funcao.SQDB().InsertObject_Entrega(data)
					self.Nome.text(), self.Rg.text(), self.Cpf.text(), self.End.text(), self.Cep.text(), self.CodClient.text(), self.Entregador.text()
				except:
					self.Status.setText('Entregador não encontrado')
		else:
			self.Status.setText('Preencha todos os campos')

class Tabela(QWidget):
	def __init__(self, User, Type = "Entregas", Situacao = 'Entregue'):
		super().__init__()
		self.UserData = User
		self.Type = Type
		self.Linha = 0
		self.Situacao = Situacao

		self.Layout = QGridLayout()
		self.Tabela = QTableWidget()

		#Widgets
		self.Voltar = QPushButton('Voltar',self)
		self.Line = QLineEdit(self)
		self.Pesquisar = QPushButton("Pesquisar", self)

		#Configurando Widgets
		self.Voltar.clicked.connect(self.VoltarWindow)
		self.Line.setPlaceholderText("Nome ou Cod")
		self.Line.returnPressed.connect(self.Reset)
		self.Pesquisar.clicked.connect(self.Reset)

		self.TipoTabela()

		#Adicionando Widgets no Layout
		self.Layout.addWidget(self.Line)
		self.Layout.addWidget(self.Pesquisar)
		self.Layout.addWidget(self.Tabela)
		self.Layout.addWidget(self.Voltar)

		self.setLayout(self.Layout)
		Janela.setCentralWidget(self)

	def Reset(self):
		while self.Linha != 0:
			self.Tabela.removeRow(self.Linha)
			self.Linha -= 1

		self.Tabela.removeRow(self.Linha)
		self.TipoTabela()

	def TipoTabela(self):
		if self.Type == "Entregas":
			self.Entregas()
		elif self.Type == "Adm":
			self.Adm()
		elif self.Type == "User":
			self.Users()
		elif self.Type == "UserEntregas":
			self.UserEntregas()

	def VoltarWindow(self):
		if self.UserData[8] == 'Adm':
			Janela.setCentralWidget(Window_Adm(self.UserData))
		if self.UserData[8] == "User":
			Janela.setCentralWidget(Window_User(self.UserData))

	def Entregas(self): #Adiciona dados de Entregas na tabela
		self.Line.setPlaceholderText("Nome(Entregador) ou Cod (Entrega)")
		if self.Line.text() == "" or self.Line.text() == ' ':
			Data = Funcao.SQDB().cursor.execute('SELECT * FROM Objetos_Entregas')
		elif self.Line.text().isnumeric() == True:
			Data = Funcao.SQDB().cursor.execute('SELECT * FROM Objetos_Entregas WHERE Cod = ?', (int(self.Line.text()), ))
		else:
			Data = Funcao.SQDB().cursor.execute('SELECT * FROM Objetos_Entregas WHERE Entregador = ?', (self.Line.text(), ))
		Data = Data.fetchall()
		self.Tabela.setRowCount(len(Data))
		self.Tabela.setColumnCount(8)
		self.Tabela.setStyleSheet('QTableWidget {background-color: rgb(120, 120, 120); font-size: 20px}')
		Coluna = 0

		self.Items = []

		for Item in Data:
			Linha_Dict = {}
			Coluna = 0
			for Row in Item:
				self.LinhaDaTabela = QTableWidgetItem(str(Row))
				self.Tabela.setItem(self.Linha, Coluna, self.LinhaDaTabela)
				self.Tabela.setColumnWidth(Coluna, 200)
				Linha_Dict[str(Row)] = self.LinhaDaTabela
				
				Coluna += 1
			self.Items.append(Linha_Dict)
			self.Linha += 1
		self.Tipo = 'Entregas'
		self.Tabela.cellDoubleClicked.connect(self.Verificar_Selecionados)

	def UserEntregas(self):
		self.Line.setPlaceholderText("Cod (Entrega) ou Nome (Cliente)")
		if self.Line.text() == "" or self.Line.text() == ' ':
			Data = Funcao.SQDB().cursor.execute('SELECT * FROM Objetos_Entregas WHERE (Entregador, Situacao) = (?,?)', (self.UserData[1],self.Situacao))
		elif self.Line.text().isnumeric() == True:
			Data = Funcao.SQDB().cursor.execute('SELECT * FROM Objetos_Entregas WHERE (Cod, Entregador, Situacao) = (?,?, ?)', (int(self.Line.text()), self.UserData[1], self.Situacao))
		else:
			Data = Funcao.SQDB().cursor.execute('SELECT * FROM Objetos_Entregas WHERE (Nome, Situacao) = (?, ?)', (self.Line.text(), self.Situacao))

		Data = Data.fetchall()
		self.Tabela.setRowCount(len(Data))
		self.Tabela.setColumnCount(8)
		self.Tabela.setStyleSheet('QTableWidget {background-color: rgb(120, 120, 120); font-size: 20px}')
		Coluna = 0

		self.Items = []

		for Item in Data:
			Linha_Dict = {}
			Coluna = 0
			for Row in Item:
				self.LinhaDaTabela = QTableWidgetItem(str(Row))
				self.Tabela.setItem(self.Linha, Coluna, self.LinhaDaTabela)
				self.Tabela.setColumnWidth(Coluna, 200)
				Linha_Dict[str(Row)] = self.LinhaDaTabela
				
				Coluna += 1
			self.Items.append(Linha_Dict)
			self.Linha += 1
		self.Tipo = 'UserEntregas'
		self.Tabela.cellDoubleClicked.connect(self.Verificar_Selecionados)


	def Users(self): #Adiciona dados de User na tabela
		if self.Line.text() == "" or self.Line.text() == ' ':
			Data = Funcao.SQDB().cursor.execute('SELECT Cod, Nome, Cpf, Rg, Email, Tel, Status FROM Usuarios WHERE Status = "User"')
		elif self.Line.text().isnumeric() == True:
			Data = Funcao.SQDB().cursor.execute('SELECT Cod, Nome, Cpf, Rg, Email, Tel, Status FROM Usuarios WHERE (Status, Cod) = (?, ?)', ('User', int(self.Line.text()), ))
		else:
			Data = Funcao.SQDB().cursor.execute('SELECT Cod, Nome, Cpf, Rg, Email, Tel, Status FROM Usuarios WHERE (Status, Nome) = (?, ?)', ('User', self.Line.text(), ))
		Data = Data.fetchall()
		self.Tabela.setRowCount(len(Data))
		self.Tabela.setColumnCount(6)
		self.Tabela.setStyleSheet('QTableWidget {background-color: rgb(120, 120, 120); font-size: 20px}')
		Coluna = 0
		self.Items = []

		for Item in Data:
			Linha_Dict = {}
			Coluna = 0
			for Row in Item:
				self.LinhaDaTabela = QTableWidgetItem(str(Row))
				self.Tabela.setItem(self.Linha, Coluna, self.LinhaDaTabela)
				self.Tabela.setColumnWidth(Coluna, 200)
				Linha_Dict[str(Row)] = self.LinhaDaTabela
				Coluna += 1
			self.Items.append(Linha_Dict)
			self.Linha += 1
		self.Tipo = "User"
		self.Tabela.cellDoubleClicked.connect(self.Verificar_Selecionados)

	def Adm(self): #Adiciona dados de Adm na tabela
		if self.Line.text() == "" or self.Line.text() == ' ':
			Data = Funcao.SQDB().cursor.execute('SELECT Cod, Nome, Cpf, Rg, Email, Tel, Status FROM Usuarios WHERE Status = "Adm"')
		elif self.Line.text().isnumeric() == True:
			Data = Funcao.SQDB().cursor.execute('SELECT Cod, Nome, Cpf, Rg, Email, Tel, Status FROM Usuarios WHERE (Status, Cod) = (?, ?)', ('Adm', int(self.Line.text()), ))
		else:
			Data = Funcao.SQDB().cursor.execute('SELECT Cod, Nome, Cpf, Rg, Email, Tel, Status FROM Usuarios WHERE (Status, Nome) = (?, ?)', ('Adm', self.Line.text(), ))
		Data = Data.fetchall()
		self.Tabela.setRowCount(len(Data))
		self.Tabela.setColumnCount(6)
		self.Tabela.setStyleSheet('QTableWidget {background-color: rgb(120, 120, 120); font-size: 20px}')
		Coluna = 0
		self.Items = []

		for Item in Data:
			Linha_Dict = {}
			Coluna = 0
			for Row in Item:
				
				self.LinhaDaTabela = QTableWidgetItem(str(Row))
				self.Tabela.setItem(self.Linha, Coluna, self.LinhaDaTabela)
				self.Tabela.setColumnWidth(Coluna, 200)
				Linha_Dict[str(Row)] = self.LinhaDaTabela
				Coluna += 1
			self.Items.append(Linha_Dict)
			self.Linha += 1

		self.Tipo = "Adm"
		self.Tabela.cellDoubleClicked.connect(self.Verificar_Selecionados)

	def Verificar_Selecionados(self):
		for Item in self.Items:
			for items in Item.values():
				try:
					if items.isSelected() == True:
						data = Item.keys() #Comtem a lista Com os dados da linha selecionada
						lista = []
						for c in data:
							lista.append(c)
						try: self.Window = Label_Items(lista, self.Tipo, self.UserData)
						except: self.Window = Label_Items(lista, self.Tipo)
				except RuntimeError: pass

class DellObjeto_Entrega(QWidget):
	def __init__(self, User):
		super().__init__()
		self.User_Data = User

		self.Layout = QGridLayout(self)

		#Widgets
		self.Line = QLineEdit(self)
		Pesquisar = QPushButton("Pesquisar", self)
		Deletar = QPushButton('Deletar' ,self)
		self.Status = QLabel(self)
		Voltar = QPushButton("Voltar", self)

		#Configurando Widgets
		self.Line.setPlaceholderText("Cod")
		Pesquisar.clicked.connect(self.Pesquisar)
		self.Line.returnPressed.connect(self.Pesquisar)
		Voltar.clicked.connect(self.VoltarWindow)
		Deletar.clicked.connect(self.Deletar)

		#Adicionando Widgets no layout
		self.Layout.addWidget(self.Line, 0, 0, 1, 2)
		self.Layout.addWidget(Pesquisar, 1, 0)
		self.Layout.addWidget(Deletar, 1, 1)
		self.Layout.addWidget(self.Status)
		self.Layout.addWidget(Voltar, 3, 0, 1, 2)

		Janela.setCentralWidget(self)

	def Pesquisar(self):
		try:
			if self.Line.text().isnumeric() == True:
				Data = Funcao.SQDB().cursor.execute('SELECT * FROM Objetos_Entregas WHERE Cod = ?', (int(self.Line.text()), ))
				Data = Data.fetchall()
				Data = Data[0]
				self.Status.setText(f'Cod: {Data[0]} \nNome Cliente: {Data[1]} \nRG: {Data[2]} \nCPF: {Data[3]} \nEnd: {Data[4]} \nCEP: {Data[5]} \nCodCliente: {Data[6]} \nEntregador: {Data[7]}')
			else: self.Status.setText("Codigo Invalido.")
		except: self.Status.setText("Nada Encontrado")

	def Deletar(self):
		if self.Line.text().isnumeric() == True:
			try:
				Funcao.SQDB().DelObjectEntrega(int(self.Line.text()))
				self.Status.setText("Objeto de Entrega deletado dos registros.")
			except: self.Status.setText("Nada encontrado.")
		else: self.Status.setText("Codigo Invalido.")

	def VoltarWindow(self):
		if self.User_Data[8] == 'Adm':
			Janela.setCentralWidget(Window_Adm(self.User_Data))
		if self.User_Data[8] == "User":
			Janela.setCentralWidget(Window_User(self.User_Data))

class Permissoes(QWidget):
	def __init__(self, User):
		super().__init__()
		self.User_Data = User
		self.Permissions = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

		self.Layout = QGridLayout(self)

		#Widgets
		voltar = QPushButton('Voltar', self)
		self.definir = QPushButton("Definir permissoes")

		self.Cadaster_adm_Permission = QPushButton('Sim', self)
		self.Cadaster_User_Permission = QPushButton('Sim', self)
		self.Search_Users_Permission = QPushButton('Sim', self)
		self.Dell_Users_Permission = QPushButton("Sim", self)
		self.AddBojects_Entrega = QPushButton("Sim", self)
		self.Tabela_Entrega = QPushButton("Sim", self)
		self.Tabela_Adms = QPushButton("Sim", self)
		self.Tabela_Users = QPushButton("Sim", self)
		self.Dell_ObjetoEntrega = QPushButton("Sim", self)
		self.Alterar_Permissoes = QPushButton('Sim', self)
		self.AlterarStatus_Entrega = QPushButton('sim', self)

		#Configurando Widgets
		voltar.clicked.connect(self.VoltarWindow)
		self.definir.clicked.connect(self.DefinirPermissoes)

		self.Cadaster_adm_Permission.clicked.connect(self.setPermission_CadasterAdm)
		self.Cadaster_User_Permission.clicked.connect(self.setPermission_CadasterUser)
		self.Search_Users_Permission.clicked.connect(self.setPermission_SearchUsers)
		self.Dell_Users_Permission.clicked.connect(self.setPermission_DellUsers)
		self.AddBojects_Entrega.clicked.connect(self.setPermission_AddObjectEntrega)
		self.Tabela_Entrega.clicked.connect(self.setPermission_TabelaEntregas)
		self.Tabela_Adms.clicked.connect(self.setPermission_TabelaAdms)
		self.Tabela_Users.clicked.connect(self.setPermission_TabelaUsers)
		self.Dell_ObjetoEntrega.clicked.connect(self.setPermission_DellObjetoEntrega)
		self.Alterar_Permissoes.clicked.connect(self.setPermission_AlterarPermissoes)
		self.AlterarStatus_Entrega.clicked.connect(self.setPermission_AlterarStatusEntrega)

		#Inserindo Widgets no layout
		self.Layout.addWidget(self.Cadaster_adm_Permission, 7, 1)
		self.Layout.addWidget(QLabel('Cadastarar Adm', self), 7, 0)
		self.Layout.addWidget(self.Cadaster_User_Permission, 8, 1)
		self.Layout.addWidget(QLabel("Cadastarar User", self), 8, 0)
		self.Layout.addWidget(self.Search_Users_Permission, 9, 1)
		self.Layout.addWidget(QLabel("Pesquisar Usuarios e Adm", self), 9, 0)
		self.Layout.addWidget(self.Dell_Users_Permission,10 , 1)
		self.Layout.addWidget(QLabel("Deletar Users e adms", self), 10, 0)
		self.Layout.addWidget(self.AddBojects_Entrega, 11, 1)
		self.Layout.addWidget(QLabel("Adicionar Objetos para Entrega", self), 11, 0)
		self.Layout.addWidget(self.Tabela_Entrega, 12, 1)
		self.Layout.addWidget(QLabel("Tabela de Entregas", self), 12, 0)
		self.Layout.addWidget(self.Tabela_Adms, 13, 1)
		self.Layout.addWidget(QLabel("Tabela de Adms", self), 13, 0)
		self.Layout.addWidget(self.Tabela_Users, 14, 1)
		self.Layout.addWidget(QLabel("Tabela de User", self), 14, 0)
		self.Layout.addWidget(self.Dell_ObjetoEntrega, 15, 1)
		self.Layout.addWidget(QLabel("Deletar Objeto de Entrega", self), 15, 0)
		self.Layout.addWidget(self.Alterar_Permissoes, 16, 1)
		self.Layout.addWidget(QLabel("Alterar Permissoes de User", self), 16, 0)
		self.Layout.addWidget(self.AlterarStatus_Entrega, 17, 1)
		self.Layout.addWidget(QLabel("Alterar Situação de Entregas", self), 17, 0)

		self.Layout.addWidget(voltar)
		self.Layout.addWidget(self.definir)

		setStyle(self)
		self.show()

	def VoltarWindow(self):
			self.close()

	def DefinirPermissoes(self):
		ShelFile = shelve.open('GestionAPP')
		ShelFile['Permissoes'] = self.Permissions
		ShelFile.close()
	
	def setPermission_CadasterAdm(self):
		if self.Permissions[0] == 1:
			self.Permissions[0] = 0
			self.Cadaster_adm_Permission.setText('Não')
		else:
			self.Permissions[0] = 1
			self.Cadaster_adm_Permission.setText('Sim')

	def setPermission_CadasterUser(self):
		if self.Permissions[1] == 1:
			self.Permissions[1] = 0
			self.Cadaster_User_Permission.setText('Não')
		else:
			self.Permissions[1] = 1
			self.Cadaster_User_Permission.setText('Sim')
	
	def setPermission_SearchUsers(self):
		if self.Permissions[2] == 1:
			self.Permissions[2] = 0
			self.Search_Users_Permission.setText('Não')
		else:
			self.Permissions[2] = 1
			self.Search_Users_Permission.setText('Sim')

	def setPermission_DellUsers(self):
		if self.Permissions[3] == 1:
			self.Permissions[3] = 0
			self.Dell_Users_Permission.setText('Não')
		else:
			self.Permissions[3] = 1
			self.Dell_Users_Permission.setText('Sim')
	
	def setPermission_AddObjectEntrega(self):
		if self.Permissions[4] == 1:
			self.Permissions[4] = 0
			self.AddBojects_Entrega.setText('Não')
		else:
			self.Permissions[4] = 1
			self.AddBojects_Entrega.setText('Sim')
		
	def setPermission_TabelaEntregas(self):
		if self.Permissions[5] == 1:
			self.Permissions[5] = 0
			self.Tabela_Entrega.setText('Não')
		else:
			self.Permissions[5] = 1
			self.Tabela_Entrega.setText('Sim')

	def setPermission_TabelaAdms(self):
		if self.Permissions[6] == 1:
			self.Permissions[6] = 0
			self.Tabela_Adms.setText('Não')
		else:
			self.Permissions[6] = 1
			self.Tabela_Adms.setText('Sim')

	def setPermission_TabelaUsers(self):
		if self.Permissions[7] == 1:
			self.Permissions[7] = 0
			self.Tabela_Users.setText('Não')
		else:
			self.Permissions[7] = 1
			self.Tabela_Users.setText('Sim')

	def setPermission_DellObjetoEntrega(self):
		if self.Permissions[8] == 1:
			self.Permissions[8] = 0
			self.Dell_ObjetoEntrega.setText('Não')
		else:
			self.Permissions[8] = 1
			self.Dell_ObjetoEntrega.setText('Sim')

	def setPermission_AlterarPermissoes(self):
		if self.Permissions[9] == 1:
			self.Permissions[9] = 0
			self.Alterar_Permissoes.setText('Não')
		else:
			self.Permissions[9] = 1
			self.Alterar_Permissoes.setText('Sim')
	
	def setPermission_AlterarStatusEntrega(self):
		if self.Permissions[10] == 1:
			self.Permissions[10] = 0
			self.AlterarStatus_Entrega.setText('Não')
		else:
			self.Permissions[10] = 1
			self.AlterarStatus_Entrega.setText('Sim')

class Label_Items(QWidget):
	def __init__(self, Data, Tipo, User=None):
		super().__init__()
		self.User = User
		self.Tipo = Tipo

		self.Layout = QGridLayout(self)

		self.Label_Config(Data)
		voltar = QPushButton('Voltar', self)
		if Tipo == "Entregas":
			voltar.clicked.connect(lambda : Janela.setCentralWidget(Tabela(self.User)))
		else:
			voltar.clicked.connect(lambda : Janela.setCentralWidget(Tabela(self.User, self.Tipo)))

		self.Layout.addWidget(voltar, 2,0,1,2)
		Janela.setCentralWidget(self)

	def Label_Config(self, Data):
		if self.Tipo == 'Entregas':
			self.Layout.addWidget(QLabel('Codigo: \nCliente:  \nRG: \nCPF: \nEndereço: \nCEP: \nCodigo Cliente: \nEntregador: \nSituação',self), 0, 0)
			self.Layout.addWidget(QLabel(f'{Data[0]} \n{Data[1]} \n{Data[2]} \n{Data[3]} \n{Data[4]} \n{Data[5]} \n{Data[6]} \n{Data[7]} \n{Data[8]}', self), 0, 1)
			self.AlterSituation = QPushButton("Altera Situação", self)
			try: 
				Perm = Funcao.SQDB().GetPermissions(self.User[0])
				Perms = []
				for item in Perm:
					if item.isnumeric() == True:
						Perms.append(item)
				if int(Perms[10]) == 1:
					self.AlterSituation.setEnabled(True)
				else:
					self.AlterSituation.setEnabled(False)
			except:
				pass
			self.Layout.addWidget(self.AlterSituation, 1, 0, 1, 2)
			self.AlterSituation.clicked.connect(lambda : setSituation_Entregas(self.User, Data, self.Tipo, self))
		
		elif self.Tipo == 'UserEntregas':
			self.Layout.addWidget(QLabel('Codigo: \nCliente:  \nRG: \nCPF: \nEndereço: \nCEP: \nCodigo Cliente: \nEntregador: \nSituação',self), 0, 0)
			self.Layout.addWidget(QLabel(f'{Data[0]} \n{Data[1]} \n{Data[2]} \n{Data[3]} \n{Data[4]} \n{Data[5]} \n{Data[6]} \n{Data[7]} \n{Data[8]}', self), 0, 1)
			self.AlterSituation = QPushButton("Altera Situação", self)
			try: 
				Perm = Funcao.SQDB().GetPermissions(self.User[0])
				Perms = []
				for item in Perm:
					if item.isnumeric() == True:
						Perms.append(item)
				if int(Perms[10]) == 1:
					self.AlterSituation.setEnabled(True)
				else:
					self.AlterSituation.setEnabled(False)
			except:
				pass
			self.Layout.addWidget(self.AlterSituation, 1, 0, 1, 2)
			self.AlterSituation.clicked.connect(lambda : setSituation_Entregas(self.User, Data, 'UserEntregas', self))

		elif self.Tipo == 'User':
			self.Layout.addWidget(QLabel('Cod: \nNome: \nCpf: \nRg: \nEmail: \nTel: \nStatus:', self), 0, 0)
			self.Layout.addWidget(QLabel(f'{Data[0]} \n{Data[1]} \n{Data[2]}\n {Data[3]}\n {Data[4]}\n {Data[5]}\n {Data[6]}', self),0 ,1)
			self.Status = QLabel(self)
			Window_SearchUsers.GetPermissions(self, Data[0])
			self.Layout.addWidget(self.Status, 1, 0, 1, 2)
		
		elif self.Tipo == 'Adm':
			self.Layout.addWidget(QLabel('Cod: \nNome: \nCpf: \nRg: \nEmail: \nTel \nStatus', self), 0, 0)
			self.Layout.addWidget(QLabel(f'{Data[0]} \n{Data[1]} \n{Data[2]} \n{Data[3]} \n{Data[4]} \n{Data[5]} \n{Data[6]}', self),0 , 1)

class setSituation_Entregas(QWidget):
	def __init__(self, User, Entrega, Tipo, Window=None):
		super().__init__()
		self.Tipo = Tipo
		try:
			Window.close()
		except: pass
		self.Layout = QGridLayout(self)
		self.Tipo_Situacao = "Em Aberto"

		self.Label = QLabel('Cod: \nNome: \nRG: \nCPF: \nEnd: \nCEP: \nCodigo Cliente: \nEntregador: \nSituação:', self)
		self.Label_Entrega = QLabel(f"{Entrega[0]} \n{Entrega[1]} \n{Entrega[2]}\n {Entrega[3]}\n {Entrega[4]} \n{Entrega[5]} \n{Entrega[6]} \n{Entrega[7]} \n{Entrega[8]}", self)
		self.Situatios = QComboBox(self)
		self.Situatios.insertItem(0, 'Em Aberto')
		self.Situatios.insertItem(1, 'Entregue')
		self.Situatios.insertItem(2, 'Endereço não encontrado')
		Alter = QPushButton('Alterar',self)
		voltar = QPushButton("Voltar", self)
		Status = QLabel(self)
		self.Situatios.activated[str].connect(self.DefinirSituacao)

		self.Layout.addWidget(self.Label, 0, 0)
		self.Layout.addWidget(self.Label_Entrega, 0, 1)
		self.Layout.addWidget(self.Situatios, 1, 0, 1, 2)
		self.Layout.addWidget(Status, 2, 0, 1, 2)
		self.Layout.addWidget(Alter, 3, 0, 1, 2)
		self.Layout.addWidget(voltar, 4, 0, 1, 2)

		voltar.clicked.connect(lambda : Tabela(User, self.Tipo))
		Alter.clicked.connect(lambda : Funcao.SQDB().AlterSituation_Entrega(Entrega[0], self.Tipo_Situacao))
		Alter.clicked.connect(lambda : Status.setText(f"\n\nALTERAÇÂO EFETUADA SITUAÇÂO: {self.Tipo_Situacao}"))

		Janela.setCentralWidget(self)

	def DefinirSituacao(self, text):
		self.Tipo_Situacao = text

def setStyle(Window):
	Window.setStyleSheet('QMainWindow {background-color: rgb(50, 50, 50)}\
		QPushButton {border-radius: 10px; padding: 5px; background-color: rgb(100, 100, 100); border: 1px solid rgb(150, 150, 150)}\
			QPushButton:hover:!pressed {background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(40, 40, 40), stop: 1 rgb(100, 100, 100)); border-style: outset} \
			QWidget {font-size: 15px; font: bold; color: rgb(200, 200, 200); background-color: rgb(50, 50, 50)}\
				QLineEdit {background: rgb(70,70,70); border-radius: 10px; padding: 3px}\
					QComboBox {border-radius: 10px; padding: 2px; background: rgb(100, 100, 100); color: rgb(200, 200, 200)}\
						QComboBox:hover:!pressed {background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(40, 40, 80), stop: 1 rgb(100, 100, 180)); border-style: outset}')
	
	Window.setGeometry(400, 100, 500, 400)
	Window.setWindowTitle('MyApp JIPSlok')

App = QApplication(sys.argv)
Janela = Janela_Principal()
sys.exit(App.exec_())
