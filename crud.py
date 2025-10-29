from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from modelos import Estudiante, Curso, estudiante_curso
from esquemas import EstudianteCrear, CursoCrear, EstudianteActualizar, CursoActualizar
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
    
    bd.delete(estudiante_bd)
    bd.commit()
    return {"mensaje": "Estudiante eliminado correctamente"}


# CRUD para Cursos
def crear_curso(bd: Session, curso: CursoCrear):
    existente = bd.query(Curso).filter(Curso.codigo == curso.codigo).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Código de curso ya registrado"
        )
    
    nuevo = Curso(
        codigo=curso.codigo,
        nombre=curso.nombre,
        creditos=curso.creditos,
        horario=curso.horario
    )
    bd.add(nuevo)
    bd.commit()
    bd.refresh(nuevo)
    return nuevo

# obtener cursos creditos codigo
def obtener_cursos_creditos_codigo(bd: Session, creditos: int = None, codigo: str = None):
    consulta = bd.query(Curso)
    if creditos is not None:
        consulta = consulta.filter(Curso.creditos == creditos)
    if codigo:
        consulta = consulta.filter(Curso.codigo.ilike(f"%{codigo}%"))
    return consulta.all()

# obtener cursos con id
def obtener_curso_id(bd: Session, curso_id: int):
    curso = bd.query(Curso).filter(Curso.id == curso_id).first()
    if not curso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso no encontrado"
        )
    return curso

# actualizar cursos
def actualizar_curso(bd: Session, curso_id: int, curso_actualizar: CursoActualizar):
    curso_bd = obtener_curso_id(bd, curso_id)
    
    datos_actualizar = curso_actualizar.dict(exclude_unset=True)
    for campo, valor in datos_actualizar.items():
        setattr(curso_bd, campo, valor)
    
    bd.commit()
    bd.refresh(curso_bd)
    return curso_bd

# eliminar cursos
def eliminar_curso(bd: Session, curso_id: int):
    curso_bd = obtener_curso_id(bd, curso_id)
    bd.delete(curso_bd)
    bd.commit()
    return {"mensaje": "Curso eliminado correctamente"}

# relacion estudiantes

def obtener_cursos_estudiante(bd: Session, estudiante_id: int):
    estudiante = obtener_estudiante_id(bd, estudiante_id)
    return estudiante.cursos

def obtener_estudiantes_curso(bd: Session, curso_id: int):
    curso = obtener_curso_id(bd, curso_id)
    return curso.estudiantes