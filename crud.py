from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from modelos import Estudiante, estudiante_curso
from esquemas import EstudianteCrear, EstudianteActualizar
from fastapi import HTTPException, status

# Crear estudiante
def crear_estudiante(bd: Session, estudiante: EstudianteCrear):
    existente = bd.query(Estudiante).filter(Estudiante.cedula == estudiante.cedula).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cédula ya registrada"
        )
    
    nuevo = Estudiante(
        cedula=estudiante.cedula,
        nombre=estudiante.nombre,
        email=estudiante.email,
        semestre=estudiante.semestre
    )
    bd.add(nuevo)
    bd.commit()
    bd.refresh(nuevo)
    return nuevo

# Listar estudiantes (opcional: por semestre)
def obtener_estudiantes(bd: Session, semestre: int = None):
    consulta = bd.query(Estudiante)
    if semestre:
        consulta = consulta.filter(Estudiante.semestre == semestre)
    return consulta.all()

# Obtener estudiante por ID
def obtener_estudiante_id(bd: Session, estudiante_id: int):
    estudiante = bd.query(Estudiante).filter(Estudiante.id == estudiante_id).first()
    if not estudiante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudiante no encontrado"
        )
    return estudiante

# Obtener estudiante con cursos
def obtener_estudiante_con_cursos(bd: Session, estudiante_id: int):
    estudiante = obtener_estudiante_id(bd, estudiante_id)
    return estudiante

# Actualizar estudiante
def actualizar_estudiante(bd: Session, estudiante_id: int, estudiante_actualizar: EstudianteActualizar):
    estudiante_bd = obtener_estudiante_id(bd, estudiante_id)
    
    datos_actualizar = estudiante_actualizar.dict(exclude_unset=True)
    for campo, valor in datos_actualizar.items():
        setattr(estudiante_bd, campo, valor)
    
    bd.commit()
    bd.refresh(estudiante_bd)
    return estudiante_bd

# Eliminar estudiante
def eliminar_estudiante(bd: Session, estudiante_id: int):
    estudiante_bd = obtener_estudiante_id(bd, estudiante_id)
    
    # Eliminar matrículas del estudiante (cascada manual)
    bd.execute(
        estudiante_curso.delete().where(estudiante_curso.c.estudiante_id == estudiante_id)
    )
    
    bd.delete(estudiante_bd)
    bd.commit()
    return {"mensaje": "Estudiante eliminado correctamente"}
