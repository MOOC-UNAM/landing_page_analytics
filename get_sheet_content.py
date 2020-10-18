from mooc_unam_spreadsheet import validador


ID_HOJADECALCULO = '1dsW2kClGh3E73EhuybthLeTkIoFzscjAr_uXbbrZ1tA'
RANGO = 'Descargas!A2:F104'


def lista_columna(columna):
    '''
    número de la columna de la que se quieren obtener datos.
    [0] Nombre del curso
    [1] slug
    [2] Tipo de datos
    [3] Request date
    [4] Status
    [5] Size (KB)
    '''
    lista = []

    try:
        datostabla = validador(ID_HOJADECALCULO, RANGO)
        for row in datostabla:
            lista.append('%s' % (row[columna]))
    except:
        print("no hay datos")

    return lista
