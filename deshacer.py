from data_structures import Pila

class Deshacer:
    '''Almacena historial de estados en forma de pila. Se puede agregar estados, sacar estados, comprobar si hay estados disponibles para deshacer, y vaciar el historial.'''
    def __init__(self):
        '''Inicializa historial de estados vacio'''
        self.acciones = Pila()


    def agregar_estado(self, estado):
        '''Agrega el estado del nivel al historial de acciones. Si el estado enviado es el mismo que el anterior, no hace nada'''
        if self.acciones.esta_vacia() or not self.acciones.ver_tope() == estado:       
            self.acciones.apilar(estado)


    def deshacer_movimiento(self):
        '''pre: El historial de movimientos debe tener por lo menos 1 elemento
        Devuelve el ultimo estado almacenado.'''
        if self.acciones.esta_vacia():
            raise ValueError('No Existe ningun valor que deshacer')

        return self.acciones.desapilar()


    def se_puede_deshacer(self):
        '''Devuelve si se se puede deshacer al estado anterior.'''
        return not self.acciones.esta_vacia()


    def vaciar(self):
        '''Vacia el historial de estados'''
        self.acciones = Pila()

