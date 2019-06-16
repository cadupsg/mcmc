import random
import copy
import math
import time

# metodo que verifica as viabilidades das configuracoes geradas
def verificaViabilidade(demanda, gtUnid, custo, tOn, tOff, decisao, n, temp):

    # declara a variavel booleana que indica se a configuracao em questao eh viavel ou nao
    verificaBol = True

    # verifica se ha atendimento a restricao de demanda
    for i in range(0, temp):
        if not ((sum(decisao[i][j] * gtUnid[j] for j in range(0, n)) >= demanda[i])):
            verificaBol = False;
            break;

    # somente deve-se testar as outras restricoes se a primeira for cumprida
    if verificaBol:

        for i in range(0, n):
            for j in range(1, temp):

                # verifica se nao violou tempo minimo ligado
                if (j + tOn[i] - 1 <= temp - 1):
                    if not (sum(decisao[k][i] for k in range(j, j + tOn[i])) >= tOn[i] * (
                            decisao[j][i] - decisao[j - 1][i])):
                        verificaBol = False
                        break;
                else:
                    if not (sum(decisao[k][i] for k in range(j, temp)) >= (temp - j) * (
                            decisao[j][i] - decisao[j - 1][i])):
                        verificaBol = False
                        break;

                # verifica se violou o tempo minimo desligado
                if (j + tOff[i] - 1 <= temp - 1):
                    if not (sum((1 - decisao[k][i]) for k in range(j, j + tOff[i])) >= tOff[i] * (
                            decisao[j - 1][i] - decisao[j][i])):
                        verificaBol = False
                        break;
                else:
                    if not (sum((1 - decisao[k][i]) for k in range(j, temp)) >= (temp - j) * (
                            decisao[j - 1][i] - decisao[j][i])):
                        verificaBol = False
                        break;

    return verificaBol

# metodo que gera uma configuracao de unidades a partir de variaveis aleatorias uniformes
def geraConfiguracao(n, temp, decisao):

    # declara as variaveis auxiliares
    decisaoAlt = copy.deepcopy(decisao)
    isValida = False # variavel booleana que indica se a configuracao em questao eh viavel ou nao neste metodo

    while not (isValida):

        x = random.randint(0, temp - 1)  # gera um valor uniforme para alterar a posicao da linha - referente ao tempo
        y = random.randint(0, n - 1)  # gera um valor uniforme para alterar a posicao da coluna - referente a unit

        # se a unit y no temp x estiver ligada, ela sera desligada neste tempo
        # esta mesma unit tambem sera desligada durante o intervalo de tempo em que deve permanecer desligada
        if (decisaoAlt[x][y] == 1):
            if (x + tOff[y] - 1 <= temp - 1):
                for i in range(x, x + tOff[y]):
                    decisaoAlt[i][y] = 0
            else:
                for i in range(x, temp):
                    decisaoAlt[i][y] = 0

        # se a unit y no temp x estiver desligada, ela sera ligada neste tempo
        # esta mesma unit tambem sera ligada durante o intervalo de tempo em que deve permanecer ligada
        else:
            if (x + tOn[y] - 1 <= temp - 1):
                for i in range(x, x + tOn[y]):
                    decisaoAlt[i][y] = 1
            else:
                for i in range(x, temp):
                    decisaoAlt[i][y] = 1

        # caham o metodo que verifica a viabilidade da configuracao gerada
        isValida = verificaViabilidade(demanda, gtUnid, custo, tOn, tOff, decisaoAlt, n, temp)

        if not (isValida):
            # caso nao seja viavel, volta-se com a ultima configuracao valida encontrada
            decisaoAlt = copy.deepcopy(decisao)

    return decisaoAlt

# metodo que calcula o valor da funcao objeto - minimizacao do custo de geracao
def fobjetivo(s, custo, n, temp):

    # inicializa variavel que armazena o valor da funcao objetivo
    valorFObj = 0

    for i in range(0, temp):
        valorFObj += sum(s[i][j] * custo[j] for j in range(0, n))

    return valorFObj

