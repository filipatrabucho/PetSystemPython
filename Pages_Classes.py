# Importa as bibliotecas necessárias
import csv
from tkinter import *
from tkinter import Label, PhotoImage, messagebox,Tk
from tkinter.ttk import Treeview
import pandas as pd

# Define o diretório local como o diretório onde o script está sendo executado
from os.path import split as pth  
localdir = pth(__file__)[0]+'\\' # Coloca a identificação do ficheiro num array dividindo o nome e a path

# Define cores usadas na interface gráfica
cor1 = "#b1bae5" # lilás claro background color
cor2 = "#000000" # preto

# classe base (superclasse) para janelas da aplicação
class Janela:
    menu = {}

    def __init__(self, title=''):
        self.janela = None
        self.title = title

    # Método para criar uma janela
    def CriaJanela(self):
        self.janela = Tk()
        self.janela.title(self.title)
        self.janela.geometry ("1244x700+150+0")
        self.janela.configure(bg=cor1)
        self.janela.resizable(False,False)

    # Método para adicionar imagem à janela
    def CriaImage(self, img):
        self.img = PhotoImage(file = localdir+img, master=self.janela)
        label_imagem = Label(self.janela, image=self.img)
        label_imagem.place(x=0, y=0)

    # Método para adicionar uma etiqueta de texto à janela   
    def CriaLabel(self,text,x,y):
        Label(self.janela, text=text, font="Calibri 14", bg=cor1).place(x=x, y=y)

    # Método para adicionar um campo de entrada de texto à janela
    def CriaEntry(self,x, y):
        entry = Entry(self.janela, width=30, font="Calibri 14")
        entry.pack(pady=10)
        entry.place(x=x, y=y)
        return entry

    # Método para adicionar um botão à janela
    def CriaButton(self, text, x,y,command):
        button = Button(self.janela, text=text, width=9, height= 1,
                        font="Calibri 14", command=command,
                        bg=cor1, fg=cor2, relief="raised", overrelief="ridge")
        button.pack()
        button.place(x=x, y=y)

    # Método para fechar a janela
    def FechaJanela(self):
        if self.janela:
            self.janela.destroy()
            self.janela = None

    # Método para exibir a janela
    def MostraJanela(self):
        if self.janela == None:
            self.CriaJanela()

        self.janela.mainloop()

    # Método para limpar os campos de entrada de texto
    def LimpaCampos(self, campos):
        for x in campos:
            x.delete(0,END)

    # Métodos para interação entre as janelas (linhas 76 à 94)
    def Consulta(self):
        if Janela.menu['Consulta']:
            self.FechaJanela()
            Janela.menu['Consulta'].MostraJanela()

    def Animal(self):
        if Janela.menu['Animal']:
            self.FechaJanela()
            Janela.menu['Animal'].MostraJanela()

    def Menu(self):
        if Janela.menu['Menu']:
            self.FechaJanela()
            Janela.menu['Menu'].MostraJanela()
    
    def Creditos(self):
        if Janela.menu['Créditos']:
            self.FechaJanela()
            Janela.menu['Créditos'].MostraJanela()

    # Métodos para criar menu lateral 
    def MenuLateral(self):
        def Botao(text, y, command):
            button = Button(self.janela, text=text, font="Calibri 14",
                            bg=cor1, fg=cor2, width=10, command=command,
                            relief="raised", overrelief="ridge")
            button.pack()
            button.place(x=70, y=y)

        # Adicionar Menu lateral
        Botao("Menu", 300, self.Menu)
        Botao("Sair", 350, self.FechaJanela)

