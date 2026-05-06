# 🎓 CRUD de Estudiantes — FastAPI + MySQL

Aplicación web para gestionar el registro de alumnos de asesorías académicas. Permite crear, visualizar, editar y eliminar estudiantes desde una interfaz web sencilla.

---

## 🛠️ Tecnologías

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)
![Jinja2](https://img.shields.io/badge/Jinja2-Templates-red)

---

## ⚙️ Funcionalidades

- ✅ Registrar un nuevo alumno (nombre, edad, correo, tema de asesoría)
- ✅ Listar todos los alumnos registrados
- ✅ Editar los datos de un alumno
- ✅ Eliminar un alumno del sistema

---

## 📂 Estructura del proyecto

crud_estudiantes/

├── database.py        # Conexión a MySQL

├── main.py            # Rutas y lógica principal (FastAPI)

├── templates/         # Vistas HTML con Jinja2

├── requirements.txt   # Dependencias

├── test_db.py         # Prueba de conexión a la base de datos

└── .env               # Variables de entorno (no incluido en el repo)

---

## 🚀 Cómo ejecutar el proyecto

**1. Clona el repositorio**
```bash
git clone https://github.com/alfavinyl/crud_estudiantes.git
cd crud_estudiantes
```

**2. Instala las dependencias**
```bash
pip install -r requirements.txt
```

**3. Crea tu archivo `.env`** con tus credenciales de MySQL:

DB_HOST=localhost

DB_USER=tu_usuario

DB_PASSWORD=tu_contraseña

DB_NAME=asesorias

**4. Crea la tabla en MySQL**
```sql
CREATE DATABASE asesorias;
USE asesorias;

CREATE TABLE alumnos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    edad INT,
    correo VARCHAR(100),
    tema VARCHAR(100),
    ciudad VARCHAR(100)
);
```

**5. Levanta el servidor**
```bash
uvicorn main:app --reload
```

**6. Abre en tu navegador**

http://localhost:8000/usuarios

---

## 👤 Autor

**Fernando Teodoro Gabino**
[LinkedIn](https://www.linkedin.com/in/fernandoteodorogabino/) • [GitHub](https://github.com/alfavinyl)
