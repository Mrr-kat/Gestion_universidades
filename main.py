from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from DB import obtener_bd, motor
from modelos import Base
from esquemas import (
    Estudiante, EstudianteCrear, EstudianteActualizar
)
import crud

# Crear tablas
Base.metadata.create_all(bind=motor)

app = FastAPI()

# Endpoints para Estudiantes
@app.post("/estudiantes/", response_model=Estudiante, status_code=status.HTTP_201_CREATED)
def crear_estudiante(estudiante: EstudianteCrear, bd: Session = Depends(obtener_bd)):
    return crud.crear_estudiante(bd=bd, estudiante=estudiante)

@app.get("/estudiantes/", response_model=List[Estudiante])
def leer_estudiantes(semestre: Optional[int] = None, bd: Session = Depends(obtener_bd)):
    return crud.obtener_estudiantes(bd=bd, semestre=semestre)

@app.put("/estudiantes/{estudiante_id}", response_model=Estudiante)
def actualizar_estudiante(estudiante_id: int, estudiante: EstudianteActualizar, bd: Session = Depends(obtener_bd)):
    return crud.actualizar_estudiante(bd=bd, estudiante_id=estudiante_id, estudiante_actualizar=estudiante)

@app.delete("/estudiantes/{estudiante_id}")
def eliminar_estudiante(estudiante_id: int, bd: Session = Depends(obtener_bd)):
    return crud.eliminar_estudiante(bd=bd, estudiante_id=estudiante_id)

@app.get("/")
def leer_raiz():
    return {"mensaje": "Sistema de Gestión Universitaria"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)