#
#
# Author: Raul Crespo
# Create date: 12 november 2019
# Description: programa para gerenciar compras e vendas de assentos de um cinema
# Name: cinema-tickets
# Link: https://snipsave.com/user/crespo/snippet/REHAWrVX2v8TZYaVPX/
#
#

import os.path


class ControladorAssentos:
    def __init__(self, linhas, colunas):
        self.__listaAssentos = []
        self.__linhas = linhas
        self.__colunas = colunas
        self.__count = 0
        self.__total = 0
        self.__ingressosDevolvidos = 0
        self.__ocupacaoSala = 0
        self.__zfill_helper = len(str((self.__linhas * self.__colunas) - 1))

    def criar_assentos(self):
        valor = 20
        for num in range(self.__linhas * self.__colunas):
            self.__listaAssentos.append(Assento(num, valor, 1))
            self.__count += 1

            if self.__count == self.__colunas:
                valor -= 1
                if valor == 0:
                    valor = 1
                self.__count = 0

    def mostrar_assentos(self):
        for assento in self.__listaAssentos:
            numero = assento.getNumero()

            if self.__count == self.__colunas:
                print('')
                self.__count = 0
            if assento.getDisponivel() == 0:
                print('x' * self.__zfill_helper, end=' ')
            else:
                print(f'{str(numero).zfill(self.__zfill_helper)}', end=' ')
            self.__count += 1

    def comprarAssentos(self, numeros_assentos):
        sucesso = True
        mensagem_retorno = 'Assentos comprados.'
        assentos = numeros_assentos.split(',')

        for assento in assentos:
            try:
                if int(assento) > ((self.__linhas * self.__colunas) - 1) or int(assento) < 0:
                    mensagem_retorno = f'\nAssento {assento} não existe.'
                    sucesso = False
                    break
            except (TypeError, ValueError):
                mensagem_retorno = f'Erro, "{assento}" não é um assento.'
                sucesso = False
                break

            if self.__listaAssentos[int(assento)].getDisponivel() == 1:
                sucesso = True
            else:
                sucesso = False
                mensagem_retorno = f'Assento {assento} ocupado. Compra cancelada.'
                break

        if sucesso:
            for assento in assentos:
                self.__listaAssentos[int(assento)].setDisponivel(0)
                self.__total += self.__listaAssentos[int(assento)].getPreco()
                self.__ocupacaoSala += 1

        return sucesso, mensagem_retorno

    def devolverAssentos(self, numeros_assentos):
        sucesso = True
        mensagem_retorno = 'Assentos devolvidos.'
        assentos = numeros_assentos.split(',')

        for assento in assentos:
            try:
                if int(assento) > ((self.__linhas * self.__colunas) - 1) or int(assento) < 0:
                    mensagem_retorno = f'\nAssento {assento} não existe.'
                    sucesso = False
                    break
            except (TypeError, ValueError):
                mensagem_retorno = f'Erro, "{assento}" não é um assento.'
                sucesso = False
                break

            if self.__listaAssentos[int(assento)].getDisponivel() == 0:
                sucesso = True
            else:
                sucesso = False
                mensagem_retorno = f'Assento {assento} livre. Devolução cancelada.'
                break

        if sucesso:
            for assento in assentos:
                self.__listaAssentos[int(assento)].setDisponivel(1)
                self.__total -= (self.__listaAssentos[int(assento)].getPreco() * 0.9)
                self.__ocupacaoSala -= 1
                self.__ingressosDevolvidos += 1

        return sucesso, mensagem_retorno

    def emitirResumo(self):
        print(f'Ocupação da sala no momento: {self.__ocupacaoSala}')
        print(f'Quantidade de ingressos devolvidos: {self.__ingressosDevolvidos}')
        print('Valor total apurado: R$%.2f' % self.__total, end='')

    def salvarArquivo(self):
        f = open('dados_cinema.txt', 'w')
        f.write(f'{self.__linhas}:{self.__colunas}:{self.__total}:{self.__ingressosDevolvidos}:{self.__ocupacaoSala}')
        for assento in self.__listaAssentos:
            f.write(f'\n{assento.getNumero()}:{assento.getPreco()}:{assento.getDisponivel()}')
        f.close()

    def carregarArquivo(self):
        self.__total = float(dados[2])
        self.__ingressosDevolvidos = int(dados[3])
        self.__ocupacaoSala = int(dados[4])
        for linha in f:
            linha = linha.replace('\n', '').replace('\r', '')
            linha = linha.split(':')
            self.__listaAssentos.append(Assento(int(linha[0]), int(linha[1]), int(linha[2])))


class Assento:
    def __init__(self, numero, preco, disponivel):
        self.__numero = numero
        self.__preco = preco
        self.__disponivel = disponivel

    def getNumero(self):
        return self.__numero

    def setNumero(self, novo_numero):
        self.__numero = novo_numero

    def getPreco(self):
        return self.__preco

    def getDisponivel(self):
        return self.__disponivel

    def setDisponivel(self, novo_disponivel):
        self.__disponivel = novo_disponivel


escolha = 'y'

while True:
    if os.path.exists('dados_cinema.txt'):
        escolha = input('Sessão já existente registrada. Deseja começar uma nova? (y/n) ')
    else:
        escolha = 'y'
    if escolha.lower() == 'n':
        f = open('dados_cinema.txt', 'r')
        dados = f.readline().split(':')
        controladorAssentos = ControladorAssentos(int(dados[0]), int(dados[1]))
        controladorAssentos.carregarArquivo()
        break
    elif escolha.lower() == 'y':
        while True:
            try:
                linhas = int(input('Informe o número de linhas: '))
                colunas = int(input('Informe o número de colunas: '))
            except (TypeError, ValueError):
                """ Here, you will catch a error if the user types a invalid option in variable option
                    like strings, floats or booleans, and return back to the menu. """
                print('\nApenas é aceito números inteiros como opções.\nOpções válidas: 1, 2, 3 e 4.\n')
                continue
            controladorAssentos = ControladorAssentos(linhas, colunas)
            controladorAssentos.criar_assentos()
            break
        break
    else:
        print('Não entendi o que você quis dizer...')
        continue

while True:
    print('')
    controladorAssentos.mostrar_assentos()

    print('\n\n'
          'Bem vindo ao sistema de venda de ingressos.\n'
          'Escolha a operação:\n'
          '1- Comprar ingressos\n'
          '2- Devolver ingressos\n'
          '3- Resumo das vendas\n'
          '4- Sair\n')
    try:
        escolha = int(input('Digite sua escolha: '))
    except (TypeError, ValueError):
        """ Here, you will catch a error if the user types a invalid option in variable option
            like strings, floats or booleans, and return back to the menu. """
        print('\nApenas é aceito números inteiros como opções.\nOpções válidas: 1, 2, 3 e 4.')
        continue

    if escolha == 1:
        lista = input('Quais assentos deseja comprar: ')

        print(controladorAssentos.comprarAssentos(lista)[1])

    elif escolha == 2:
        lista = input('Quais assentos deseja devolver: ')

        print(controladorAssentos.devolverAssentos(lista)[1])

    elif escolha == 3:
        controladorAssentos.emitirResumo()

    elif escolha == 4:
        controladorAssentos.salvarArquivo()
        break

    else:
        print('\nNúmero de 1 até 4 apenas.')
