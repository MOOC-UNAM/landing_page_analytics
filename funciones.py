from get_sheet_content import lista_columna
import itertools

def titulos_matriculas(texto, matricula):
    cont_pa = len(texto.split())
    freq = cont_pa / matricula
    return freq

titulos = lista_columna(0)

matricula = lista_columna(6)


for t, m in zip(titulos, matricula):
    m = float(m)
    print(titulos_matriculas(t, m))
