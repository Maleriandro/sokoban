import time
import soko
import gamelib as gl
import renderer as render
import parser_archivos as parser
from deshacer import Deshacer
from pista import Backtracking

# Usado para controlar en que nivel empieza el juego.
PRIMER_NIVEL = 1

ARCHIVO_NIVELES = "src/niveles.txt"
ARCHIVO_CONTROLES = "src/teclas.txt"


def main():
    '''Inicializa el juego'''

    gl.title("Sokoban")


    try:
    # Genera la lista de niveles, con la matriz de objetos, y el nombre del nivel.
        niveles = parser.lista_niveles(ARCHIVO_NIVELES)
    except (IOError, FileNotFoundError):
        render.error_archivo(ARCHIVO_NIVELES)

        ev = gl.wait(gl.EventType.KeyPress)
        return

    try:
        # Genera el diccionario con las teclas, y la accion que generan esas teclas
        controles = parser.dict_controles(ARCHIVO_CONTROLES)
    except (IOError, FileNotFoundError):
        render.error_archivo(ARCHIVO_CONTROLES)

        ev = gl.wait(gl.EventType.KeyPress)
        return
    

    nivel_nro = PRIMER_NIVEL - 1

    # Empezar contador de tiempo para dar tiempo total luego de finalizados todos los niveles
    tiempo_inicial = time.time()
    

    # Itera por cada nivel
    while gl.is_alive():

        nivel = niveles[nivel_nro].copy()

        grilla = nivel["grilla"]
        titulo = nivel["title"]

        nivel_actual = soko.crear_grilla(grilla)  

        x,y = render.cambiar_tamanio_ventana(nivel_actual)

        render.titulo(titulo, (x,y))
        time.sleep(1)
        
        accion = (0,1)

        # Crea nuevas instancias, para que no genere errores cuando pase de nivel
        deshacer = Deshacer()
        backtraking = Backtracking()

        # Este ciclo solo espera al input del jugador
        while True:
            gl.draw_begin()

            render.nivel(nivel_actual, accion)

            gl.draw_end()

            ev = gl.wait(gl.EventType.KeyPress)
            if not ev:
                return


            tecla = ev.key

            if not tecla in controles:
                continue

            accion = controles[tecla]


            # Actualizar el estado del juego, según la `tecla` presionada
            if type(accion) == tuple:
                deshacer.agregar_estado(nivel_actual)
                backtraking.solucion_disponible = False
                nivel_actual = soko.mover(nivel_actual, accion)

            elif accion == "REINICIAR":
                deshacer.agregar_estado(nivel_actual)
                nivel_actual = soko.crear_grilla(grilla)
                backtraking.solucion_disponible = False
            
            elif accion == "PISTA":
                if not backtraking.solucion_disponible:
                    render.pensando_solucion(nivel_actual)
                    try:
                        backtraking.generar_solucion(nivel_actual)
                    except:
                        render.error_backtracking()
                        ev = gl.wait(gl.EventType.KeyPress)
                        render.cambiar_tamanio_ventana(nivel_actual)

                else:
                    deshacer.agregar_estado(nivel_actual)
                    accion = backtraking.obtener_mov()
                    nivel_actual = soko.mover(nivel_actual, accion)
                    
            elif accion == "DESHACER":
                if deshacer.se_puede_deshacer():
                    nivel_actual = deshacer.deshacer_movimiento()
                    backtraking.solucion_disponible = False
                else:
                    gl.play_sound('src/alert.wav')

            elif accion == "SALIR":
                return

            if soko.juego_ganado(nivel_actual):               
                break

        # Paso al siguiente nivel
        nivel_nro += 1

        # Verifica que haya terminado todos los niveles
        if nivel_nro >= len(niveles):

            tiempo_final = time.time()
            tiempo_total = tiempo_final - tiempo_inicial

            # Genera horas, minutos y segundos  
            tiempo = "Tiempo total " + convertir_segundos(tiempo_total)

            render.final((x,y), tiempo)

            ev = gl.wait(gl.EventType.KeyPress)

            return


def convertir_segundos(segundos):
    '''Recibe una cantidad de segundos (float), y devuelve la cantidad de horas, minutos, y segundos que representan en formato hh:mm:ss'''
    h = str(int(segundos // 3600))
    segundos %= 3600

    m = str(int(segundos // 60))
    segundos %= 60

    s = str(int(segundos))

    h,m,s = map(lambda num: num if len(num)>1 else "0"+num, [h,m,s])

    return f"{h}:{m}:{s}"
  


gl.init(main)