# metodo que executa o Simulated Annealing
def simulatedAnnealing(n, temp, decisao, custo, alfa, saMax, t0):

    # solucao atual - sol - pega a solucao inicial (configuracao valida inicial)
    sol = copy.deepcopy(decisao)

    # contador do numero de iteracoes na temperatura t
    iterT = 0

    # temperatura corrente comeca com a temperatura inicial
    tatual = t0

    # inicializacao de variaveis auxiliares
    x = 0 # variavel aleatoria uniforme de 0 a 1
    delta = 0 # diferenca nos valores da funcao objetivo
    valorFO = fobjetivo(decisao, custo, n, temp) # valor da FO na configuracao inicial
    valoresFO = [] # array que armazena os valores das FO encontrados
    valoresFO.append(valorFO)
    configViavel = copy.deepcopy(decisao) # variavel que armazena a config viavel gerada
    ultimaConfigViavel = copy.deepcopy(decisao) # variavel que armazena a ultima config viavel (anterior)

    while (tatual > 0.0001):
        while (iterT < saMax):

            iterT += 1
            configViavel = geraConfiguracao(n, temp, ultimaConfigViavel)
            delta = fobjetivo(configViavel, custo, n, temp) - fobjetivo(ultimaConfigViavel, custo, n, temp)

            if (delta < 0):
                ultimaConfigViavel = configViavel
                valoresFO.append(fobjetivo(ultimaConfigViavel, custo, n, temp))
                if (fobjetivo(ultimaConfigViavel, custo, n, temp) < fobjetivo(sol, custo, n, temp)):
                    sol = ultimaConfigViavel
                    valorFO = fobjetivo(ultimaConfigViavel, custo, n, temp)
            else:
                x = random.uniform(0, 1)
                if (x < math.exp(-(delta / tatual))):
                    ultimaConfigViavel = configViavel

        # decrescimento linear
        tatual = tatual * alfa

        # decrescimento exponencial
        # tatual = t0*(alfa**tatual)

        # outras funcoes
        # tatual = t0*math.exp(-alfa*tatual)
        # tatual = alfa/(math.log(tatual + alfa, math.e))

        iterT = 0

    # imprime os valores armazenados dentro do array e, em seguida, o valor da FO da solucao otima encontrada
    print(valoresFO)
    print(valorFO)

    # encerra o metodo retornando a solucao otima encontrada
    return sol

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# ENTRADA DOS DADOS !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# declaracao dos vetores que serao utilizados nas analises
vetorSolucoes = []
vetorCustos = []
vetorTempos = []

"""# CASO COM N = 5 E T = 5
# numero de unidades termicas
n = 5

# discretizacao do tempo
temp = 5

# alfa = taxa de resfriamento 0<alfa<1
alfa = 0.9

# saMax = numero maximo de iteracoes para cada temperatura
saMax = 500

# t0 = temperatura inicial
t0 = 100000000

# popula vetores principais
demanda = [250, 210, 185, 210, 270] # demanda por tempo em horas
gtUnid = [100, 70, 40, 150, 120] # geracao em MWh
custo = [200, 165, 170, 210, 200] # custo em RS por MWh
tOn = [1,3,2,1,2] # tempo em horas
tOff = [1,3,2,1,2] # tempo em horas
decisao = [[1 for x in range(0,n)] for y in range (0, temp)]"""

# CASO COM N = 10 e T = 24
# numero de unidades termicas
n = 10

# discretizacao do tempo
temp = 24

# alfa = taxa de resfriamento 0<alfa<1
alfa = 0.9

# saMax = numero maximo de iteracoes para cada temperatura
saMax = 500

# t0 = temperatura inicial
t0 = 100000000

# popula vetores principais
demanda = [440, 478, 228, 342, 468, 411, 345, 395, 260, 364, 242, 475,
           480, 357, 313, 205, 304, 400, 291, 223, 255, 385, 319, 332]  # demanda por tempo em horas
gtUnid = [50, 60, 70, 30, 110, 80, 50, 40, 90, 65]  # geracao em MWh
custo = [200, 150, 220, 190, 250, 260, 195, 200, 230, 240]  # custo em RS por MWh
tOn = [5, 10, 3, 6, 2, 1, 4, 2, 5, 2]  # tempo em horas
tOff = [5, 10, 3, 6, 2, 1, 4, 2, 5, 2]  # tempo em horas
decisao = [[1 for x in range(0, n)] for y in range(0, temp)]

solucao = simulatedAnnealing(n, temp, decisao, custo, alfa, saMax, t0)

# chama metodo que realiza o simulated Annealing e imprime a solucao
"""for i in range(0, 30):
    print (i)
    ini = time.time()
    solucao = simulatedAnnealing(n, temp, decisao, custo, alfa, saMax, t0)
    fim = time.time()
    vetorSolucoes.append(solucao)
    vetorCustos.append(fobjetivo(solucao, custo, n, temp))
    vetorTempos.append(fim-ini)

print(vetorSolucoes)
print(vetorCustos)
print(vetorTempos)"""

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# ANALISE POS-OTIMIZACAO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# verifica as geracoes totais por unidade de tempo
"""for i in range(0,24):
    print(sum(solucao[i][j]*gtUnid[j] for j in range (0,10)))"""

