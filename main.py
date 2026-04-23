# ===== IMPORTACIONES (IMPORTS) =====
# Los imports son como "traer herramientas" que necesitamos de bibliotecas externas
# Es como ir a una ferretería y comprar las herramientas que necesitas para construir algo

from fastapi import FastAPI, Request, Form
# FastAPI: Es el framework (marco de trabajo) principal que usamos para crear nuestra API web
#          Es como el "motor" de nuestra aplicación web
# Request: Nos permite acceder a la información de las peticiones HTTP que llegan al servidor
#          Por ejemplo, saber qué página está pidiendo el usuario, qué datos envió, etc.
# Form: Nos permite recibir datos de formularios HTML (como cuando llenas un registro con nombre, email, etc.)
#       Captura lo que el usuario escribe en los campos de un formulario

from fastapi.responses import HTMLResponse
# HTMLResponse: Nos permite enviar páginas HTML como respuesta al navegador del usuario
#               Es decir, le dice al navegador "aquí está tu página web en formato HTML"

from fastapi.templating import Jinja2Templates
# Jinja2Templates: Es un sistema de plantillas que nos permite crear páginas HTML dinámicas
#                  Imagina que tienes una plantilla de carta, y solo cambias el nombre del destinatario
#                  Jinja2 hace lo mismo pero con páginas web: tienes una plantilla y cambias los datos

from fastapi.responses import RedirectResponse
# RedirectResponse: Nos permite redirigir al usuario a otra página
#                   Es como cuando terminas de hacer algo y te mandan automáticamente a otra pantalla
#                   Ejemplo: después de crear un usuario, te redirige a la lista de usuarios

from database import get_connection
# get_connection: Esta es una función que TÚ creaste en otro archivo llamado "database.py"
#                 Esta función se encarga de conectarse a tu base de datos
#                 Es como tener una llave para abrir la puerta de tu base de datos


# ===== CONFIGURACIÓN DE LA APLICACIÓN =====

app = FastAPI()
# Aquí estamos CREANDO nuestra aplicación web
# "app" es el nombre que le damos a nuestra aplicación (puedes llamarla como quieras, pero "app" es común)
# Los paréntesis () significan que estamos "ejecutando" o "iniciando" FastAPI
# Es como encender el motor de un carro

templates = Jinja2Templates(directory="templates")
# Aquí le decimos a nuestra aplicación DÓNDE están las plantillas HTML
# "templates" es el nombre de la carpeta donde guardas tus archivos .html
# Jinja2Templates buscará en esa carpeta cada vez que quieras mostrar una página
# Es como decirle a tu programa: "Las páginas HTML están en esta carpeta llamada 'templates'"


#----------------------------------------------------------------------#
# MOSTRAR FORMULARIO (GET)
# Esta sección se encarga de MOSTRAR la página del formulario cuando alguien la visita


@app.get("/form", response_class=HTMLResponse)
# @app.get: Este es un DECORADOR (se identifica por el símbolo @)
#           Los decoradores son como "etiquetas" que le dicen a tu función qué hacer
#           @app.get específicamente significa: "cuando alguien VISITE esta ruta, ejecuta esta función"
#           
# "/form": Esta es la RUTA o URL que el usuario visitará en su navegador
#          Por ejemplo: http://localhost:8000/form
#          Es como la dirección de una casa, pero en tu aplicación web
#
# response_class=HTMLResponse: Le dice a FastAPI que esta función va a devolver HTML
#                              Es decir, una página web completa, no solo texto o datos


