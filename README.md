
# Sistema de Gestión Universitaria

Aplicación web desarrollada con FastAPI y SQLAlchemy para gestionar estudiantes, cursos y matrículas en una universidad.

## Características principales

- CRUD completo para Estudiantes y Cursos  
- Relación muchos a muchos (N:M) entre Estudiantes y Cursos  
- Gestión de Matrículas  
- Logica de negocio:
  - Cédula única
  - Código de curso único
  - Evita matrícula doble en el mismo curso
  - Evita conflictos de horario entre cursos
- Eliminación en cascada manual, al eliminar estudiante o curso, se eliminan sus respectivas matrículas
- Filtros en consultas:
  - Estudiantes por semestre
  - Cursos por créditos o código

---

## Estructura del proyecto

proyecto_universidad

- main.py          
- crud.py         
- modelos.py       
- esquemas.py      
- DB.py            
- universidad.db   


---

## Instalación y ejecución

### 1️ Clonar el repositorio
git clone https://github.com/tuusuario/proyecto_universidad.git
cd proyecto_universidad


### 2️ Crear un entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate   # En Linux/Mac
venv\Scripts\activate      # En Windows


### 3️ Instalar dependencias

pip install -r requerimientos.txt


### 4️ Ejecutar la aplicación
uvicorn main:app --reload


### 5️⃣ Acceder al sistema

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Endpoints principales

| Método | Endpoint | Descripción |
|--------|-----------|-------------|
| **POST** | `/estudiantes/` | Crear estudiante |
| **GET** | `/estudiantes/` | Listar estudiantes (filtro: `semestre`) |
| **GET** | `/estudiantes/{id}/cursos` | Ver cursos matriculados |
| **PUT** | `/estudiantes/{id}` | Actualizar estudiante |
| **DELETE** | `/estudiantes/{id}` | Eliminar estudiante |
| **POST** | `/cursos/` | Crear curso |
| **GET** | `/cursos/` | Listar cursos (filtro: `creditos`, `codigo`) |
| **GET** | `/cursos/{id}/estudiantes` | Ver estudiantes inscritos |
| **PUT** | `/cursos/{id}` | Actualizar curso |
| **DELETE** | `/cursos/{id}` | Eliminar curso |
| **POST** | `/matricular/` | Matricular estudiante en curso |
| **DELETE** | `/desmatricular/` | Desmatricular estudiante de curso |

---

## Ejemplo de uso

1. Crear un estudiante:
```json
{
  "cedula": "123456789",
  "nombre": "Ana López",
  "email": "ana@example.com",
  "semestre": 3
}
```

2. Crear un curso:
```json
POST /cursos/
{
  "codigo": "CS101",
  "nombre": "Programación I",
  "creditos": 3,
  "horario": "Lunes 8-10"
}
```

3. Matricular estudiante:
```json
POST /matricular/
{
  "estudiante_id": 1,
  "curso_id": 1
}
```