# subclasse Animal da superclasse Janela
class Animal(Janela):
    def CriaJanela(self):
        super().CriaJanela() # Chama o método CriaJanela da classe base (Janela)

        #Criar Imagem
        self.CriaImage("4.png")

       # Criar Label para os campos de entrada
        self.CriaLabel("Nº Chip: ",430,120)
        self.CriaLabel("Nome: ", 430,160)
        self.CriaLabel("Idade: ", 430,200)
        self.CriaLabel("Raça: ", 430,240)
        self.CriaLabel("Porte: ", 430,280)
        self.CriaLabel("Peso: ", 430,320)
        self.CriaLabel("Dono: ", 430,360)
        self.CriaLabel("Tel.: ", 430,400)
        self.CriaLabel("Nif: ", 430,440)
        self.CriaLabel("Morada: ", 430,480)

        # Adicionar TextBox para inserção de dados de entrada
        self.nr_animal_entry=self.CriaEntry(510,120)
        self.name_entry=self.CriaEntry(510,160)
        self.idade_entry=self.CriaEntry(510,200)
        self.raca_entry=self.CriaEntry(510,240)
        self.porte_entry=self.CriaEntry(510,280)
        self.peso_entry=self.CriaEntry(510,320)
        self.dono_entry=self.CriaEntry(510,360)
        self.contato_entry=self.CriaEntry(510,400)
        self.nif_entry=self.CriaEntry(510,440)
        self.morada_entry=self.CriaEntry(510,480)

        # Adiciona botões para adicionar, procurar, editar e eliminar animal
        self.CriaButton("Adicionar", 400,555, self.GuardarAnimal)
        self.CriaButton("Procurar", 520,555, self.ProcurarAnimal)
        self.CriaButton("Editar", 640,555, self.EditarAnimal)
        self.CriaButton("Eliminar", 760,555, self.EliminarAnimal)

        # Adicionar título a janela
        label =Label(text="Inserir Animal", font="Calibri 36 bold",bg=cor1)
        label.place(x=500, y=25)
        
        # Adiciona um menu lateral à janela
        self.MenuLateral()    

    # Chama o método LimpaCampos da classe base (Janela) para limpar os campos comuns
    def LimpaCampos(self):
        super().LimpaCampos([self.nr_animal_entry,
                   self.name_entry,
                   self.idade_entry,
                   self.raca_entry,
                   self.porte_entry,
                   self.peso_entry,
                   self.dono_entry,
                   self.contato_entry,
                   self.nif_entry,
                   self.morada_entry
                   ])
        
    #Guardar Animal em Csv e DataFrame
    def GuardarAnimal(self):
        #Inputs do Form Adicionar animal
        listInputs=[self.nr_animal_entry.get(),
                    self.name_entry.get(),
                    self.idade_entry.get(),
                    self.raca_entry.get(),
                    self.porte_entry.get(),
                    self.peso_entry.get(),
                    self.dono_entry.get(),
                    self.contato_entry.get(),
                    self.nif_entry.get(),
                    self.morada_entry.get()
                    ]
    
        # Adiciona os dados (coletados acima) ao arquivo 'DadosAnimal.csv'
        f = open('DadosAnimal.csv', 'a')
        writer = csv.writer(f)
        writer.writerow(listInputs)
        f.close()
        print("Animal Adicionado")
       
        #Mensagem a validar os dados guardados
        messagebox.showinfo("Dados Animal","Dados Guardados Com Sucesso") 
        self.LimpaCampos()

    # Função Procura Animal e mostra os dados na janela
    def ProcurarAnimal(self):
        # Lê as informações do arquivo 'DadosAnimal.csv' em um DataFrame
        df = pd.read_csv('DadosAnimal.csv') 
        print(df)
        #Recebe o nrChip que o utilizador colocou e transforma a string em inteiro
        query=int(self.nr_animal_entry.get())

        # Procura no DataFrame os dados do animal com o número de chip fornecido, retornando numa lista
        pesquisa=df[df["Nr Chip"]==query]
        print(df["Nr Chip"]==query)
        print(type(pesquisa))
        print(pesquisa.shape[0])

        # Verifica que o número  do chip introduzido encontra-se no ficheiro DadosAnimal.csv
        if not pesquisa.empty:
            #Exibe os valores da lista do animal encontrado em cada caixa de texto
            self.name_entry.insert(0, str(pesquisa.iloc[0, 1]))
            self.idade_entry.insert(0, str(pesquisa.iloc[0, 2]))
            self.raca_entry.insert(0, str(pesquisa.iloc[0, 3]))
            self.porte_entry.insert(0, str(pesquisa.iloc[0, 4]))
            self.peso_entry.insert(0, str(pesquisa.iloc[0, 5]))
            self.dono_entry.insert(0, str(pesquisa.iloc[0, 6]))
            self.contato_entry.insert(0, str(pesquisa.iloc[0, 7]))
            self.nif_entry.insert(0, str(pesquisa.iloc[0, 8]))
            self.morada_entry.insert(0, str(pesquisa.iloc[0, 9])) 
        else:  
            messagebox.showerror("Procurar","Animal não se encontra na base de dados")
    
    # Edita o Animal Procurado na Função ProcurarAnimal
    def EditarAnimal(self): 
        nome_arquivo="DadosAnimal.csv" # Ficheiro onde se encontram os dados dos Animais
        chip = int(self.nr_animal_entry.get()) #Lê numero chip introduzido pelo utilizador e transforma de string para inteiro
      
        dg = pd.read_csv(nome_arquivo) # Carregar o arquivo CSV
                  
        animal_index = dg.index[dg['Nr Chip'] == chip].tolist() #Cria lista com o index correspondente ao nr chip colocado pelo utilizador
        #Verifica se existe o numero chip introduzido
        if animal_index: # Atualizar os dados Consulta introduzidos pelo utilizador com a função get
            dg.at[animal_index[0], 'Nr Chip'] = chip
            dg.at[animal_index[0], 'Nome'] = self.name_entry.get()
            dg.at[animal_index[0], 'Idade'] = self.idade_entry.get()
            dg.at[animal_index[0], 'Raca'] = self.raca_entry.get()
            dg.at[animal_index[0], 'Porte'] = self.porte_entry.get()
            dg.at[animal_index[0], 'Peso'] = self.peso_entry.get()
            dg.at[animal_index[0], 'Dono'] = self.dono_entry.get()
            dg.at[animal_index[0], 'Contato'] = self.contato_entry.get()
            dg.at[animal_index[0], 'Nif'] = self.nif_entry.get()
            dg.at[animal_index[0], 'Morada'] = self.morada_entry.get()

            # Guarda o DataFrame de volta no arquivo CSV
            dg.to_csv(nome_arquivo, index=False)
        
            messagebox.showinfo("Alterar Dados","Dados do animal alterados com sucesso!") # Mensagem a verificar que os dados foram atualizados com sucesso
        
        else: # Caso não exista o numero do chip mostra mensagem de erro
            messagebox.showerror("Alterar Dados","Animal não encontrado no arquivo.")
        
        #Limpa Campos de Textboxs
        self.LimpaCampos()
  
    # Função recebe nr chip, encontra linha onde o mesmo está guardado, por fim retira-o da lista
    def EliminarAnimal(self): 
        nome_arquivo = "DadosAnimal.csv"
        dg = pd.read_csv(nome_arquivo)
        chip = int(self.nr_animal_entry.get())
        
        dg = dg[dg['Nr Chip'] != chip] # Filtra o DataFrame para manter apenas as linhas que não correspondem ao chip fornecido
        
        if len(dg) < len(pd.read_csv(nome_arquivo)): # Verifica se alguma linha foi removida
            messagebox.showinfo("System Vet Py", "Animal removido com sucesso")
        else:
            messagebox.showerror("System Vet Py", "Erro a remover animal")

        # Guarda o DataFrame de volta no arquivo CSV
        dg.to_csv(nome_arquivo, index=False)
    
        # Limpa Campos de Textboxs
        self.LimpaCampos()