def mostrar_formulario(request: Request):
# def: Palabra clave de Python para DEFINIR (crear) una función
# mostrar_formulario: Es el NOMBRE que le damos a nuestra función (puedes ponerle el nombre que quieras)
# request: Request: Es un PARÁMETRO que recibe información sobre la petición del usuario
#                   Request (con mayúscula) indica el TIPO de dato que esperamos
#                   Jinja2Templates necesita este "request" para funcionar correctamente

    return templates.TemplateResponse(
        "form.html",
        {"request": request}
    )
    # return: Significa "devolver" o "regresar" algo como respuesta
    #
    # templates.TemplateResponse: Le dice a Jinja2 "busca y muestra esta plantilla HTML"
    #                             Recuerda que "templates" lo definimos al inicio
    #
    # "form.html": Es el NOMBRE del archivo HTML que queremos mostrar
    #              Este archivo debe estar en la carpeta "templates"
    #              Es la página del formulario que verá el usuario
    #
    # {"request": request}: Es un DICCIONARIO (se identifica por las llaves {})
    #                       Le pasamos el "request" a la plantilla HTML
    #                       Jinja2 necesita esto obligatoriamente para funcionar
    #                       Es como darle contexto a la página sobre quién la está visitando


# ===== RESUMEN DE ESTA SECCIÓN =====
# Cuando un usuario visita http://tuservidor.com/form
# FastAPI ejecuta esta función y le muestra la página "form.html"
# Es la primera parte del CRUD: mostrar la interfaz para CREAR (Create) algo



#----------------------------------------------------------------------#
# ENDPOINT CREAR USUARIO (POST)
# Esta sección GUARDA un nuevo usuario en la base de datos cuando se envía el formulario


@app.post("/guardar")
# @app.post: Es un DECORADOR similar a @app.get, pero para ENVIAR datos
#            .get = OBTENER/VER información (leer)
#            .post = ENVIAR/GUARDAR información (crear/modificar)
#            Cuando el usuario llena el formulario y presiona "Guardar", se usa POST
#
# "/guardar": Es la RUTA donde se enviarán los datos del formulario
#             El formulario HTML debe tener: action="/guardar" method="POST"
#             Es como la dirección de destino donde llegan los datos


def guardar_usuario(
    nombre: str = Form(...),
    edad: int = Form(...),
    correo: str = Form(...),
    tema: str = Form(...)
):
# def guardar_usuario: NOMBRE de la función que guardará al usuario
#
# nombre: str = Form(...): Recibe el campo "nombre" del formulario
#     - nombre: es el NOMBRE del parámetro (debe coincidir con el name="" en tu HTML)
#     - str: significa que esperamos un STRING (texto)
#     - Form(...): le dice a FastAPI "este dato viene de un formulario HTML"
#     - (...): los tres puntos significan que este campo es OBLIGATORIO
#
# edad: int = Form(...): Recibe el campo "edad" del formulario
#     - int: significa que esperamos un INTEGER (número entero)
#     - Todo lo demás funciona igual que "nombre"


    # ===== PASO 1: CONECTARSE A LA BASE DE DATOS =====
    conn = get_connection()
    # conn: Es la CONEXIÓN a tu base de datos (como abrir la puerta)
    # get_connection(): Llama a la función que creaste en database.py
    #                   Esta función devuelve una conexión activa a MySQL/PostgreSQL/etc.
    
    cursor = conn.cursor()
    # cursor: Es como un "apuntador" o "puntero" que te permite ejecutar comandos SQL
    #         Imagina que es un lápiz para escribir en la base de datos
    #         Sin el cursor, no puedes hacer consultas SQL


    # ===== PASO 2: PREPARAR LA CONSULTA SQL =====
    sql = "INSERT INTO alumnos (nombre, edad, correo, tema) VALUES (%s, %s, %s, %s)"
    # sql: Variable que guarda nuestro comando SQL
    # INSERT INTO: Comando SQL para INSERTAR (agregar) un nuevo registro
    # usuarios: Nombre de la TABLA en tu base de datos donde guardarás los datos
    # (nombre, edad): Las COLUMNAS de la tabla donde insertarás datos
    # VALUES (%s, %s): Los VALORES que insertarás
    #                  %s son "marcadores de posición" (placeholders)
    #                  Es una forma SEGURA de insertar datos (previene inyección SQL)
    #                  Cada %s será reemplazado por un valor real
    
    valores = (nombre, edad, correo, tema)
    # valores: Es una TUPLA (lista inmutable) con los datos reales
    #          El primer valor (nombre) reemplazará el primer %s
    #          El segundo valor (edad) reemplazará el segundo %s
    #          IMPORTANTE: el orden debe coincidir con los %s en la consulta SQL


    # ===== PASO 3: EJECUTAR LA CONSULTA =====
    cursor.execute(sql, valores)
    # cursor.execute(): EJECUTA el comando SQL en la base de datos
    # sql: La consulta que preparamos
    # valores: Los datos que se insertarán (reemplazan los %s)
    # En este momento se INSERTA el nuevo usuario en la tabla
    
    conn.commit()
    # commit(): CONFIRMA los cambios en la base de datos
    #           Es como presionar "Guardar" en un documento
    #           Sin commit(), los cambios NO se guardan permanentemente
    #           Es un mecanismo de seguridad para evitar guardar datos por accidente


    # ===== PASO 4: CERRAR LA CONEXIÓN =====
    cursor.close()
    # Cierra el cursor (el "lápiz" que usamos para escribir SQL)
    # Es buena práctica cerrar lo que abrimos para liberar recursos
    
    conn.close()
    # Cierra la conexión a la base de datos (cierra la "puerta")
    # Libera memoria y recursos del servidor
    # Si no cierras conexiones, puedes quedarte sin conexiones disponibles


    # ===== PASO 5: REDIRIGIR AL USUARIO =====
    return RedirectResponse(
            url="/usuarios",
            status_code = 303)
    # RedirectResponse: REDIRIGE al usuario a otra página
    #                   Es como decirle "ahora ve a esta otra dirección"
    #
    # url="/usuarios": La ruta a la que será redirigido
    #                  Probablemente es la página que muestra la lista de usuarios
    #                  Así el usuario puede ver que su nuevo usuario fue creado
    #
    # status_code=303: Es un código HTTP que indica "redirección después de POST"
    #                  303 = "See Other" (mira en otro lugar)
    #                  Es el código correcto para redirigir después de crear algo
    #                  Evita que el usuario recargue la página y cree usuarios duplicados


