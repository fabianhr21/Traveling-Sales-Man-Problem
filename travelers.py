import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random
import itertools

def zeromaker(n):
    zeros = [0]*n
    return zeros

def fun_obj(poblacion,n,G):
    a = 0
    for i in range(n):
        a = a + G[poblacion[i]][poblacion[i+1]]['weight']
    a = 1/a
    return a

def normalizacion(aptitud,muestras):
    apt_norm = zeromaker(muestras)
    for i in range(muestras):
        apt_norm[i] = aptitud[i] / sum(aptitud)
    return apt_norm

def montecarlo(apt_norm,n):
    ind = zeromaker(n)
    alfa = apt_norm.copy()
    for i in range(n):
        CDF = np.cumsum(alfa)
        r = max(CDF)*random.random()
        ind[i] = np.where(CDF >= r)[0][0]
        alfa.pop(ind[i])
    return ind

def fill(hijo,padre1,padre2,CI):
    g = random.randint(1,len(padre1)-4)
    genoma_padre1 = padre1[g:g+3]
    hijo[g:g+3] = genoma_padre1
    a = []
    GEN = []
    cont = 0
    for i in padre2:
        if i not in genoma_padre1 and i != CI:
            a.append(i)
    for i in range(1,len(hijo)-1):
        if hijo[i] not in genoma_padre1 or (i not in range(g,g+3) and hijo[i] == 0):
            hijo[i] = a[cont]
            GEN.append(i)
            cont += 1
    return hijo,GEN,a

def mutacion(hijo,GEN,Pmut):
    mut = random.random()
    if mut <= Pmut:
        r = random.sample(GEN,2)
        a = hijo[r[0]]
        hijo[r[0]] = hijo[r[1]]
        hijo[r[1]] = a  
    return hijo     

def minimos(aptitud,n=2):
    ind = zeromaker(n)
    alfa = aptitud.copy()
    for i in range(n):
        ind[i] = alfa.index(min(alfa))
        alfa.pop(ind[i])
    return ind
        

# Inicialización
def travelers(Muestras=100,Niter=1000,Prob_mut=0.25,Nodos=10,CiudadInicial=0):
    muestras = Muestras
    Niter = Niter
    Pmut = Prob_mut
    poblacion = []
    aptitud = zeromaker(muestras)
    CI = CiudadInicial      # Ciudad inicial y final
    max_apt = zeromaker(Niter)
    # Generacion de grafo
    n = Nodos
    N = list(range(n))
    Nz = N[0:CI] + N[CI+1:]
    G = nx.complete_graph(n)
    # Añade pesos aleatorios
    for (u, v, w) in G.edges(data=True):
        w['weight'] = random.randint(0, 100) 
    pesos = nx.get_edge_attributes(G, 'weight')
    pos = nx.spring_layout(G,seed=63)


    fig1, ax = plt.subplots(layout='constrained')
    nx.draw(G,pos,with_labels=True)
    ax.set_xlabel('x')  # Add an x-label to the axes.
    ax.set_ylabel('y')  # Add a y-label to the axes.
    ax.set_title("Grafo de ciudades")  # Add a title to the axes.
    plt.show()

    # Generacion de poblacion inicial
    for i in range(muestras):
        poblacion.append(zeromaker(n))

    for i in range(muestras):
        poblacion[i] = [CI] + random.sample(Nz,len(Nz)) + [CI]

    #Funcion de aptitud
    for j in range(muestras):
        apt = fun_obj(poblacion[j],n,G)
        aptitud[j] = apt
        
    #Normalización de función de aptitud
    apt_norm = normalizacion(aptitud,muestras)

    ## Algoritmo genético ##
    for i in range(Niter):
    #Selección de padre por método de ranking    
        ind = montecarlo(apt_norm,2)
        padre1 = poblacion[ind[0]]
        padre2 = poblacion[ind[1]]
        hijo1 = [CI] + zeromaker(n-1) + [CI]
        hijo2 = [CI] + zeromaker(n-1) + [CI]
        #Reproduccion ordenada
        hijo1,GEN1,a1 = fill(hijo1,padre1,padre2,CI)
        hijo2,GEN2,a2 = fill(hijo2,padre2,padre1,CI)
        #Mutación
        hijo1 = mutacion(hijo1,GEN1,Pmut)
        hijo2 = mutacion(hijo2,GEN2,Pmut)
        # Reemplazo
        indmin = minimos(aptitud)
        poblacion[indmin[0]] = hijo1
        poblacion[indmin[1]] = hijo2
        aptitud[indmin[0]] = fun_obj(hijo1,n,G)
        aptitud[indmin[1]] = fun_obj(hijo2,n,G)
        apt_norm = normalizacion(aptitud,muestras)
        max_apt[i] = max(aptitud)
        if max_apt[i] >= max(max_apt):
            opt_path = poblacion[aptitud.index(max(aptitud))]
        

    for i in range(Niter):
        max_apt[i] = 1/max_apt[i]

    fig2, ax = plt.subplots(layout='constrained')
    plt.plot(max_apt)
    ax.set_xlabel('Iteraciones')  # Add an x-label to the axes.
    ax.set_ylabel('Distancia')  # Add a y-label to the axes.
    ax.set_title("Función objetivo")  # Add a title to the axes.
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.show()

    opt = zeromaker(n)
    for i in range(n):
        opt[i] = (opt_path[i], opt_path[i+1])
        

    fig3, ax = plt.subplots(layout='constrained')
    nx.draw(G, pos,with_labels=True)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_edges(
        G, pos, edgelist=opt,width=6, alpha=0.5,edge_color="red"
    )
    ax.set_xlabel('x')  # Add an x-label to the axes.
    ax.set_ylabel('y')  # Add a y-label to the axes.
    ax.set_title("Camino óptimo")  # Add a title to the axes.
    plt.show()
    return fig1,fig2,fig3,opt_path

if __name__=="__main__":
    travelers()

    
        
        
        
