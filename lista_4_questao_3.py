import math

def matriz_anel(n):
    # declaracao da matriz de transicao
    mat = [[0 for j in range (0,n)] for i in range(0,n)]

    # implementa as excecoes:
    mat[0][1] = 1/4
    mat[0][n-1] = 1/4
    mat[n-1][0] = 1/4
    mat[n-1][n-2] = 1/4

    # preenche o restante da matriz
    for i in range(0, n):
        for j in range(0, n):
            if (i==j):
                mat[i][j] = 1/2
            elif (i>0 and i<n-1):
                if ((j==i-1) or (j==i+1)):
                    mat[i][j] = 1/4

    # imprime a matriz
    for i in range(0,n):
            print(str(mat[i]) + " , ")

    return

def matriz_tree(n):

    # declaracao da matriz de transicao
    mat = [[0 for j in range(0, n)] for i in range(0, n)]

    # implementa as excecoes:
    mat[0][0] = 1/2
    mat[0][1] = 1/4
    mat[0][2] = 1/4

    # nivel dos vertices que estao na base da arvore
    m = int(math.sqrt(n))
    print(m)

    # preenche o restante da matriz
    for i in range(1, n):
        for j in range(0, n):
            if (i==j):
                mat[i][j] = 1/2
            elif ((i+1>=2**m) and (i+1<=2**m+(2**m)-1)):
                if ((j+1==(i+1)/2) or (j+1==i/2)):
                    mat[i][j] = 1/2
            elif ((j+1==2*(i+1)) or (j+1==(2*(i+1))+1) or (j+1==(i+1)/2) or (j+1==i/2)):
                    mat[i][j] = 1/6

    # imprime a matriz
    for i in range(0, n):
        print(str(mat[i]) + " , ")

    return

def matriz_grid2d(n):

    # declaracao das variaveis auxiliares
    cont = 0
    aux = 1

    # declaracao da matriz de transicao
    mat = [[0 for j in range(0, n)] for i in range(0, n)]

    # numero de vertices que tem por linha
    raiz_n = int(math.sqrt(n))

    # implementa as probabilidades para os vertices ponta:
    mat[0][0] = 1/2
    mat[0][1] = 1/4
    mat[0][raiz_n] = 1/4
    mat[raiz_n-1][raiz_n-1] = 1/2
    mat[raiz_n-1][raiz_n-2] = 1/4
    mat[raiz_n-1][(2*raiz_n)-1] = 1/4
    mat[n-raiz_n][n-raiz_n] = 1/2
    mat[n-raiz_n][n-raiz_n+1] = 1/4
    mat[n-raiz_n][n-(2*raiz_n)] = 1/4
    mat[n-1][n-1] = 1/2
    mat[n-1][n-2] = 1/4
    mat[n - 1][n-1-raiz_n] = 1/4


    # implementa as probabilidades para os vertices canto - parte 1
    for i in range(1, raiz_n-1):
        mat[i][i] = 1/2
        mat[i][i+1] = 1/6
        mat[i][i-1] = 1/6
        mat[i][i+raiz_n] = 1/6

    # implementa as probabilidades para os vertices canto - parte 2
    for i in range(raiz_n, n-raiz_n):
        mat[i][i] = 1/2
        cont += 1
        if (cont==raiz_n):
            aux += 1
            cont = 0
        if (i == (aux*raiz_n)-1):
            mat[i][i-1] = 1/6
            mat[i][i-raiz_n] = 1/6
            mat[i][i+raiz_n] = 1/6
        elif (i == aux*raiz_n):
            mat[i][i+1] = 1/6
            mat[i][i-raiz_n] = 1/6
            mat[i][i+raiz_n] = 1/6
        else:
            # probabilidades dos vertices centrais
            mat[i][i+1] = 1/8
            mat[i][i-1] = 1/8
            mat[i][i-raiz_n] = 1/8
            mat[i][i+raiz_n] = 1/8

    # implementa as probabilidades para os vertices canto - parte 3
    for i in range(n-raiz_n+1, n-1):
        mat[i][i] = 1/2
        mat[i][i+1] = 1/6
        mat[i][i-1] = 1/6
        mat[i][i-raiz_n] = 1/6

    # imprime a matriz
    for i in range(0, n):
        print(str(mat[i]) + " , ")

    return

# definicao do numero de vertices
n = 16

# metodo para criar a matriz do grafo anel
# matriz_anel(n)

# metodo para criar a matriz do grafo arvore binaria cheia
# matriz_tree(n)

# metodo para criar a matriz do grafo grid 2D (apenas quadrados perfeitos)
matriz_grid2d(n)