# ===== RESUMEN DE ESTA SECCIÓN (FLUJO COMPLETO) =====
# 1. Usuario llena el formulario con nombre y edad
# 2. Presiona el botón "Guardar"
# 3. Los datos se envían a "/guardar" usando método POST
# 4. Esta función recibe los datos
# 5. Se conecta a la base de datos
# 6. Inserta el nuevo usuario con INSERT INTO
# 7. Confirma los cambios con commit()
# 8. Cierra las conexiones
# 9. Redirige al usuario a "/usuarios" para ver la lista actualizada
# ¡Esto es la "C" de CRUD = CREATE (Crear)!


#----------------------------------------------------------------------#
# ENDPOINT OBTENER USUARIOS (READ)
# Esta sección MUESTRA la lista de todos los usuarios que están en la base de datos


@app.get("/usuarios")
# @app.get: Decorador para cuando alguien VISITA esta ruta (método GET = ver/leer)
# "/usuarios": La URL que el usuario visitará
#              Por ejemplo: http://localhost:8000/usuarios
#              Esta es la página que muestra la lista de todos los usuarios


def mostrar_usuarios(request : Request):
# def mostrar_usuarios: NOMBRE de la función que mostrará la lista de usuarios
# request: Request: Recibe información sobre la petición del usuario
#                   Necesario para que Jinja2Templates funcione correctamente


    try:
    # try: Inicia un bloque de código que puede tener ERRORES
    #      Si algo sale mal dentro de este bloque, Python no se "rompe"
    #      En su lugar, salta al bloque "except" y maneja el error
    #      Es como decir: "INTENTA hacer esto, y si falla, tengo un plan B"
    
    
        # ===== PASO 1: CONECTARSE A LA BASE DE DATOS =====
        conn = get_connection()
        # conn: Conexión a la base de datos (abre la "puerta")
        
        cursor = conn.cursor(dictionary = True)
        # cursor: El "apuntador" para ejecutar comandos SQL
        #
        # dictionary=True: ¡MUY IMPORTANTE! 
        #                  Hace que los resultados se devuelvan como DICCIONARIOS
        #                  Sin esto: [('Juan', 25), ('María', 30)] (solo valores)
        #                  Con esto: [{'nombre': 'Juan', 'edad': 25}, {'nombre': 'María', 'edad': 30}]
        #                  Los diccionarios son más fáciles de usar en las plantillas HTML
        #                  Puedes acceder a los datos como: usuario['nombre']
        
        
        # ===== PASO 2: EJECUTAR LA CONSULTA SQL =====
        cursor.execute("SELECT id, nombre, edad, correo, tema FROM alumnos")
        # cursor.execute(): EJECUTA el comando SQL
        #
        # "SELECT id, nombre, edad FROM usuarios": La consulta SQL
        #     - SELECT: Comando para SELECCIONAR (obtener) datos
        #     - id, nombre, edad: Las COLUMNAS que queremos obtener de la tabla
        #     - FROM usuarios: De qué TABLA queremos los datos
        #     - Esta consulta dice: "Dame el id, nombre y edad de TODOS los usuarios"
        #     - No hay WHERE, así que trae TODOS los registros de la tabla
        
        
        # ===== PASO 3: OBTENER LOS RESULTADOS =====
        usuarios = cursor.fetchall()
        # usuarios: Variable que guardará la LISTA de todos los usuarios
        #
        # fetchall(): "Trae TODOS los resultados" de la consulta
        #             fetch = traer, all = todos
        #             Devuelve una LISTA de diccionarios (gracias a dictionary=True)
        #             Ejemplo: [
        #                 {'id': 1, 'nombre': 'Juan', 'edad': 25},
        #                 {'id': 2, 'nombre': 'María', 'edad': 30},
        #                 {'id': 3, 'nombre': 'Pedro', 'edad': 22}
        #             ]
        #
        # Alternativas que NO usamos aquí:
        #     - fetchone(): Trae solo UN resultado (el primero)
        #     - fetchmany(5): Trae una cantidad específica de resultados
        
        
        # ===== PASO 4: CERRAR LAS CONEXIONES =====
        cursor.close()
        # Cierra el cursor (libera recursos)
        
        conn.close()
        # Cierra la conexión a la base de datos
        # Siempre debes cerrar lo que abres
        
        
        # ===== PASO 5: MOSTRAR LA PÁGINA HTML =====
        return templates.TemplateResponse(
            "usuarios.html",{
                "request" : request,
                "usuarios" : usuarios
                }
        )
        # templates.TemplateResponse: Renderiza (muestra) una plantilla HTML
        #
        # "usuarios.html": El archivo HTML que se mostrará
        #                  Debe estar en la carpeta "templates"
        #                  Esta página mostrará la lista de usuarios
        #
        # { ... }: Un DICCIONARIO con los datos que enviaremos a la plantilla HTML
        #
        # "request": request: Obligatorio para Jinja2Templates
        #                     Le da contexto a la plantilla
        #
        # "usuarios": usuarios: Enviamos la LISTA de usuarios al HTML
        #                       En el HTML podrás hacer un loop: {% for usuario in usuarios %}
        #                       Y acceder a cada dato: {{ usuario.nombre }}, {{ usuario.edad }}
        #                       La clave "usuarios" es el nombre que usarás en el HTML
        #                       El valor usuarios es la lista que obtuvimos de la BD
        
        
    except Exception as e:
    # except: Se ejecuta SOLO si hubo un ERROR en el bloque try
    #         Es el "plan B" si algo sale mal
    #
    # Exception as e: Captura CUALQUIER tipo de error que ocurra
    #                 Exception: es la clase general de todos los errores
    #                 as e: guarda el error en una variable llamada "e"
    #                       para poder ver qué fue lo que falló
    
        return {"error" : str(e)}
        # Si hay un error, devuelve un DICCIONARIO con información del error
        # {"error": ...}: Formato JSON que muestra el error
        # str(e): Convierte el error a TEXTO legible
        #         Por ejemplo: "Error: No se pudo conectar a la base de datos"
        #
        # Esto es útil para debugging (encontrar errores)
        # En producción (cuando tu app esté en internet), deberías mostrar
        # un mensaje más amigable al usuario, no el error técnico


