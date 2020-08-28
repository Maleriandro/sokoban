from data_structures import Pila
import soko

DIRECCIONES = ((0,1),(0,-1),(1,0),(-1,0))

class Backtracking:
    '''Modulo que realiza una busqueda de posibles soluciones para un nivel.''' 
    def __init__(self):
        '''Inicializa el modulo, sin buscar solucion.'''
        self.acciones_solucion = Pila()
        self.solucion_disponible = False

    def generar_solucion(self, estado_inicial):
        '''Recibe un estado inicial de un nivel, y busca una posible solucion a este nivel, y almacena los movimientos requeridosa para esta solucion.
        Si no encuentra solucion, lanza un error'''
        self.acciones_solucion = Pila()
        visitados = {}
        self.solucion_disponible = self._backtrack(estado_inicial, visitados)
        if not self.solucion_disponible:
            raise Exception('El algoritmo no encontró una solucion al puzzle')

    def _backtrack(self, estado, visitados):
        '''Busca los movimientos disponibles para el estado del juego. Devuelve si es posible realizar el movimiento,
        y almacena los movimientos requeridos para llegar a ese estado valido.'''
        visitados[str(estado)] = estado

        if soko.juego_ganado(estado):
            return True

        for direccion in DIRECCIONES:
            nuevo_estado = soko.mover(estado, direccion)

            if str(nuevo_estado) in visitados:
                continue

            solucion_encontrada = self._backtrack(nuevo_estado, visitados)
            if solucion_encontrada:
                
                self.acciones_solucion.apilar(direccion)

                return True

        return False

    def obtener_mov(self):
        '''Devuelve el proximo movimiento a realizar para llegar a la solucion encontrada por la funcion generar_solucion(),
        y lo elimina de los movimientos a realizar. Si no hay ningun movimiento para realizar, devuelve un error.'''
        if self.acciones_solucion.esta_vacia():
            raise Exception('No hay ningun movimiento disponible para llegar a una solucion')

        return self.acciones_solucion.desapilar()
