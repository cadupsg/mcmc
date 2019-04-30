import requests
import string
import itertools
import random
import numpy as np
from matplotlib import pyplot as plt

# verifica se a URL existe
def checkIfUrlExists(url):
   
    # testa URLs
    try:
        request = requests.get(url)
        if request.status_code == 200:
            # print('Url ' + url + ' existe')
            return 1
        else:
            # print('Url ' + url + ' nao existe')
            return 0
    except:
        # print('Erro ao pegar a url ' + url)
        return 0

# checa todas as possibilidades existentes
def todas_possibilidades(k):

    # declara as variaveis necessarias
    alphabet = list(string.ascii_lowercase)
    cont = 0
    samples = []

    # cria as permutacoes possiveis
    for i in range(1,k+1):
        permutations = itertools.permutations(alphabet, i) # gera permutacoes de tamanho i
        samples += list(permutations)

    for elem in samples: # para cada permutacao, valida a url
        cont += checkIfUrlExists('http://www.' + ''.join(elem) + '.ufrj.br')
        print cont

    return cont

# metodo para escolher uma permutacao aleatoria
def gera_rand(k):
    
    # primeiro deve-se gerar um numero aleatorio de 1 ate k
    num = random.randint(1,4)

    # em seguida retorna uma amostra aleatoria de num elementos com reposicao
    return np.random.choice(list(string.ascii_lowercase), num, replace=True)

# metodo de monte carlo para amostragem aleatoria
def monte_carlo(n_amostras, k):
    
    # calcula a media amostral e a utiliza para estimar o valor de cont
    soma_amostras = 0
    for i in range(n_amostras):
        x = gera_rand(k)
        soma_amostras += checkIfUrlExists('http://www.' + ''.join(x) + '.ufrj.br')
        
        # imprime quantas amostras sao dominios existentes ate o presente momento
        print soma_amostras
    
    return soma_amostras

# gera o grafico do valor do estimador em relacao ao numero de amostras
def mostra_grafico(n, k):

    # definicao de variaveis
    estim_w1 = [0 for i in range(n)]
    estim_w2 = [0 for i in range(n)]

    # calcula o estimador
    for i in xrange (0, n):
        estim_w1[i] = monte_carlo(n, k)
    
    # parte que cria os graficos
    eixoX = np.linspace(0,n,n)

    fig, ax = plt.subplots()
    ax.plot(eixoX, estim_w1, c = 'blue')
    ax.set_title("Estimador de Wn x N")
    ax.set_ylabel("Cont Estimador")

    plt.show()
    plt.close()
    return

# resulCompleto = todas_possibilidades(4)
# print resulCompleto
# resulMC = monte_carlo(10000, 4)
# print resulMC
mostra_grafico(1000, 4)

