"""
"""

import networkx as nx
import numpy as np

def entropia_shanon_normalizada(G): #Donde G es la red
    grados_nodos = list(G.degree())
    grados_nodos = [grados_nodos[i][1] for i in range(len(grados_nodos))]
    
    k_min = min(grados_nodos) if len(grados_nodos) != 0 else 0
    k_max = max(grados_nodos) if len(grados_nodos) != 0 else 0
    
    if k_min == k_max: #Aquí si en la red el grado mínimo es igual al grado máximo la entropía debe ser 0
        return 0
    
    lista_k_i = [(k_i - k_min)/(k_max - k_min) if k_max != k_min else (k_i - k_min) for k_i in grados_nodos]#Hasta aquí obtengo los k_i normalizados
    
    suma = sum(lista_k_i)
    return -sum((k_i / suma) * np.log(k_i / suma) for k_i in lista_k_i if k_i>0)


def entropia_shanon_1(G):#G es la red y q es un número natural 
    grados_nodos = list(G.degree())
    grados_nodos = [grados_nodos[i][1] for i in range(len(grados_nodos))]
    suma = sum(grados_nodos)
    return -sum((k_i/suma) * np.log(k_i/suma) for k_i in grados_nodos if k_i>0)
    
    
def entropia_shanon_2(G):
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

def entropia_tsallis_1(G,q):
    N = len(G)
    nodos_grados=list(G.degree())#Hasta aquí tenemos una lista de tuplas [(id_nodo,grado)]
    grados = [nodos_grados[i][1] for i in range(N)]#Me quedo únicamente con los grados de los nodos
    suma = sum(grados)#Esta seria la suma que va en el denominador de nuestras p_i
    if suma==0:
        return 0#En caso de que la suma=0, la red está totalmente desconectada, por lo que regresaremos 0 cómo entropía
    p_i = [grado/suma for grado in grados] #Aquí ya tenemos la lista de las p_i
    p_i_q = [pow(p,q) for p in p_i]#Ahora ya tenemos la lista de las p_i elevadas a q
    return (1-sum(p_i_q))/(q-1)

def entropia_tsallis_2(G,q):
    N = len(G)
    nodos_grados=list(G.degree())#Hasta aquí tenemos la lista de tuplas de la forma [(id_nodo,grado)]
    grados = [nodos_grados[i][1] for i in range(N)]#Nos quedamos únicamente con los grados
    distribucion = {}#Hacemos un diccionario para contar cuántas veces aparece un grado en particular
    for grado in grados:
        if grado not in distribucion:#Si aún no lo hemos contado ninguna vez, lo inicializamos
            distribucion[grado] = 0#En 0 porque de cualquier forma vamos a sumarle uno en el siguiente paso
        distribucion[grado]+=1#Aumentamos el conteo del grado
    distribucion=list(distribucion.values())#Nos quedamos únicamente con el conteo
    distribucion=[grado/N for grado in distribucion]
    distribucion=[pow(p,q) for p in distribucion]
    return (1-sum(distribucion))/(q-1)

    
def completar_Q(P, Q):
    dict_Q = dict(Q)
    
    Q_completa = [(grado, dict_Q.get(grado, 0)) for grado, _ in P]
    
    return Q_completa

def DKL_3(P,Q): #En está función vamos a obtener dos funciones de densidad de probabilidad discretas, que son las distribuciones de grados y vamos a calcular
              #la DKL, en general se toma a P: distribución real, Q: distribución aproximada, fitteada o atacada, queremos ver cuánta perdida de información hay 
              #En cada ataque o fallo en la red
    #Para empezar como Q viene de una red con al menos 1 nodo menos que P, va a ser menor que P, por lo que debemos corregir ese punto:
    Q = completar_Q(P,Q)
    
    probabilidades_P = [probabilidad for _,probabilidad in P]

    probabilidades_Q = [probabilidad for _,probabilidad in Q]

    epsilon = 1e-10
    probabilidades_P = [max(p, epsilon) for p in probabilidades_P]
    probabilidades_Q = [max(q, epsilon) for q in probabilidades_Q]
    
    return sum(p * np.log(p / q) for p, q in zip(probabilidades_P, probabilidades_Q))

def DKL_1(P,Q,n): #En está función vamos a calcular la DKL entre las distribuciones inducidas por H_1(G). En general P va a ser la distribución antes de
                #Empezar a atacar la red, mientras que Q va a ser la distribución en un escenario de fallos/ataques después de i iteraciones
                #Dónde i = 1,2,3,...,N. Naturalmente cómo Q es atacada no va a ser del mismo tamaño que P, por lo que vamos a acompletar está lista de 
                #probabilidades para que tengan el mismo tamaño, y vamos a tomar en cuenta parcialmente estás probabilidades usando un epsilon <<< 0
                #n es la lista de nodos que se han ido quitando en orden y va a servirnos para completar la distribución Q.

    nodos = [id for id,_ in Q]
    nodos_faltantes = [(id,0) for id in n if id not in nodos]
    Q = Q + nodos_faltantes
    Q = sorted(Q, key=lambda x:x[0])
    
    probabilidades_P = [probabilidad for _,probabilidad in P]
    probabilidades_Q = [probabilidad for _,probabilidad in Q]
    epsilon = 1e-10
    probabilidades_P = [max(p, epsilon) for p in probabilidades_P]
    probabilidades_Q = [max(q, epsilon) for q in probabilidades_Q]
    
    return sum(p * np.log(p / q) for p, q in zip(probabilidades_P, probabilidades_Q))

    



    