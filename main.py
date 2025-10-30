from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional

from DB import obtener_bd, motor
from modelos import Base
from esquemas import Estudiante, EstudianteCrear, EstudianteActualizar,Curso, CursoCrear, CursoActualizar, CursoConEstudiantes, Matricula

import crud

# Crear tablas
Base.metadata.create_all(bind=motor)

app = FastAPI(title="Sistema de Gestión Universitaria")

# Crear estudiante
@app.post("/estudiantes/", response_model=Estudiante, status_code=status.HTTP_201_CREATED)
def crear_estudiante(estudiante: EstudianteCrear, bd: Session = Depends(obtener_bd)):
    return crud.crear_estudiante(bd=bd, estudiante=estudiante)

# Listar estudiantes (con filtro opcional por semestre)
@app.get("/estudiantes/", response_model=List[Estudiante])
def leer_estudiantes(semestre: Optional[int] = None, bd: Session = Depends(obtener_bd)):
    return crud.obtener_estudiantes(bd=bd, semestre=semestre)

# Actualizar estudiante
@app.put("/estudiantes/{estudiante_id}", response_model=Estudiante)
def actualizar_estudiante(estudiante_id: int, estudiante: EstudianteActualizar, bd: Session = Depends(obtener_bd)):
    return crud.actualizar_estudiante(bd=bd, estudiante_id=estudiante_id, estudiante_actualizar=estudiante)

# Eliminar estudiante
@app.delete("/estudiantes/{estudiante_id}")
def eliminar_estudiante(estudiante_id: int, bd: Session = Depends(obtener_bd)):
    return crud.eliminar_estudiante(bd=bd, estudiante_id=estudiante_id)

# Endpoints para Cursos
@app.post("/cursos/", response_model=Curso, status_code=status.HTTP_201_CREATED)
def crear_curso(curso: CursoCrear, bd: Session = Depends(obtener_bd)):
    return crud.crear_curso(bd=bd, curso=curso)

@app.get("/cursos/", response_model=List[Curso])
def leer_cursos(
    creditos: Optional[int] = None, 
    codigo: Optional[str] = None, 
    bd: Session = Depends(obtener_bd)
):
    return crud.obtener_cursos_creditos_codigo(bd=bd, creditos=creditos, codigo=codigo)

@app.get("/cursos/{curso_id}", response_model=CursoConEstudiantes)
def leer_curso(curso_id: int, bd: Session = Depends(obtener_bd)):
   return crud.obtener_curso_con_estudiantes(bd=bd, curso_id=curso_id)


@app.put("/cursos/{curso_id}", response_model=Curso)
def actualizar_curso(curso_id: int, curso: CursoActualizar, bd: Session = Depends(obtener_bd)):
    return crud.actualizar_curso(bd=bd, curso_id=curso_id, curso_actualizar=curso)

@app.delete("/cursos/{curso_id}")
def eliminar_curso(curso_id: int, bd: Session = Depends(obtener_bd)):
    return crud.eliminar_curso(bd=bd, curso_id=curso_id)

# Endpoints para Matrículas
@app.post("/matricular/", status_code=status.HTTP_201_CREATED)
def matricular_estudiante(matricula: Matricula, bd: Session = Depends(obtener_bd)):
    return crud.matricular_estudiante(
        bd=bd, 
        estudiante_id=matricula.estudiante_id, 
        curso_id=matricula.curso_id
    )

@app.delete("/desmatricular/")
def desmatricular_estudiante(matricula: Matricula, bd: Session = Depends(obtener_bd)):
    return crud.desmatricular_estudiante(
        bd=bd, 
        estudiante_id=matricula.estudiante_id, 
        curso_id=matricula.curso_id
    )

@app.get("/estudiantes/{estudiante_id}/cursos", response_model=List[Curso])
def obtener_cursos_estudiante(estudiante_id: int, bd: Session = Depends(obtener_bd)):
    return crud.obtener_cursos_estudiante(bd=bd, estudiante_id=estudiante_id)

@app.get("/cursos/{curso_id}/estudiantes", response_model=List[Estudiante])
def obtener_estudiantes_curso(curso_id: int, bd: Session = Depends(obtener_bd)):
    return crud.obtener_estudiantes_curso(bd=bd, curso_id=curso_id)


# raíz
@app.get("/")
def leer_raiz():
    return {"mensaje": "Sistema de Gestión Universitaria activo"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
