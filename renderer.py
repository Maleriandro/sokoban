import gamelib as gl
import soko

IMG_SUELO = "src/ground.gif"
IMG_CAJA = "src/box.gif"
IMG_PARED = "src/wall.gif"
IMG_OBJETIVO = "src/goal.gif"
IMG_JUGADOR = {
    (0,1) : "src/player_s.gif",
    (0,-1) : "src/player_n.gif",
    (1,0) : "src/player_e.gif",
    (-1,0) : "src/player_o.gif"
    }


TAMANIO_CASILLA = 64    # Este tamaño debe coincidir con el tamaño de las texturas
                        # para que el juego se renderice de forma correcta

def cambiar_tamanio_ventana(grilla):
    '''Recibe un nivel en forma de grilla (lista de listas) y ajusta el tamaño de la ventana,
    acorde a las dimensiones del nivel. Devuelve el tamaño de la ventana en pixeles (x, y)'''
    x, y = soko.dimensiones(grilla)

    x *= TAMANIO_CASILLA
    y *= TAMANIO_CASILLA


    gl.resize(x, y)

    return x,y


def nivel(grilla, accion = None):
    '''Recibe un nivel en forma de grilla (lista de listas), y dibuja en la ventana
    la representacion de esa grilla.
    '''


    tamanio_x, tamanio_y = soko.dimensiones(grilla)

    for x in range(tamanio_x):
        for y in range(tamanio_y):

            px_x = (x * TAMANIO_CASILLA) + 2  # Lo desplazo 2 pixeles, porque es lo que ocupan
            px_y = (y * TAMANIO_CASILLA) + 2  # los bordes de la ventana.

            gl.draw_image(IMG_SUELO, px_x, px_y)


            if soko.hay_jugador(grilla, x, y):
                gl.draw_image(IMG_JUGADOR.get(accion, "src/player_s.gif"), px_x, px_y)

            elif soko.hay_caja(grilla, x, y):
                gl.draw_image(IMG_CAJA, px_x, px_y)

            elif soko.hay_pared(grilla, x, y):
                gl.draw_image(IMG_PARED, px_x, px_y)
            
            if soko.hay_objetivo(grilla, x, y):
                gl.draw_image(IMG_OBJETIVO, px_x, px_y)


def titulo(title, tamanio):
    '''Recibe un string, y un array o lista con el tamaño de la ventana actual. Dibuja en pantalla el titulo pasado por parametro.
    '''

    x,y = tamanio

    x /= 2
    y /= 2

    gl.draw_begin()
    
    gl.draw_text(title, x, y, 30)

    gl.draw_end()


def final(tamanio, tiempo):
    '''Recibe un array o lista con el tamaño de la ventana actual, y un string.
    Dibuja en pantalla el mensaje final para mostrar al jugador, junto con el tiempo que se pase como parametro
    '''

    x = tamanio[0]/2
    y = tamanio[1]/2

    gl.draw_begin()

    gl.draw_text("Felicidades!\nPasaste todos los niveles disponibles.", x, y+20, justify= "center")
    gl.draw_text("GAME OVER", x, y-50, 40)
    gl.draw_text(str(tiempo), x, y+90)
    gl.draw_text("Presiona una tecla para salir del juego", x, (y*2)-15, 7)

    gl.draw_end()

def error_archivo(archivo):
    '''Recibe como parametro un string. Muestra en pantalla un error de archivo'''

    gl.resize(500,300)

    error= "Hubo un error con el archivo: " + archivo + "\nSi modificó el archivo, regrese a su archivo original.\nSi no lo modificó, reinstale el juego."

    gl.draw_begin()

    gl.draw_text(error, 250, 150, justify= "center", fill = "red")
    gl.draw_text("Presiona una tecla para salir del juego", 250, 285, 7)

    gl.draw_end()

def error_backtracking():
    '''Muestra en pantalla que el backtracing no pudo realizarse'''

    gl.resize(500,300)

    error= "No se pudo resolver el nivel."

    gl.draw_begin()

    gl.draw_text(error, 250, 150, justify= "center", fill = "red")
    gl.draw_text("Presiona una tecla para continuar", 250, 285, 7)

    gl.draw_end()

def pensando_solucion(nivel_actual):
    '''Muestra en pantalla que el backtracing se esta realizando'''
    gl.draw_begin()

    nivel(nivel_actual)

    gl.draw_text('Pensando una solucion', 10, 20, fill = 'white', anchor = 'w')

    gl.draw_end()





            

    
