# ===== IMPORTACIONES (IMPORTS) =====
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from database import get_connection


# ===== CONFIGURACIÓN =====
app = FastAPI()
templates = Jinja2Templates(directory="templates")


# ===== GET: MOSTRAR FORMULARIO =====
@app.get("/form", response_class=HTMLResponse)
def mostrar_formulario(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


# ===== POST: CREAR USUARIO =====
@app.post("/guardar")
def guardar_usuario(
    nombre: str = Form(...),
    edad: int = Form(...),
    correo: str = Form(...),
    tema: str = Form(...)
):
    conn = get_connection()
    cursor = conn.cursor()

    sql = "INSERT INTO alumnos (nombre, edad, correo, tema) VALUES (%s, %s, %s, %s)"
    valores = (nombre, edad, correo, tema)

    cursor.execute(sql, valores)
    conn.commit()

    cursor.close()
    conn.close()

    return RedirectResponse(url="/usuarios", status_code=303)


# ===== GET: OBTENER USUARIOS =====
@app.get("/usuarios")
def mostrar_usuarios(request: Request):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id, nombre, edad, correo, tema FROM alumnos")
        usuarios = cursor.fetchall()

        cursor.close()
        conn.close()

        return templates.TemplateResponse(
            "usuarios.html",
            {"request": request, "usuarios": usuarios}
        )
    except Exception as e:
        return {"error": str(e)}


# ===== GET: FORMULARIO EDITAR =====
@app.get("/usuarios/editar/{id}", response_class=HTMLResponse)
def editar_usuario_form(request: Request, id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = "SELECT id, nombre, edad, correo, tema FROM alumnos WHERE id = %s"
        cursor.execute(sql, (id,))
        usuario = cursor.fetchone()

        cursor.close()
        conn.close()

        return templates.TemplateResponse(
            "editar.html",
            {"request": request, "usuario": usuario}
        )
    except Exception as e:
        return {"error": str(e)}


# ===== POST: EDITAR USUARIO =====
@app.post("/usuarios/editar/{id}")
def editar_usuario(
    id: int,
    nombre: str = Form(...),
    edad: int = Form(...),
    correo: str = Form(...),
    tema: str = Form(...)
):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            UPDATE alumnos
            SET nombre = %s, edad = %s, correo = %s, tema = %s
            WHERE id = %s
        """

        cursor.execute(sql, (nombre, edad, correo, tema, id))
        conn.commit()

        cursor.close()
        conn.close()

        return RedirectResponse(url="/usuarios", status_code=303)
    except Exception as e:
        return {"error": str(e)}


# ===== POST: ELIMINAR USUARIO =====
@app.post("/eliminar/usuario/{id}")
def eliminar_usuario(id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = "DELETE FROM alumnos WHERE id = %s"
        cursor.execute(sql, (id,))
        conn.commit()

        cursor.close()
        conn.close()

        return RedirectResponse(url="/usuarios", status_code=303)
    except Exception as e:
        return {"error": str(e)}