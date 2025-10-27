from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional

from DB import obtener_bd, motor
from modelos import Base
from esquemas import Estudiante, EstudianteCrear, EstudianteActualizar
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

# raíz
@app.get("/")
def leer_raiz():
    return {"mensaje": "Sistema de Gestión Universitaria activo"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
