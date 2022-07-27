import pandas as pd
import socket
import time
import threading
from PySimpleGUI import PySimpleGUI as sg

caminho = r'C:\Users\pedro\Music\Python\Trab-Final-Redes\Base-Dados.xlsx' #Insira o caminho do arquivo Base-Dados.xlsx aqui
df = pd.read_excel(caminho)
conexoes = []
allAddress = []
compradores = []
ofertas = []
previous_winner = 100
previous_winner2 = 200

def main():
    global lock
    global cln
    df = pd.read_excel(caminho)
    sg.theme('Reddit')
    layoutMain = [
        [sg.Button('Inserir Produto', size=(20,1)), sg.Button('Alterar Produto', size=(20,1))],
        [sg.Button('Excluir Produto', size=(20,1)), sg.Button('Iniciar Leilão', size=(20,1))]
    ]

    janelaMain = sg.Window('Gerenciador Leilão', layoutMain)

    while True:
        eventos, valores = janelaMain.read()
        if eventos == sg.WINDOW_CLOSED:
            break
        if eventos == 'Inserir Produto':
            insereProduto()
        if eventos == 'Alterar Produto':
            alteraProduto()
        if eventos == 'Excluir Produto':
            deletaProduto()
        if eventos == 'Iniciar Leilão':
            iniciaLeilao()

def iniciaLeilao():
    global cln
    global lock
    sg.theme('Reddit')
    layoutIniciaLeilao = [
        [sg.Text('Número de clientes:', size=(20,1)), sg.Input(key='numClientes', size=(10,1))],
        [sg.Button('Confirmar', size=(10,1))]
    ]
    janelaIniciaLeilao = sg.Window('Número Clientes', layoutIniciaLeilao)
    
    while True:
        eventos, valores = janelaIniciaLeilao.read()
        if eventos == sg.WINDOW_CLOSED:
            break
        if eventos == 'Confirmar':
            cln = int(valores['numClientes'])
            lock = threading.Lock()
            janelaIniciaLeilao.close()
            criaSocket()
            bindSocket()
            welcomers()
            



def insereProduto():
    df = pd.read_excel(caminho)
    sg.theme('Reddit')
    layoutinsere = [
        [sg.Text('Nome do Produto: ', size=(20,1)), sg.Input(key='nomeProduto', size=(10,1))],
        [sg.Text('Preço do Produto: ', size=(20,1)), sg.Input(key='precoProduto', size=(10,1))],
        [sg.Button('Confirmar', size=(10,1))]
    ]
    janelaInsere = sg.Window('Insere Produto', layoutinsere)
    while True:
        eventos, valores = janelaInsere.read()
        if eventos == sg.WINDOW_CLOSED:
            break
        if eventos == 'Confirmar':
            rows_count = df.count()['Nome Produto']
            i = int(rows_count)
            df.loc[i,'Nome Produto'] = str(valores['nomeProduto'])
            df.loc[i, 'Preco'] = int(valores['precoProduto'])
            df.loc[::, 'Nome Produto':].to_excel(caminho)
            janelaInsere.close()

def alteraProduto():
    df = pd.read_excel(caminho)
    sg.theme('Reddit')
    layoutAltera = [
        [sg.Text('ID do Produto:', size=(20,1)), sg.Input(key='idProduto', size=(10,1))],
        [sg.Text('Nome do Produto:', size=(20,1)), sg.Input(key='novoNome', size=(10,1))],
        [sg.Text('Preço do Produto:', size=(20,1)), sg.Input(key='novoPreco', size=(10,1))],
        [sg.Button('Confirmar', size=(10,1))]
    ]
    janelaAltera = sg.Window('Altera Produto', layoutAltera)

    while True:
        eventos, valores = janelaAltera.read()
        if eventos == sg.WINDOW_CLOSED:
            break
        if eventos == 'Confirmar':
            rows_count = df.count()['Nome Produto']
            i = int(rows_count)
            idProduto = int(valores['idProduto'])
            if idProduto <= i-1 and idProduto >=0:
                df.loc[idProduto, 'Nome Produto'] = str(valores['novoNome'])
                df.loc[idProduto, 'Preco'] = int(valores['novoPreco'])
                df.loc[::, 'Nome Produto':].to_excel(caminho)
                janelaAltera.close()

