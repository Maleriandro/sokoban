# Estados de cada "bloque"
VACIO = " "
PARED = "#"
CAJA = "$"
JUGADOR = "@" 
OBJ = "."
OBJ_CAJA = "*"
OBJ_JUGADOR = "+"


def crear_grilla(desc):
    '''Crea una grilla a partir de la descripción del estado inicial.

    La descripción es una lista de cadenas, cada cadena representa una
    fila y cada caracter una celda. Los caracteres pueden ser los siguientes:

    Caracter  Contenido de la celda
    --------  ---------------------
           #  Pared
           $  Caja
           @  Jugador
           .  Objetivo
           *  Objetivo + Caja
           +  Objetivo + Jugador

    Ejemplo:

    >>> crear_grilla([
        '#####',
        '#.$ #',
        '#@  #',
        '#####',
    ])
    '''
  

    grilla = []

    for i in desc:
        grilla.append(list(i))
        
    # Esta manera tiene la desventaja de que cuando referencio algún elemento de
    # la grilla, tengo que referenciarlo como [y][x], por el orden en el que esta,
    # pero me da la ventaja de poder trabajar, en casi todos los casos directamente 
    # con el parametro grilla, sin tener que "formatearlo" con mi funcion crear_grilla()

    return grilla
    
    
def dimensiones(grilla):
    '''Devuelve una tupla con la cantidad de columnas y filas de la grilla.'''
    filas = len(grilla)
    columnas = len(grilla[0])
    return (columnas, filas)
    

# A partir de acá, empiezo a usar como coordenadas de cada bloque de la grilla, los
# ejes cartesianos que me son mas intuitivos que pensar en filas y columnas.

def hay_pared(grilla, x, y):
    '''Devuelve True si hay una pared en la columna y fila (x, y).'''
    return grilla[y][x] == PARED


def hay_objetivo(grilla, x, y):
    '''Devuelve True si hay un objetivo en la columna y fila (x, y).'''
    return grilla[y][x] in (OBJ, OBJ_CAJA, OBJ_JUGADOR)


def hay_caja(grilla, x, y):
    '''Devuelve True si hay una caja en la columna y fila (x, y).'''
    return grilla[y][x] in (CAJA, OBJ_CAJA)


def hay_jugador(grilla, x, y):
    '''Devuelve True si el jugador está en la columna y fila (x, y).'''
    return grilla[y][x] in (JUGADOR, OBJ_JUGADOR)


def que_hay(grilla, x, y):
    '''Devuelve el objeto colisionable o VACIO que hay en la columna y fila, (x, y)'''


    pos = (grilla, x, y)

    if hay_pared(*pos):
        return PARED

    elif hay_jugador(*pos):
        return JUGADOR

    elif hay_caja(*pos):
        return CAJA

    else:
        return VACIO


def obtener_siguiente_posicion(x, y, direccion):
    '''Devuelve la coordenada siguiente a las pasadas por parametro, avanzando segun la direccion'''
    next_x = x + direccion[0]
    next_y = y + direccion[1]

    return [next_x, next_y]


def juego_ganado(grilla):
    '''Devuelve True si el juego está ganado.'''
    for f in grilla:   # Verifico que exista alguna caja, lo que significa
        if CAJA in f:  # que hay por lo menos 1 caja que no esta en el objetivo.
            return False 
        
    return True