# ===== RESUMEN DE ESTA SECCIÓN (FLUJO COMPLETO) =====
# 1. Usuario visita http://tuservidor.com/usuarios
# 2. La función se ejecuta y se conecta a la base de datos
# 3. Hace una consulta SELECT para obtener todos los usuarios
# 4. Trae TODOS los resultados con fetchall()
# 5. Cierra las conexiones
# 6. Envía los datos a la plantilla "usuarios.html"
# 7. La plantilla HTML muestra una tabla o lista con todos los usuarios
# 8. Si algo falla, muestra un mensaje de error
# ¡Esto es la "R" de CRUD = READ (Leer/Obtener)!



#----------------------------------------------------------------------#
# ENDPOINT EDITAR USUARIO (UPDATE)
# Esta sección tiene DOS partes:
# 1. MOSTRAR el formulario de edición con los datos actuales del usuario (GET)
# 2. GUARDAR los cambios cuando el usuario modifica los datos (POST)


# ========== PARTE 1: MOSTRAR FORMULARIO DE EDICIÓN (GET) ==========

@app.get("/usuarios/editar/{id}", response_class=HTMLResponse)
# @app.get: Decorador para MOSTRAR/VER la página de edición
#
# "/usuarios/editar/{id}": La RUTA con un parámetro dinámico
#     - {id}: Es un PARÁMETRO DE RUTA (path parameter)
#             Las llaves {} indican que es un valor variable
#             Por ejemplo: /usuarios/editar/5 (edita el usuario con id=5)
#                         /usuarios/editar/12 (edita el usuario con id=12)
#             El número que pongas en la URL se captura automáticamente
#
# response_class=HTMLResponse: Indica que devolveremos una página HTML


