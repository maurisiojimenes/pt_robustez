"""
"""

import networkx as nx
import numpy as np

def entropia_normalizada_1(G): #Donde G es la red
    grados_nodos = list(G.degree())
    grados_nodos = [grados_nodos[i][1] for i in range(len(grados_nodos))]
    
    k_min = min(grados_nodos) if len(grados_nodos) != 0 else 0
    k_max = max(grados_nodos) if len(grados_nodos) != 0 else 0
    
    lista_k_i = [(k_i - k_min)/(k_max - k_min) if k_max != k_min else (k_i - k_min) for k_i in grados_nodos]#Hasta aquí obtengo los k_i normalizados
    
    suma = sum(lista_k_i)    
    return -sum((k_i / suma) * np.log(k_i / suma) for k_i in lista_k_i if k_i>0)


def entropia_normalizada_2(G): # Donde G es la red
    N = len(G.nodes())
    grados_nodos = list(G.degree())
    grados_nodos = [grados_nodos[i][1] for i in range(len(grados_nodos))]
    
    k_min = min(grados_nodos) if len(grados_nodos) != 0 else 0
    k_max = max(grados_nodos) if len(grados_nodos) != 0 else 0
    
    lista_k_i = [(k_i - k_min) / (k_max - k_min) if k_max != k_min else (k_i - k_min) for k_i in grados_nodos]  # Normalizamos los grados
    suma = sum(lista_k_i)
    
    return -sum((k_i / suma) * np.log10(k_i / suma) for k_i in lista_k_i if k_i>0)

def entropia_shanon_1(G):#G es la red y q es un número natural
    grados_nodos = list(G.degree())
    grados_nodos = [grados_nodos[i][1] for i in range(len(grados_nodos))]
    
    suma = sum(grados_nodos)
    
    return -sum((k_i/suma) * np.log(k_i/suma) for k_i in grados_nodos if k_i>0)
    
def entropia_shanon_2(G):#G es la red y q es un número natural
    grados_nodos = list(G.degree())
    grados_nodos = [grados_nodos[i][1] for i in range(len(grados_nodos))]
    suma = sum(grados_nodos)
    
    return -sum((k_i/suma) * np.log10(k_i/suma) for k_i in grados_nodos if k_i>0)
    
    
def entropia_distribucion_1(G):
    grados_nodos = list(G.degree())
    grados_nodos = [grados_nodos[i][1] for i in range(len(grados_nodos))]
    N = len(G.nodes())
    
    distribucion_grados = {}
    
    for grado in grados_nodos: #Con este for obtenemos la distribucion de los grados
        if grado not in distribucion_grados:
            distribucion_grados[grado] = 0 #Si no está el grado, lo inicializamos
        distribucion_grados[grado] += 1 #Luego aumentamos el conteo del grado
        
    distribucion_grados = list(distribucion_grados.values())

    distribucion_grados = [grado/N for grado in distribucion_grados] #Dividimos el conteo entre N pq asi está definida p(k)
    
    return -sum(p_k * np.log(p_k) for p_k in distribucion_grados)


def entropia_distribucion_2(G):
    grados_nodos = list(G.degree())
    grados_nodos = [grados_nodos[i][1] for i in range(len(grados_nodos))]
    N = len(G.nodes())
    
    distribucion_grados = {}
    
    for grado in grados_nodos: #Con este for obtenemos la distribucion de los grados
        if grado not in distribucion_grados:
            distribucion_grados[grado] = 0 #Si no está el grado, lo inicializamos
        distribucion_grados[grado] += 1 #Luego aumentamos el conteo del grado
        
    distribucion_grados = list(distribucion_grados.values())

    distribucion_grados = [grado/N for grado in distribucion_grados] #Dividimos el conteo entre N pq asi está definida p(k)
    
    return -sum(p_k * np.log10(p_k) for p_k in distribucion_grados)