def mover(grilla, direccion):
    '''Mueve el jugador en la dirección indicada.

    La dirección es una tupla con el movimiento horizontal y vertical. Dado que
    no se permite el movimiento diagonal, la dirección puede ser una de cuatro
    posibilidades:

    direccion  significado
    ---------  -----------
    (-1, 0)    Oeste
    (1, 0)     Este
    (0, -1)    Norte
    (0, 1)     Sur

    La función debe devolver una grilla representando el estado siguiente al
    movimiento efectuado. La grilla recibida NO se modifica; es decir, en caso
    de que el movimiento sea válido, la función devuelve una nueva grilla.
    '''

    x_jugador, y_jugador = obtener_posicion_jugador(grilla)                      # Busco el x,y de la posicion
    x_next, y_next = obtener_siguiente_posicion(x_jugador, y_jugador, direccion) # del jugador, de su posicion
    x_next2, y_next2 = obtener_siguiente_posicion(x_next, y_next, direccion)     # siguiente, y su subsiguiente.


    siguiente = que_hay(grilla, x_next, y_next)


    if siguiente == PARED:
        new_grilla = crear_grilla(grilla)  #crear_grilla(grilla)

    elif siguiente == VACIO:
        new_grilla = mover_objeto(grilla, x_jugador, y_jugador, direccion)

    elif siguiente == CAJA:
        siguiente2 = que_hay(grilla, x_next2, y_next2)  
        # Ejecuto recien en esta linea, para que no intente acceder a una parte fuera del estado (fuera del mapa)
        # si el jugador esta en un borde e intenta moverse hacia éste. Como hay una caja, me aseguro de que como
        # mínimo hay una pared de por medio. 

        if siguiente2 == CAJA or siguiente2 == PARED:
            new_grilla = crear_grilla(grilla)  # crear_grilla(grilla)

        else:
            temporal_grilla = mover_objeto(grilla, x_next, y_next, direccion)
            # Muevo primero el bloque, así no lo reescribo con el personaje,
            # para no tener que crear una nueva instancia del bloque.
            new_grilla = mover_objeto(temporal_grilla, x_jugador, y_jugador, direccion) 
        
    return new_grilla


def obtener_posicion_jugador(grilla):
    '''Devuelve la posicion del jugador en x, y'''
    for y in range(len(grilla)):                        # Paso por cada posicion del mapa hasta que
                                                        # que en una encuentro al jugador y devuelvo
        for x in range(len(grilla[0])):                 # esas coordenadas.

            if grilla[y][x] in (JUGADOR, OBJ_JUGADOR): 
                return x,y

    
def mover_objeto(grilla, x, y, direccion):
    '''Devuelve una grilla, con el objeto en x,y movido hacia la direccion indicada,
    y rellena con vacío u objetivo el lugar que ocupaba anteriormente'''

    grilla_new = crear_grilla(grilla)  # crear_grilla(grilla)
    objeto_movido = grilla_new[y][x]

    next_x, next_y = obtener_siguiente_posicion(x, y, direccion)

    # Toda esta parte es para saber si cuando muevo un objeto, tengo que poner el objeto solo
    # o el objeto que contiene un objetivo, y en el espacio que ocupaba antes, si tengo que poner
    # vacío, o un objetivo
    if hay_objetivo(grilla, x, y):
        if hay_objetivo(grilla, next_x, next_y): # Hay objetivo en el inicial y siguiente
            grilla_new[y][x] = OBJ
            grilla_new[next_y][next_x] = objeto_movido

        else:                                    # Hay objetivo en el inicial pero no en el siguiente
            grilla_new[y][x] = OBJ
            grilla_new[next_y][next_x] = invertir_objetivo_en_objeto(objeto_movido)

    else:
        if hay_objetivo(grilla, next_x, next_y): # No hay objetivo en el inicial pero si en el siguiente
            grilla_new[y][x] = VACIO
            grilla_new[next_y][next_x] = invertir_objetivo_en_objeto(objeto_movido)

        else:                                    # No hay objetivo en el inicial ni en el siguiente
            grilla_new[y][x] = VACIO
            grilla_new[next_y][next_x] = objeto_movido

    return grilla_new


def invertir_objetivo_en_objeto(objeto):   
    '''Devuelve el objeto pasado por parametro, eliminando, o agregando el
    el objetivo según si existe o no.'''
    

    if objeto == OBJ_CAJA:
        return CAJA

    elif objeto == CAJA:
        return OBJ_CAJA


    elif objeto == OBJ_JUGADOR:
        return JUGADOR

    elif objeto == JUGADOR:
        return OBJ_JUGADOR
