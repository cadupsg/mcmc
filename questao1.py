import random
import math as m
import numpy as np
from matplotlib import pyplot as plt

# monte carlo
def monte_carlo(n):

    # numero de amostras dentro da parabola
    amostra = 0

    for i in xrange(0, n):
        # gera uniforme em [0, 2].
        x = random.uniform(0,2)
        y = random.uniform(0,2)
        # verifica se esta dentro da parabola
        if y < (-1*(x**2)) + 2:
            amostra += 1
    
    return (float(amostra)/n)*3

def mostra_grafico(n):

    # definicao de variaveis
    estim_m = [0 for i in range(n)]
    erro_m = [0 for i in range(n)]

    # calcula o estimador e o erro
    for i in xrange (1, n+1):
        estim_m[i-1] = monte_carlo(i)
        erro_m[i-1] = (abs(estim_m[i-1]-m.sqrt(2)))/m.sqrt(2)
        print estim_m[i-1]
    
    # parte que cria os graficos
    eixoX = np.linspace(0,n,n)

    fig1, ax1 = plt.subplots()
    ax1.plot(eixoX, erro_m, ls = '-', lw = '1.5', c = 'blue')
    ax1.set_title("Erro Estimador de Nn x n")
    ax1.set_ylabel("Erro")
    ax1.set_xscale("log")
    plt.show()
    plt.close()
    
    return

# calcula a media do estimador
# Ep = monte_carlo(1000000)
# print(Ep)

# cria o grafico
mostra_grafico(10000)