def editar_usuario_form(request: Request, id: int):
# def editar_usuario_form: NOMBRE de la función que muestra el formulario de edición
#
# request: Request: Para que Jinja2Templates funcione
#
# id: int: Recibe el ID del usuario que queremos editar
#          Este valor viene de la URL (el {id} que pusimos arriba)
#          int: indica que esperamos un número entero
#          FastAPI automáticamente convierte el valor de la URL a número


    try:
    # try: Intenta ejecutar el código, si falla, salta al except
    
    
        # ===== PASO 1: CONECTARSE A LA BASE DE DATOS =====
        conn = get_connection()
        # Abre la conexión a la base de datos
        
        cursor = conn.cursor(dictionary=True)
        # Crea el cursor con dictionary=True para obtener resultados como diccionarios


        # ===== PASO 2: BUSCAR EL USUARIO ESPECÍFICO =====
        sql = "SELECT id, nombre, edad, correo, tema FROM alumnos WHERE id = %s"
        # sql: La consulta SQL para buscar UN usuario específico
        #
        # SELECT id, nombre, edad: Las columnas que queremos obtener
        # FROM usuarios: De la tabla usuarios
        # WHERE id = %s: Condición que filtra por ID
        #                WHERE = "donde" (condición)
        #                id = %s: "donde el id sea igual a este valor"
        #                %s: marcador de posición para el valor del id
        #                Esta condición hace que solo traiga UN usuario
        
        cursor.execute(sql, (id,))
        # cursor.execute(): Ejecuta la consulta SQL
        # sql: La consulta que preparamos
        # (id,): Una TUPLA con el valor del id
        #        La coma después de id es IMPORTANTE: (id,)
        #        Sin la coma, Python no lo reconoce como tupla
        #        Este valor reemplaza el %s en la consulta
        #        Si id=5, la consulta se convierte en: "SELECT ... WHERE id = 5"
        
        usuario = cursor.fetchone()
        # usuario: Variable que guarda el resultado
        #
        # fetchone(): Trae SOLO UN resultado (una fila)
        #             Como buscamos por ID (que es único), solo hay un usuario
        #             Resultado: {'id': 5, 'nombre': 'Juan', 'edad': 25}
        #             Si no encuentra el usuario, devuelve None


        # ===== PASO 3: CERRAR CONEXIONES =====
        cursor.close()
        conn.close()
        # Siempre cerrar lo que abrimos


        # ===== PASO 4: MOSTRAR EL FORMULARIO DE EDICIÓN =====
        return templates.TemplateResponse(
            "editar.html",
            {
                "request": request,
                "usuario": usuario
            }
        )
        # templates.TemplateResponse: Muestra la plantilla HTML
        #
        # "editar.html": Archivo HTML con el formulario de edición
        #                Este formulario estará PRE-LLENADO con los datos actuales
        #
        # "request": request: Obligatorio para Jinja2
        #
        # "usuario": usuario: Enviamos los datos del usuario al HTML
        #                     En el HTML podrás poner:
        #                     <input value="{{ usuario.nombre }}"> (pre-llena el campo)
        #                     <input value="{{ usuario.edad }}">
        #                     Así el usuario ve sus datos actuales y puede modificarlos


    except Exception as e:
    # Si hay algún error (usuario no existe, problema de BD, etc.)
        return {"error": str(e)}
        # Devuelve el error en formato JSON