# subclasse consulta da Superclasse Janela
class Consulta(Janela):
    def CriaJanela(self):
        super().CriaJanela() # Chama o método CriaJanela da classe base (Janela)
        
        # Cria uma imagem na janela
        self.CriaImage("5.png")

        # Criar Label para os campos de entrada
        self.CriaLabel("Id: ", 800,250)
        self.CriaLabel("Data: ",800,300)
        self.CriaLabel("Motivo: ",800,350)
        self.CriaLabel("Obs: ",800,400)
        self.CriaLabel("Nr Chip: ",800,450)
        
        # Adicionar TextBox para inserção de dados de entrada
        self.idconsulta_entry=self.CriaEntry(880,250)
        self.dataconsulta_entry=self.CriaEntry(880,300)
        self.motivoconsulta_entry=self.CriaEntry(880,350)
        self.obsconsulta_entry=self.CriaEntry(880,400)
        self.biconsulta_entry=self.CriaEntry(880,450)
        
        # Input para procurar
        self.CriaLabel("Nr Chip: ", 300,200)
        self.procura_entry=self.CriaEntry(400,200)        
        self.CriaButton("Procurar", 725,195, self.ProcurarConsulta) # Adiciona um botão para iniciar a busca

        # Adiciona botões para adicionar, remover, editar e selecionar consultas
        self.CriaButton("Adicionar", 1085,525, self.MarcarConsulta)
        self.CriaButton("Desmarcar", 955,525, self.EliminarConsulta)
        self.CriaButton("Editar", 825,525, self.EditaConsulta)
        self.CriaButton("Selecionar", 465,525, self.SelecionarConsulta)
        
        # Adiciona um menu lateral à janela
        self.MenuLateral()

         # Adiciona um título à janela
        label =Label(text="Consultas", font="Calibri 36 bold",bg=cor1)
        label.place(x=450, y=70)

        # Cria uma tabela para exibir as consultas com base no número do chip introduzido
        campos=["Id","Data","Motivo","Obs","Bi Animal"]
        self.trv=Treeview(self.janela,selectmode="browse")
        self.trv.grid(row=2,column=1,columnspan=3,pady=10)
        self.trv.place(x=300,y=250)
        self.trv["height"]=10
        self.trv["show"]="headings"
        self.trv["columns"]=campos

        # Configura as colunas da tabela
        for i in campos:
            self.trv.column(i,width=90,anchor='c')
            self.trv.heading(i,text=i)

    # Chama o método LimpaCampos da classe base (Janela) para limpar os campos comuns
    def LimpaCampos(self):
        super().LimpaCampos([self.idconsulta_entry,
                   self.dataconsulta_entry,
                   self.motivoconsulta_entry,
                   self.obsconsulta_entry,
                   self.biconsulta_entry])
    
    # Guarda Informaçao das Consultas em ficheiro Csv
    def MarcarConsulta(self):
        # Cria uma lista com os dados inseridos
        listDados=[self.idconsulta_entry.get(),
                   self.dataconsulta_entry.get(),
                   self.motivoconsulta_entry.get(),
                   self.obsconsulta_entry.get(),
                   self.biconsulta_entry.get()]
     
        # Abre o arquivo CSV em modo de adição e adiciona novos dados 
        g = open('DadosConsultas.csv', 'a')
        writer = csv.writer(g)
        writer.writerow(listDados)
        
        # Fecha o arquivo CSV após a escrita
        g.close()
        print("Dados Inseridos")
        
        # Limpa Campos de Textboxs
        self.LimpaCampos()
    
    # Procura consultas com base no número do chip do animal
    def ProcurarConsulta(self):

        # Lê os dados do arquivo CSV e carrega em DataFrame
        df= pd.read_csv('DadosConsultas.csv')  
        l1=list(df)

        # Filtra os dados
        query=self.procura_entry.get() # Obtém um valor de consulta a partir do campo de entrada
        print(query)
        str1=df["Bi Animal"]==int(query) # cria uma série booleana indicando se o valor da coluna "Bi Animal" é igual ao valor inserido
        df2=df[(str1)] # Filtra o DataFrame original para incluir apenas as linhas onde a condição é verdadeira
        r_set=df2.to_numpy().tolist() # resultando em um novo DataFrame apenas as consultas correspondentes ao número do chip do animal
        
        # Exibe na Treeview as consultas encontradas
        for dt in r_set:
            v=[r for r in dt]
            self.trv.insert("",'end',iid=v[0],values=v)

    # Eliminar Consulta
    def EliminarConsulta(self):
        # Lê os dados do arquivo CSV
        nome_arquivo="DadosConsultas.csv"
        df= pd.read_csv(nome_arquivo)  
        
        # Obtém o ID da consulta a ser eliminada
        id = int(self.idconsulta_entry.get())

        # Filtra o DataFrame para verificar a linha que corresponde ao id introduzido pela Procura       
        df = df[df['Id'] != id]
        if len(df) < len(pd.read_csv(nome_arquivo)):
            messagebox.showinfo("System Vet Py", "Consulta Removida com Sucesso ")
        else:
            messagebox.showerror("System Vet Py", "Erro a Editar Consulta")

        # Salva o DataFrame de volta no arquivo CSV
        df.to_csv(nome_arquivo, index=False)
        self.trv.delete(*self.trv.get_children())
        
        # Limpa Campos de Textboxs
        self.LimpaCampos()

    # Selecionar Consulta
    def SelecionarConsulta(self):
        self.LimpaCampos()
        
        # Obtém o ID selecionado na Treeview
        selected =self.trv.focus()

        # Obtém os valores da linha selecionada na Treeview
        values=self.trv.item(selected,"values")
       
        # Preenche os campos de entrada com os valores obtidos
        self.idconsulta_entry.insert(0,values[0])
        self.dataconsulta_entry.insert(0,values[1])
        self.motivoconsulta_entry.insert(0,values[2])
        self.obsconsulta_entry.insert(0,values[3])
        self.biconsulta_entry.insert(0,values[4])

    def EditaConsulta(self):
        nome_arquivo="DadosConsultas.csv"
        
        # Obtém o número do chip do animal
        chip = int(self.procura_entry.get())

        # Obtém os valores dos campos de entrada
        id = self.idconsulta_entry.get()
        data= self.dataconsulta_entry.get()
        motivo=self.motivoconsulta_entry.get()
        obs=self.obsconsulta_entry.get()
        bi=self.biconsulta_entry.get()
    
         # Carrega o arquivo CSV como DataFrame
        df = pd.read_csv(nome_arquivo)
            
        # Verificar se o animal está no DataFrame
        animal_index = df.index[df['Bi Animal'] == chip].tolist()
        
        if animal_index:
            # Atualiza os dados da consulta no DataFrame
            df.at[animal_index[0], 'Id'] = id
            df.at[animal_index[0], 'Data'] = data
            df.at[animal_index[0], 'Motivo'] = motivo
            df.at[animal_index[0], 'Obs'] = obs
            df.at[animal_index[0], 'Bi Animal'] = bi
                
            # Salvar o DataFrame de volta ao arquivo CSV e exibe mensagem de sucesso na alteração
            df.to_csv(nome_arquivo, index=False)
            self.trv.delete(*self.trv.get_children())
            self.ProcurarConsulta()
            messagebox.showinfo("Alterar Dados","Dados do animal alterados com sucesso!")
        
        # Exibe mensagem de erro se o animal não for encontrado no arquivo
        else:  
            messagebox.showerror("Alterar Dados","Animal não encontrado no arquivo.")

