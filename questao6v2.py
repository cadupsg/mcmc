import numpy as np
import math
import random
from matplotlib import pyplot as plt

def gera_rand(valor_min, valor_max):
    
    #gera valor aleatorio a partir de uma distribuicao uniforme entre os valores a e b (limites de integracao)
    limite = valor_max - valor_min
    num = random.uniform(0,1)
    return valor_min + limite*num

def f_de_x(x, alfa):
    
    # retorna a funcao que sera integrada
    return (x**alfa)

def monte_carlo(n_amostras, alfa, a, b):
    
    # calcula a media amostral e a utiliza para estimar o valor de g(alfa,a,b)
    soma_amostras = 0
    for i in range(n_amostras):
        x = gera_rand(a, b)
        soma_amostras += f_de_x(x, alfa)
    
    return (b - a) * float(soma_amostras/n_amostras) 

def integral_analitica(alfa, a , b):
    alfa = float(alfa)
    a = float(a)
    b = float(b)
    return (((b**(alfa+1))/(alfa+1))-((a**(alfa+1))/(alfa+1)))

def mostra_grafico(n):

     # definicao de variaveis
    estim_g1 = [[0 for i in range(n)] for ialfa in range(3)]
    erro1 = [[0 for i in range(n)] for ialfa in range(3)]
    estim_g2 = [[0 for i in range(n)] for ialfa in range(3)]
    erro2 = [[0 for i in range(n)] for ialfa in range(3)]
    estim_g3 = [[0 for i in range(n)] for ialfa in range(3)]
    erro3 = [[0 for i in range(n)] for ialfa in range(3)]

    # calcula os erros para cada alfa e b
    for alfa in xrange(1,4):
        g_analitica1 = integral_analitica(alfa, 0, 1)
        g_analitica2 = integral_analitica(alfa, 0, 2)
        g_analitica3 = integral_analitica(alfa, 0, 4)
        for i in xrange(1, n+1):
            estim_g1[alfa-1][i-1] = monte_carlo(i, alfa, 0, 1)
            erro1[alfa-1][i-1] = (abs(estim_g1[alfa-1][i-1]-g_analitica1))/g_analitica1
            estim_g2[alfa-1][i-1] = monte_carlo(i, alfa, 0, 2)
            erro2[alfa-1][i-1] = (abs(estim_g2[alfa-1][i-1]-g_analitica2))/g_analitica2
            estim_g3[alfa-1][i-1] = monte_carlo(i, alfa, 0, 4)
            erro3[alfa-1][i-1] = (abs(estim_g3[alfa-1][i-1]-g_analitica3))/g_analitica3
    
    # parte que cria os graficos
    cor = ['red', 'blue', 'magenta', 'k']
    eixoX = np.linspace(0,n,n)
    for i in xrange(0,3):
        # cria figura com 3 graficos
        fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(20, 20), dpi=80)

        axes[0].plot(eixoX, erro1[i], ls = '-', lw = '1.5', c = cor[0])
        axes[0].set_ylabel('Erro', color='k')
        axes[0].set_title('b = 1', color='k')

        axes[1].plot(eixoX, erro2[i], ls = '-', lw = '1.5', c = cor[1])
        axes[1].set_ylabel('Erro', color='k')
        axes[1].set_title('b = 2', color='k')

        axes[2].plot(eixoX, erro3[i], ls = '-', lw = '1.5', c = cor[2])
        axes[2].set_ylabel('Erro', color='k')
        axes[2].set_title('b = 4', color='k')

        # Colocando titulo do grafico
        fig.suptitle('Erro x N - Alfa = ' + str(i+1) )
    
    plt.show()
    plt.close()
    return

# calcula a media do estimador
# Ep = monte_carlo(1000000)
# print(Ep)

# cria o grafico
mostra_grafico(10000)