# ========== PARTE 2: GUARDAR LOS CAMBIOS (POST) ==========

@app.post("/usuarios/editar/{id}")
# @app.post: Decorador para ENVIAR/GUARDAR datos (método POST)
# "/usuarios/editar/{id}": La misma ruta, pero ahora para GUARDAR cambios
#                          El formulario enviará los datos a esta ruta
#                          {id}: También captura el ID del usuario a editar


def editar_usuario(
    id: int,
    nombre: str = Form(...),
    edad: int = Form(...),
    correo: str = Form(...),
    tema: str = Form(...)
):
# def editar_usuario: NOMBRE de la función que GUARDA las modificaciones
#
# id: int: El ID del usuario (viene de la URL)
#          Necesario para saber QUÉ usuario estamos actualizando
#
# nombre: str = Form(...): Recibe el nuevo nombre del formulario
# edad: int = Form(...): Recibe la nueva edad del formulario
#                        Estos son los valores MODIFICADOS por el usuario


    try:
    # Intenta ejecutar el código de actualización
    
    
        # ===== PASO 1: CONECTARSE A LA BASE DE DATOS =====
        conn = get_connection()
        cursor = conn.cursor()
        # Nota: Aquí NO usamos dictionary=True porque NO necesitamos leer datos
        #       Solo vamos a ACTUALIZAR, no a obtener resultados


        # ===== PASO 2: PREPARAR LA CONSULTA DE ACTUALIZACIÓN =====
        sql = """
            UPDATE alumnos
            SET nombre = %s, edad = %s, correo = %s, tema = %s 
            WHERE id = %s
        """
        # sql: La consulta SQL para ACTUALIZAR (modificar) datos
        #
        # """: Comillas triples permiten escribir texto en múltiples líneas
        #      Hace el código más legible
        #
        # UPDATE usuarios: Comando SQL para ACTUALIZAR la tabla usuarios
        #
        # SET nombre = %s, edad = %s: Establece los nuevos valores
        #     SET = "establecer" (asignar nuevos valores)
        #     nombre = %s: "cambia el nombre por este nuevo valor"
        #     edad = %s: "cambia la edad por este nuevo valor"
        #
        # WHERE id = %s: Condición MUY IMPORTANTE
        #                "actualiza SOLO el registro donde el id sea este"
        #                Sin WHERE, ¡actualizarías TODOS los usuarios!
        #                Es como decir: "de todos los usuarios, solo modifica este"
        
        cursor.execute(sql, (nombre, edad, correo, tema, id))
        # cursor.execute(): Ejecuta la consulta SQL
        # sql: La consulta de actualización
        # (nombre, edad, id): TUPLA con los valores en el ORDEN correcto
        #                     - nombre reemplaza el primer %s (SET nombre = %s)
        #                     - edad reemplaza el segundo %s (SET edad = %s)
        #                     - id reemplaza el tercer %s (WHERE id = %s)
        #                     El ORDEN es crucial, debe coincidir con los %s
        
        conn.commit()
        # commit(): CONFIRMA y GUARDA los cambios en la base de datos
        #           Sin esto, los cambios NO se guardan permanentemente
        #           Es como presionar "Guardar" después de editar un documento


        # ===== PASO 3: CERRAR CONEXIONES =====
        cursor.close()
        conn.close()
        # Liberamos recursos


        # ===== PASO 4: REDIRIGIR AL USUARIO =====
        return RedirectResponse(
            url="/usuarios",
            status_code=303
        )
        # RedirectResponse: Redirige al usuario a otra página
        # url="/usuarios": Lo enviamos a la lista de usuarios
        #                  Para que vea que sus cambios se guardaron
        # status_code=303: Código HTTP para redirección después de POST
        #                  Evita que el usuario recargue y envíe el formulario otra vez


    except Exception as e:
    # Si hay algún error al actualizar
        return {"error": str(e)}
        # Devuelve el error