# subclasse Creditos da superclasse Janela          
class Creditos(Janela):
    def CriaJanela(self):
        super().CriaJanela() # Chama o método CriaJanela da superclasse para criar a janela
        
        # Cria uma imagem na janela
        self.CriaImage("7.png")
      
        # Exibir Menu lateral
        self.MenuLateral()

# subclasse Menu da superclasse Janela 
class Menu(Janela): 
    def CriaJanela(self):
        super().CriaJanela() # Chama o método CriaJanela da superclasse para criar a janela
        
        # Cria imagem na janela
        self.CriaImage("3.png")
        
        # Cria botões para as opções de menu
        self.CriaButton('Animal', 450,400, self.Animal)
        self.CriaButton('Consulta', 570,400, self.Consulta)
        self.CriaButton('Créditos', 690,400, self.Creditos)
        
        # Exibir Menu lateral
        self.MenuLateral()

    # Inicia o loop principal da janela
    def menu(self):
        self.janela.mainloop()

# subclasse login da superclasse Janela 
class Login(Janela):
    def CriaJanela(self):
        super().CriaJanela() # Chama o método CriaJanela da superclasse para criar a janela
        
        # Cria imagem na janela
        self.CriaImage("2.png") 

        # Cria campos de entrada para o nome de usuário e senha 
        self.usernametext=StringVar()
        self.passwordtext=StringVar()
        label = Label(text="Username:", font="Calibri 16",bg=cor1)
        label.place(x=450, y=400)
        username_input=Entry(textvariable=self.usernametext, font="Calibri 16",bg=cor1)
        username_input.place(x=550, y=400)
        label = Label(text="Password:", font="Calibri 16",bg=cor1)
        label.place(x=450, y=450)
        password_input=Entry(textvariable=self.passwordtext,show="*", font="Calibri 16",bg=cor1)
        password_input.place(x=550, y=455)

        # Cria botão para realizar o login
        self.CriaButton("Entrar", 552,505, self.ValidateLogs)
        
    #Funçao que Verifica se o Username e Pass estão corretos
    def ValidateLogs(self):
        userid=self.usernametext.get()
        passwordid=self.passwordtext.get()

        if userid=="carla" and passwordid=="2559":
            messagebox.showinfo("Log in com Sucesso","Bem-vinda Carla")

            # Cria um dicionário de menus disponíveis
            Janela.menu={'Consulta': Consulta('Consulta'),
                         'Animal': Animal('Animal'),
                         'Créditos': Creditos('Créditos'),
                         'Menu': Menu('Menu')
                        }
            
            # Fecha a janela de login e mostra o menu principal
            self.FechaJanela()
            Janela.menu['Menu'].MostraJanela()
            print("Lista de menus aberta")
        
        # Exibe mensagem de erro se os dados estiverem incorretos
        else:
            messagebox.showerror("Erro","Erro nos dados introduzidos")

# subclasse Inicio da superclasse Janela  
class Inicio(Janela):
    def CriaJanela(self):
        super().CriaJanela()  # Chama o método CriaJanela da superclasse para criar a janela

        # Cria imagem na janela
        self.CriaImage("1.png") 

        # Cria botão para iniciar o login
        button = Button(self.janela, text="LOGIN", width=9, height= 1,
                        font="Calibri 18", command=self.Login,
                        bg=cor1, fg=cor2, relief="raised", overrelief="ridge")
        button.pack()
        button.place(x=520, y=500)
 
    # Função para iniciar a janela de login
    def Login(self):
        self.FechaJanela()
        login = Login()
        login.MostraJanela()

# Instancia e mostra a janela inicial
inicio = Inicio('Início')
inicio.MostraJanela()
