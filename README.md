# Descripción

Este programa funciona conectándose a una tabla en Google Spreadsheets que contiene el listado de cursos ofrecidos por la UNAM a través de Coursera. El enlace a la tabla es el siguiente: https://docs.google.com/spreadsheets/d/1dsW2kClGh3E73EhuybthLeTkIoFzscjAr_uXbbrZ1tA/edit?usp=sharing (Se requiere autorización para abrir el enlace). El enlace está *hard-coded* en el archivo `get_sheet_content.py` en la variable `ID_HOJADECALCULO`.

El archivo `mooc_unam_spreadsheet.py` contiene la autorización para acceder a la tabla a través de Google API. Se requiere habilitar la Google Sheets API: https://developers.google.com/sheets/api/quickstart/python#step_1_turn_on_the 

Para asegurarse de tener las dependencias necesarias puede correr el archivo requirements.txt

`pip install -r requirements.txt`

El archivo `get_sheet_content.py` cotiene solamente una función que regresa el contenido específico de una columna desde la tabla de Google Spreadsheets. El parámetro de la función es un valor numérico que corresponde a cada columna de la tabla, así:

    [0] Nombre del curso
    [1] slug
    [2] Tipo de datos
    [3] Request date
    [4] Status
    [5] Size (KB)

El archivo `get_feedback.py` contiene las funciones y el script que explora cada página y regresa los comentarios de cada curso.

La información que recupera este script es:

- Calificación (estrellas) dadas por el comentarista al curso (1 a 5)
- Nombre del comentarista
- Fecha del comentario
- Texto del comentario
- Cantidad de veces que el comentario ha sido considerado útil.

Todo esto se guarda en un JSON array con la siguiente estructura:

```
[
    {
    "testimonio": "Texto del testimonio.",
    "nombre": "Nombre del comentarista",
    "mooc": "Título del curso",
    "url": "https://es.coursera.org/learn/slug-curso",
    "util": "número de me gusta",
    "estrellas": "número de estrellas",
    "fecha": "fecha del comentario",
    "url": "url del curso"
    }
]
```

Las tareas (TODO) pueden listarse a través de la librería `extract-todo`: https://pypi.org/project/extract-todo/

`extract-todo get_feedback.py`