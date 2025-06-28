"""
    Ésta biblioteca fue creada para almacenar funciones relacionada con la parte de redes, aquí encontramos las siguientes funciones:
    
    crear_gráfica: nos devuelve una red sintética que fue creada ya sea con el modelo de Albert-Barabási o el de Watts-Strogratz según se le      pida.
    
    densidad: nos devuelve la densidad de una red. Necesitamos, además de la red G, N que será el número de nodos que había en la red antes 
    de iniciar los ataques/fallos en la red.
    
    obtener_distribucion_grados: nos devuelve la distribucion de grados de una red G en forma de lista en dónde la primera entrada es el         grado y la segunda entrada es la probabilidad de obtener un nodo con el grado de la primera entrada.  
   
    grado_promedio: nos devuelve el grado promedio de la red que le pasemos.
    
    componentes conexas: le damos la red y nos devuelve el número de componentes conexas que hay en la red, si no está desconectada lo que 
    nos va a regresar va a ser 1
    
    momentos: Está función recibe una red y un parámetro n, lo que hace es calcular el n-ésimo momento (que depende del parámetro n que 
    pasemos) a partir de la distribución de grados.
    
    indice_robustez: El índice de robustez es un valor que nos regresa un valor que indica que tan "robusta" es la red con respecto
    a la medida de robustes que le pasemos. Estás medidas de robustes son caracterizadas por la propía red, puede ser el grado promedio
    la densidad, el número de componentes conexas, etc. En general todas estás anteriormente mencionadas son básicas dentro de la redes
    y nos indican de cierta forma que tan conectada está la red aún, pero son en general medidas a posteriori, es decir, que nos indican
    el estado de la red más no lo predicen; queremos verificar si ocurre lo mismo al definir la entropia en una red y al utilizarla en
    estos indices de robustez.
    Esta función recibe la red G, una función f, un peso w (que por lo general será 1 o la entropía antes de recibir ataques/fallos), 
    criterio de ataque, y un parámetro k que nos indica hasta donde vamos a atacar la red. 
    
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

def densidad(G,N):#Aquí N es el número inicial de nodos, no podemos tomar el len(G) porque puede ser que ya hayamos atacado la red
    numero_aristas = G.number_of_edges()
    return (2*numero_aristas)/(N*(N-1)) if len(G) !=0 else 0


def obtener_distribucion_grados(G): #Con está función recibimos una red y devolvemos la distribución de grados de la red
        N = len(G)
                
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
    return sum(dict(grados).values())/len(G) if len(G) > 0 else 0.0

def componentes_conexas(G):
    componentes_conexas = list(nx.connected_components(G))
    return len(componentes_conexas)

def LCC(G,criterio,N):  ## 1: es para medir el LCC con los nodos iniciales en la red, 2: es para medir el LCC con los nodos que restan en la red
    if criterio == 1:
        N=N
    elif criterio == 2:
        N=len(G)
    if N == 0:
        return 0
    componente_mas_grande = max(nx.connected_components(G), key=len)
    proporcion = len(componente_mas_grande)/N
    return proporcion

def momentos(G,n): # con está función vamos a obtener el n-ésimo momento de la red G (de su distribución de grados)
    N = len(G)
    distribucion_grados = obtener_distribucion_grados(G)
    return (sum(np.power(k,n) * probabilidad * N for k,probabilidad in distribucion_grados))/N if N > 0 else 0

    
def indice_robustez(G,f,w,criterio,k): 
    #G es la red
    #f es la medida de robustez que estamos usando
    #w string criterio
    #criterio es el criterio sobre el cuál estamos atacando la red 
    #k es el parámetro que nos dice el número de nodos que vamos a atacar, en general: k <= N 
    N = len(G)
    f_inicial = f(G)
    #Para calcular el indice de robustez de.-m  f, 
    #necesitamos realizar hasta k ataques, en esté caso hasta k ataques
    #y calcular en cada ataque la f(i) y w_i que en general va a ser constante
    critico = 0
    f_i = []
    for i in range(k):
        G = ataques(G,criterio)
        f_G = f(G)
        f_i.append(f_G)                
        if f_G == 0: #El crítico es el i en dónde la función de robustez se hace 0 y por tanto también el índice de robustez
            critico = i
            break
            
    if w == 1:
        w_i = 1/N
    elif w == 2:
        w_i = 1/max(f_i)
    elif w==3:
        w_i=1
    indice_robustez = (sum(w_i*f for f in f_i))/k
    
    return indice_robustez
        

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
    

