#AFD em Python
#Nome: Othavio Christmann Correa - Matricula: 162586

estados = []      #Estados
alfabeto = []       #Alfabeto
transicoes = {}        #Função de Transição
estado_inicial = None     #Estado Inicial
estados_finais = []          #Estados Finais

#Primeira Parte:
 
while True:
    estado = input("Informe um estado:")
    if estado == "":
        break

    estados.append(estado)

while True:
    caracter = input("Informe um caracter:")
    if caracter == "":
        break

    alfabeto.append(caracter)

for estado in estados:
    transicoes_local = {}
    for caracter in alfabeto:
        transicao = input(f"({estado},{caracter}) =")
        
        transicoes_local[caracter] = transicao

    transicoes[estado] = transicoes_local

estado_inicial = input("Informe o estado inicial:")

while True:
    estado_final = input("Informe um estado final:")
    if estado_final == "":
        break

    estados_finais.append(estado_final)

#Segunda Parte:

while True:
    estado_atual = estado_inicial
    palavra = input("Informe uma palavra:")         #O AFD reconhece ("aceita") a palavra

    for caracter in palavra:
        proximo_estado = transicoes[estado_atual][caracter]

        estado_atual = proximo_estado

    if estado_atual in estados_finais:
        print("Palavra aceita")
    else:
        print("Palavra não aceita")