def deletaProduto():
    df = pd.read_excel(caminho)
    sg.theme('Reddit')
    layoutDeleta = [
        [sg.Text('ID do do produto que deseja deletar: ', size=(40,1)), sg.Input(key='deletaProduto', size=(10,1))],
        [sg.Button('Confirmar', size=(10,1))]
    ]
    janelaDeleta = sg.Window('Deleta Produto', layoutDeleta)

    while True:
        df = pd.read_excel(caminho)
        eventos, valores = janelaDeleta.read()
        if eventos == sg.WINDOW_CLOSED:
            break
        if eventos == 'Confirmar':
            idProduto = int(valores['deletaProduto'])
            df = df.drop(idProduto)
            df.loc[::, 'Nome Produto':].to_excel(caminho)
            df = pd.read_excel(caminho)
            df.loc[::, 'Nome Produto':].to_excel(caminho)
            janelaDeleta.close()


def criaSocket():
    try:
        global host
        global porta
        global server
        host = "localhost" #Insira aqui o IP
        porta = 8082
        server = socket.socket()
    except socket.error as msg:
        print("Erro ao criar o socket: " + str(msg))

def bindSocket():
    global cln
    try:
        global host
        global porta
        global server
        print("Binding the Port: " + str(porta))
        server.bind((host, porta))
        server.listen(5)
    except socket.error as msg:
        bindSocket()

def welcomers():
    global cln
    for _ in range(cln):
        t = threading.Thread(target=aceitaConexao)
        t.daemon = True
        t.start()
        t.join()

def aceitaConexao():
    i=0
    global cln
    while True:
        try:
            conn, address = server.accept()
            server.setblocking(1)
            conexoes.append(conn)
            allAddress.append(address)
            cl=conexoes[i]
            cl.send(str.encode("Insira seu nome:"))
            compradores.append(str(conn.recv(1024).decode("utf-8")))
            print(compradores[i] + " entrou para o leilão usando a porta: " + str(address[1]))
            conn.send(str.encode("Bem vindo " + compradores[i] + "!"))
            i += 1
            if i == cln:
                leilao()
        except:
            print("Erro ao aceitar conexões")            

def leilao():
    global p
    global previous_winner, previous_winner2
    df = pd.read_excel(caminho)
    rows_count = df.count()['Nome Produto']
    i = int(rows_count)
    for a in range(i):
        p = a
        for x in range(len(conexoes)):
            c = conexoes[x]
            c.send(str.encode("\nLeilão irá inciar em 5 segundos\nProduto: "
                              + str(df.loc[a, 'Nome Produto']) + "\nPreço: " + str(df.loc[p, 'Preco'])))
        time.sleep(5)
        for x in range(len(conexoes)):
            c = conexoes[x]
            c.send(str.encode("Insira sua oferta:"))
            data = str(c.recv(1024).decode("utf-8"))
            ofertas.append(int(data))
        previous_winner = 100
        previous_winner2 = 200
        localizaMaior()

def localizaMaior():
    max = 0
    global previous_winner, previous_winner2
    for i in range(len(ofertas)):
        if ofertas[i] > max:
            max = ofertas[i]
            index = i
    previous_winner2 = previous_winner
    previous_winner = index
    novaChance(index)

def novaChance(winner):
    lock.acquire()
    for x in range(len(conexoes)):
        cl = conexoes[x]
        if x == winner:
            cl.send(str.encode("\nVocê ofereceu o valor máximo, espere as outras ofertas"))
    for x in range(len(conexoes)):
        cl = conexoes[x]
        if x == winner:
            continue
        else:
            cl.send(str.encode(compradores[winner] + " ofereceu R$:" + str(ofertas[winner]) + " por favor ofereça um valor maior, se deseja desistir, insira novamente o valor você ofereceu"))
            data = cl.recv(1024).decode("utf-8")
            ofertas[x] = int(data)
    lock.release()


    result = verificaComprador(winner)
    if result == True:
        localizaMaior()

def verificaComprador(winner):
    df = pd.read_excel(caminho)
    global previous_winner, previous_winner2
    if winner == previous_winner2:
        for x in range(len(conexoes)):
            cl = conexoes[x]
            if x == winner:
                df.loc[p, 'Bid Atual'] = ofertas[winner]
                df.loc[p, 'Comprador'] = compradores[winner]
                df.loc[::, 'Nome Produto':].to_excel(caminho)
                cl.send(str.encode("Parabéns! Você ganhou!!!\nProduto comprado: " + df.loc[p, 'Nome Produto'] + "\nValor do Lance: R$:" + str(ofertas[winner])))
                print(compradores[x] + " comprou o " + df.loc[p, 'Nome Produto'] +"!\nValor do Lance: R$:" +
                                  str(ofertas[winner]))
            else:
                cl.send(str.encode(compradores[winner] + " comprou o " + df.loc[p, 'Nome Produto'] +
                       "\nValor do Lance: R$:" + str(ofertas[winner])))
        del ofertas[:]
        return False
    else:
        return True    

main() 