# ===== RESUMEN DE ESTA SECCIÓN (FLUJO COMPLETO) =====
# PARTE 1 (GET):
# 1. Usuario hace clic en "Editar" en un usuario específico
# 2. Se abre /usuarios/editar/5 (por ejemplo, para el usuario con id=5)
# 3. La función busca ese usuario en la base de datos
# 4. Muestra un formulario PRE-LLENADO con los datos actuales
# 
# PARTE 2 (POST):
# 5. Usuario modifica los datos y presiona "Guardar"
# 6. Los nuevos datos se envían por POST a /usuarios/editar/5
# 7. Se ejecuta el UPDATE en la base de datos
# 8. Se confirman los cambios con commit()
# 9. Se redirige a /usuarios para ver la lista actualizada
# ¡Esto es la "U" de CRUD = UPDATE (Actualizar)!



#----------------------------------------------------------------------#
# ENDPOINT ELIMINAR USUARIO (DELETE)
# Esta sección ELIMINA (borra) un usuario de la base de datos


@app.post("/eliminar/usuario/{id}")
# @app.post: Decorador para método POST
#            ¿Por qué POST y no DELETE?
#            Porque los formularios HTML solo soportan GET y POST
#            Aunque estamos eliminando, usamos POST para que funcione desde un formulario
#            En APIs REST puras se usaría @app.delete, pero aquí usamos POST por compatibilidad
#
# "/eliminar/usuario/{id}": La RUTA para eliminar
#     - {id}: Parámetro dinámico que captura el ID del usuario a eliminar
#             Ejemplo: /eliminar/usuario/5 elimina al usuario con id=5
#                     /eliminar/usuario/12 elimina al usuario con id=12


