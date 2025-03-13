import networkx as nx
import numpy as np
import random

def ataque(G,criterio):
  #elegir un nodo aleatorio
  #clustering coeficent
  #random
  #degree
  #grafica medida vs porcentaje de atacados
  if criterio == 'clustering':
    print("Aquí realizamos el ataque por clustering, si lo tuviera hecho")

  elif criterio == 'random':
    nodos = list(G.nodes())
    nodo_elegido = random.choice(nodos)
    G.remove_node(nodo_elegido)
    return G

  elif criterio == 'degree':
    nodo_grado_mayor = max(G.degree, key=lambda x: x[1])[0]
    G.remove_node(nodo_grado_mayor)

  else:
    print("El criterio no es válido")

  return G


def W(G):
    return 1/len(G.nodes())

#Criterio: criterio por el cual se va a atacar a la red G
#f: función de measure, es decir la medida que se toma en cuenta para la red
#w: peso para normalizar f
#G: la red
#i: número de nodos que se van a atacar
def indice_robustez(criterio,f,w,G,i):
    N = len(G.nodes())
    f_i = [f(G)]
    w_i = [w(G)]
    for _ in range(i):
        G = ataque(G,criterio)#No ocupe hacer un if, simplemente mando el criterio por el cual se ataca
        f_i.append(f(G))
        w_i.append(W(G))
    return sum(w*f for w,f in zip(w_i,f_i))/N

