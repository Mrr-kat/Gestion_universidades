
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

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/tuusuario/proyecto_universidad.git
cd proyecto_universidad
```

### 2️⃣ Crear un entorno virtual (opcional pero recomendado)
```bash
python -m venv venv
source venv/bin/activate   # En Linux/Mac
venv\Scripts\activate      # En Windows
```

### 3️⃣ Instalar dependencias
```bash
pip install fastapi uvicorn sqlalchemy pydantic
```

### 4️⃣ Ejecutar la aplicación
```bash
uvicorn main:app --reload
```

### 5️⃣ Acceder al sistema
Abre tu navegador en:  
👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Allí verás la **documentación interactiva (Swagger UI)** generada automáticamente por FastAPI.

---

## 📚 Endpoints principales

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

## 🧠 Ejemplo de uso

1. Crear un estudiante:
```json
POST /estudiantes/
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

---

## 🧹 Notas

- La base de datos se genera automáticamente como `universidad.db`.
- Si la eliminas, se volverá a crear al ejecutar `main.py`.
- Usa `/docs` para probar los endpoints fácilmente.
