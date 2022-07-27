import socket
from PySimpleGUI import PySimpleGUI as sg
import time

server = socket.socket()
host = "localhost"
porta = 8082

server.connect((host, porta))

def main():
    while True:
        data = (server.recv(1024).decode("utf-8"))
        try:
            last = data.split()
        except:
            continue
        if data == "Insira seu nome:":
            sg.theme('Reddit')
            layoutNome = [
                [sg.Text(data), sg.Input(key='nome')],
                [sg.Button('Confirmar')]
            ]
            janelaNome = sg.Window('Nome', layoutNome)
            while True:
                eventos, valores = janelaNome.read()
                if eventos == sg.WINDOW_CLOSED:
                    break
                if eventos == 'Confirmar':
                    data = str(valores['nome'])
                    server.send(str.encode(data))
                    janelaNome.close()

        elif data == "Insira sua oferta:":
            sg.theme('Reddit')
            layoutOferta = [
                [sg.Text(data), sg.Input(key='oferta')],
                [sg.Button('Confirmar')]
            ]
            janelaOferta = sg.Window('Insira a Oferta', layoutOferta)

            while True:
                eventos, valores = janelaOferta.read()
                if eventos == sg.WINDOW_CLOSED:
                    break
                if eventos == 'Confirmar':
                    data = str(valores['oferta'])
                    server.send(str.encode(data))
                    janelaOferta.close()

        elif last == "ofereceu":
            sg.theme('Reddit')
            layoutOfereceu = [
                [sg.Text(data)],
                [sg.Input(key='ofereceu')],
                [sg.Button('Confirmar')]
            ]
            janelaOfereceu = sg.Window('Oferta', layoutOfereceu)

            while True:
                eventos, valores = janelaOfereceu.read()
                if eventos == sg.WIN_CLOSED:
                    break
                if eventos == 'Confirmar':
                    data2 = str(valores['ofereceu'])
                    server.send(str.encode(data2))
                    janelaOfereceu.close()
        else:
            sg.theme('Reddit')
            layoutMensagem = [
                [sg.Text(data)]
            ]
            janelaMensagem = sg.Window('Mensagem', layoutMensagem)

            while True:
                eventos, valores = janelaMensagem.read()
                if eventos == sg.WINDOW_CLOSED:
                    break
                time.sleep(5)
                janelaMensagem.close()

main()