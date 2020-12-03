from mooc_unam_spreadsheet import validador


ID_HOJADECALCULO = '1dsW2kClGh3E73EhuybthLeTkIoFzscjAr_uXbbrZ1tA'
RANGO = 'Descargas!A2:G104'


def lista_columna(columna):
    '''
    número de la columna de la que se quieren obtener datos.
    [0] Nombre del curso
    [1] slug
    [2] Tipo de datos
    [3] Request date
    [4] Status
    [5] Size (KB)
    [6] Enrollment
    [7] Fecha lanzamiento
    [8] Número de semanas
    [9] Número de módulos
    [10] Número de videos
    [11] Minutos de video
    [12] Cantidad de in-video quizzes
    [13] Minutos de instrucción
    [14] Matrícula (09/2020)
    [15] Matrícula (10/2020) == [6] Enrollment
    [16] Estudiantes activos
    [17] Eficiencia terminal
    [18] Estrellas (promedio)
    [19] Última actualización
    '''
    lista = []

    try:
        datostabla = validador(ID_HOJADECALCULO, RANGO)
        for row in datostabla:
            lista.append('%s' % (row[columna]))
    except:
        print("no hay datos")

    return lista
