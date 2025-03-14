"""
    Ésta biblioteca fue creada para almacenar funciones relacionada con la parte de redes, aquí encontramos las siguientes funciones:
    
    crear_gráfica: nos devuelve una red sintética que fue creada ya sea con el modelo de Albert-Barabási o el de Watts-Strogratz según se le      pida.
    
    obtener_distribucion_grados: nos devuelve la distribucion de grados de una red G en forma de lista en dónde la primera entrada es el         grado y la segunda entrada es la probabilidad de obtener un nodo con el grado de la primera entrada.  
   
    grado_promedio: nos devuelve el grado promedio de la red que le pasemos
    
    ataques: recibe una gráfica y un criterio de ataque, regresa la gráfica atacada por dicho criterio 
    
"""
import networkx as nx
import numpy as np
import random
from collections import Counter


def crear_grafica(modelo,n,m,p):
  if modelo == "watts":
    G = nx.watts_strogatz_graph(n,m,p, seed = None) #No tenemos intéres en estudiar una semilla en particular
  if modelo == "barabasi":
    G = nx.barabasi_albert_graph(n,m, seed = None)
  return G    


def obtener_distribucion_grados(G): #Con está función recibimos una red y devolvemos la distribución de grados de la red
        N = len(G.nodes())
                
        lista_nodos = G.degree() #lista_nodos tiene una lista de los nodos con su identificador y su respectivo grado
        
        lista_grados = [grados for _,grados in lista_nodos] #hacemos una lista que tenga únicamente los grados
        
        #los contamos y con la siguiente linea obtenemos un diccionario ordenado por el grado y su frecuencia
        distribucion_grados = Counter(lista_grados) 
        distribucion_grados = dict(sorted(distribucion_grados.items()))
        
        #Por último armamos una lista con el grado, y la probabilidad de obtener dicho grado, y ésta seria nuestra distribución
        #de grados
        distribucion_grados = [(grado,frecuencia/N) for grado,frecuencia in distribucion_grados.items()]
        return distribucion_grados

    
def grado_promedio(G):
    grados = G.degree()
    return sum(dict(grados).values())/len(G)


def ataques(G,criterio):
    if criterio == 'random':
        nodos = list(G.nodes())
        nodo_elegido = random.choice(nodos)
        G.remove_node(nodo_elegido)
        return G
    elif criterio == 'degree':
        nodo_grado_mayor = max(G.degree, key=lambda x: x[1])[0]
        G.remove_node(nodo_grado_mayor)
        return G
    

