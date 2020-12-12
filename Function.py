import sqlite3
from pathlib import Path
from random import randint
from os.path import join as path_join

class SQDB(): #Funcoes com o banco de dados
    def __init__(self):
        super().__init__()

        #Criando ou abrindo a pasta do banco de dados
        Pasta = Path.home() / path_join("MyAppPasta")
        try:
            pastinha = Pasta.mkdir()
        except:
            pass
        self.connection = sqlite3.connect(Pasta / 'Database.db')
        self.cursor = self.connection.cursor()

        self.CreateTables()
        self.Tables_Alterations()

    def Tables_Alterations(self):
        try:
            self.connection.execute('ALTER TABLE Objetos_Entregas ADD COLUMN Situacao text ')
        except: pass

    def CreateTables(self): #Cria as tabelas
        self.cursor.execute('CREATE TABLE IF NOT EXISTS Usuarios(Cod interger primary key, Nome text, Login text, Senha text, Cpf text, Rg text, Email text, Tel interger, Status text)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS Permisseds(Cod interger primary key, Permisseds text)')
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Objetos_Entregas(Cod interger primary key, Nome text, RG text, CPF text, End text, CEP text, CodCliente text, Entregador text)")

    def InsertObject_Entrega(self, Data): #Insere um novo objeto a ser entregue
        cod = randint(100000000, 999999999)
        if Data[6].isnumeric() == True:
            Entregador = SQDB().GetUsers(Data[6], Cod_Name='Cod')
            Entregador = Entregador[1]
        else:
            Entregador = SQDB().GetUsers(Data[6], Cod_Name='Nome')
            Entregador = Entregador[1]
        self.cursor.execute("INSERT INTO Objetos_Entregas(Cod, Nome, RG, CPF, End, CEP, CodCliente, Entregador, Situacao) Values(?,?,?,?,?,?,?,?,?)", (cod, Data[0], Data[1], Data[2], Data[3], Data[4], Data[5], Entregador, 'Em Aberto'))
        self.connection.commit()

    def InsertUsers(self, Data, Permissions = [1,1,1,1], Type = "User"):
        if Type == "User": #Insere User no Banco de dados
            cod = randint(100000000, 999999999)
            self.cursor.execute('INSERT INTO Usuarios(Cod, Nome, Login, Senha, Cpf, Rg, Email, Tel, Status) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)', (cod, Data[0], Data[1], Data[2], Data[3], Data[4], Data[5], Data[6], "User"))
            self.cursor.execute('INSERT INTO Permisseds(Cod, Permisseds) VALUES(?, ?)', (cod, Permissions))
            self.connection.commit()

        if Type == "Adm": #Insere Adm no Banco de dados
            self.cursor.execute('INSERT INTO Usuarios(Cod, Nome, Login, Senha, Cpf, Rg, Email, Tel, Status) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)', (randint(100000000, 999999999), Data[0], Data[1], Data[2], Data[3], Data[4], Data[5], Data[6], "Adm"))
            self.connection.commit()

    def DelObjectEntrega(self, Cod):
        self.cursor.execute("DELETE FROM Objetos_Entregas WHERE Cod = ?", (Cod, ))
        self.connection.commit()
    
    def GetUsers(self, Data, Type = "Default", Cod_Name = 0):
        if Cod_Name == 0 or Cod_Name == 'Login':
            Cod_Name = 0
        elif Cod_Name == 1 or Cod_Name == "Cod":
            Cod_Name = 1
        elif Cod_Name == 2 or Cod_Name == "Nome":
            Cod_Name = 2

        if Type == "Default" and Cod_Name == 0: #Procurar um Adm ou User no Banco de dados
            User = self.cursor.execute('SELECT * FROM Usuarios WHERE Login = ?', (Data, ))

        elif Type == "Default" and Cod_Name == 1: #Procurar um Adm ou User no Banco de dados
            User = self.cursor.execute('SELECT * FROM Usuarios WHERE Cod = ?', (Data, ))
        
        elif Type == "Default" and Cod_Name == 2: #Procurar um Adm ou User no Banco de dados
            User = self.cursor.execute('SELECT * FROM Usuarios WHERE Nome = ?', (Data, ))

        elif Type == "Adm" and Cod_Name == 0: #Procura um adm no banco de dados
            User = self.cursor.execute('SELECT * FROM Usuarios WHERE (Login, Status) = (?, ?)', (Data, "Adm"))

        elif Type == "Adm" and Cod_Name == 1: #Procura um adm no banco de dados
            User = self.cursor.execute('SELECT * FROM Usuarios WHERE (Cod, Status) = (?, ?)', (Data, "Adm"))
        
        elif Type == "Adm" and Cod_Name == 2: #Procura um adm no banco de dados
            User = self.cursor.execute('SELECT * FROM Usuarios WHERE (Nome, Status) = (?, ?)', (Data, "Adm"))

        elif Type == "User" and Cod_Name == 0: #Procura um User no banco de dados
            User = self.cursor.execute('SELECT * FROM Usuarios WHERE (Login, Status) = (?, ?)', (Data, "User"))
        
        elif Type == "User" and Cod_Name == 1: #Procura um User no banco de dados
            User = self.cursor.execute('SELECT * FROM Usuarios WHERE (Cod, Status) = (?, ?)', (Data, "User"))
        
        elif Type == "User" and Cod_Name == 2: #Procura um User no banco de dados
            User = self.cursor.execute('SELECT * FROM Usuarios WHERE (Nome, Status) = (?, ?)', (Data, "User"))

        User = User.fetchall()
        try:
            return User[0]
        except:
            return User
    
    def GetPermissions(self, Cod):
        data = self.cursor.execute('SELECT Permisseds FROM Permisseds WHERE Cod = ?', (Cod, ))
        data = data.fetchall()
        return data[0][0]
    
    def DellUsers(self, Cod):
        self.cursor.execute("DELETE FROM Usuarios WHERE Cod = ?", (Cod, ))
        self.cursor.execute("DELETE FROM Permisseds WHERE Cod = ?", (Cod, ))
        self.connection.commit()
    
    def AlterSituation_Entrega(self, Cod, Situation):
        assert 'Entregue' in Situation or 'Em Aberto' in Situation or 'Endereço não encontrado' in Situation, 'Situacao Infomada Incorretamente!'
        
        self.cursor.execute("UPDATE Objetos_Entregas SET Situacao = ? WHERE Cod = ?", (Situation, Cod))
        self.connection.commit()

class VerifyDatas(): #Verificador de dados
    def __init__(self):
        pass
    
    def VerifyCampos(self, data, Type='Login'): #Verificas se todos os campos estao preenchidos
        Verify = True
        for Item in data:
            if len(str(Item)) != 0: 
                if Item != ' ': pass
                else: Verify = False
            else: Verify = False
        if Type != "Login":
            db = SQDB().GetUsers(data[0], Cod_Name='Nome')
            try:
                if db[1] == data[0]:
                    Verify = False
            except: pass
        return Verify
