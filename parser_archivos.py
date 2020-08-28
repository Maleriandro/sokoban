ACCIONES = {
    "NORTE": (0,-1),
    "SUR": (0,1),
    "ESTE": (1,0),
    "OESTE": (-1,0)
}

def lista_niveles(archivo_niveles):
    '''Recibe la ruta a un archivo .txt que contenga los nombres, y grillas de los niveles del juego,
    con un formato igual al presentado por el archivo de niveles original. Devuelve una lista de dicc,
    con cada diccionario teniendo el titulo, y matriz del nivel, con el formato:
    {"title": "", "grilla": []}
    '''

    with open(archivo_niveles) as niveles_archivo:
        nivel = {"title" : "", "grilla": []}
        niveles = [] 
        for linea in niveles_archivo: 
            
            linea = linea.rstrip()


            if linea.startswith("Level"):
                nivel["title"] += linea


            elif linea.startswith("'"):
                titulo = "\n" + linea[1:-1]
                
                nivel["title"] += titulo

            elif linea:
                nivel["grilla"].append(linea)
            else:
                niveles.append(nivel)

                nivel = {"title" : "", "grilla": []}
        

    if nivel["grilla"]:         # Si detecta que al salir del loop, el nivel no esta vacío,
        niveles.append(nivel)   # quiere decir que fue el ultimo nivel y el loop no detectó
                                # el final del nivel para poder agregarlo

    for nivel in niveles:
        columnas = len(max(nivel['grilla'], key=len))

        for fila in range(len(nivel["grilla"])):

                    nivel["grilla"][fila] = nivel["grilla"][fila].ljust(columnas)        

    
    return niveles


def dict_controles(archivo_controles):
    '''Recibe la ruta a un archivo .txt que contenga los controles del juego con un formato igual al presentado por el
    archivo de controles original.
    Devuelve un diccionario con las claves siendo las teclas, y el valor siendo la tupla que describe el movimiento,
    o el string que representa la accion.
    '''
    
    controles = {}
    with open(archivo_controles) as controles_archivo:

        for linea in controles_archivo:

            if not "=" in linea:
                continue
            
            tecla, accion_temp = linea.split("=")

            tecla = tecla.strip()
            accion_temp = accion_temp.strip()
         
            controles[tecla] = ACCIONES.get(accion_temp, accion_temp)   

    return controles
            


            