def eliminar_usuario(id : int):
# def eliminar_usuario: NOMBRE de la función que eliminará al usuario
#
# id: int: Recibe el ID del usuario que queremos eliminar
#          Este valor viene de la URL (el {id} de la ruta)
#          int: indica que esperamos un número entero
#
# NOTA: Esta función NO recibe "request" ni "Form(...)"
#       Porque NO necesitamos mostrar ninguna página HTML
#       Solo necesitamos el ID para saber qué usuario eliminar


    try:
    # try: Intenta ejecutar el código, si falla, maneja el error en except
    
    
        # ===== PASO 1: CONECTARSE A LA BASE DE DATOS =====
        conn = get_connection()
        # Abre la conexión a la base de datos
        
        cursor = conn.cursor()
        # Crea el cursor para ejecutar comandos SQL
        # NO usamos dictionary=True porque no vamos a LEER datos
        # Solo vamos a ELIMINAR


        # ===== PASO 2: PREPARAR LA CONSULTA DE ELIMINACIÓN =====
        sql = "DELETE FROM alumnos WHERE id = %s"
        # sql: La consulta SQL para ELIMINAR un registro
        #
        # DELETE FROM usuarios: Comando SQL para ELIMINAR de la tabla usuarios
        #                       DELETE = "borrar/eliminar"
        #                       FROM usuarios = "de la tabla usuarios"
        #
        # WHERE id = %s: Condición CRÍTICA para eliminar solo UN usuario
        #                "elimina SOLO donde el id sea igual a este valor"
        #                %s: marcador de posición para el valor del id
        #
        # ⚠️ ADVERTENCIA IMPORTANTE ⚠️
        # Si NO pones WHERE, eliminarás TODOS los usuarios de la tabla
        # WHERE es tu "seguro de vida" para no borrar todo por accidente
        # Siempre, SIEMPRE usa WHERE al hacer DELETE
        
        cursor.execute(sql, (id,))
        # cursor.execute(): Ejecuta la consulta SQL
        # sql: La consulta de eliminación que preparamos
        # (id,): TUPLA con el valor del id
        #        La coma después de id es importante: (id,)
        #        Este valor reemplaza el %s en la consulta
        #        Si id=5, la consulta se convierte en: "DELETE FROM usuarios WHERE id = 5"
        #        Esto eliminará SOLO al usuario con id=5
        
        conn.commit()
        # commit(): CONFIRMA la eliminación en la base de datos
        #           Sin esto, el usuario NO se eliminará permanentemente
        #           Es como confirmar "Sí, estoy seguro de borrar esto"
        #           Una vez hecho commit(), ya NO hay vuelta atrás
        #           El usuario se elimina de forma permanente


        # ===== PASO 3: CERRAR CONEXIONES =====
        cursor.close()
        # Cierra el cursor (libera el "apuntador")
        
        conn.close()
        # Cierra la conexión a la base de datos
        # Libera recursos del servidor


        # ===== PASO 4: REDIRIGIR AL USUARIO =====
        return RedirectResponse(
            url="/usuarios",
            status_code = 303)
        # RedirectResponse: Redirige automáticamente a otra página
        #
        # url="/usuarios": Envía al usuario a la lista de usuarios
        #                  Para que vea que el usuario fue eliminado
        #                  La lista se verá actualizada sin el usuario eliminado
        #
        # status_code=303: Código HTTP "See Other" (mira en otro lugar)
        #                  Es el código correcto para redirigir después de un POST
        #                  Evita que si el usuario recarga la página, vuelva a eliminar
        
        
    except Exception as e:
    # except: Se ejecuta SI hubo algún ERROR
    #         Por ejemplo:
    #         - El usuario con ese ID no existe
    #         - Problemas de conexión a la base de datos
    #         - El usuario tiene relaciones con otras tablas (claves foráneas)
    
        return {"error" : str(e)}
        # Devuelve un diccionario JSON con el mensaje de error
        # str(e): Convierte el error a texto legible
        # Ejemplo: {"error": "Cannot delete: foreign key constraint fails"}
        #
        # En una aplicación real, deberías mostrar un mensaje más amigable
        # Como: "No se pudo eliminar el usuario. Intenta de nuevo."


# ===== RESUMEN DE ESTA SECCIÓN (FLUJO COMPLETO) =====
# 1. Usuario ve la lista de usuarios en /usuarios
# 2. Hace clic en el botón "Eliminar" junto a un usuario específico
# 3. Se envía una petición POST a /eliminar/usuario/5 (por ejemplo)
# 4. Esta función recibe el id=5
# 5. Se conecta a la base de datos
# 6. Ejecuta DELETE para eliminar SOLO ese usuario (gracias al WHERE id = 5)
# 7. Confirma la eliminación con commit() (ya no hay vuelta atrás)
# 8. Cierra las conexiones
# 9. Redirige a /usuarios para ver la lista actualizada sin ese usuario
# 10. Si algo falla, muestra el error
# ¡Esto es la "D" de CRUD = DELETE (Eliminar)!

# ===== ¡FELICIDADES! =====
# Con este código ya tienes un CRUD COMPLETO:
# ✅ C = CREATE (Crear usuario) → /guardar
# ✅ R = READ (Leer/Ver usuarios) → /usuarios
# ✅ U = UPDATE (Actualizar usuario) → /usuarios/editar/{id}
# ✅ D = DELETE (Eliminar usuario) → /eliminar/usuario/{id}