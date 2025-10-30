from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from modelos import Estudiante, Curso, estudiante_curso
from esquemas import EstudianteCrear, CursoCrear, EstudianteActualizar, CursoActualizar
from fastapi import HTTPException, status

# CRUD para Estudiantes
def crear_estudiante(bd: Session, estudiante: EstudianteCrear):
    # Verificar si la cédula ya existe
    estudiante_bd = bd.query(Estudiante).filter(Estudiante.cedula == estudiante.cedula).first()
    if estudiante_bd:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cédula ya registrada"
        )
    
    estudiante_bd = Estudiante(
        cedula=estudiante.cedula,
        nombre=estudiante.nombre,
        email=estudiante.email,
        semestre=estudiante.semestre
    )
    bd.add(estudiante_bd)
    bd.commit()
    bd.refresh(estudiante_bd)
    return estudiante_bd

def obtener_estudiantes(bd: Session, semestre: int = None):
    consulta = bd.query(Estudiante)
    if semestre:
        consulta = consulta.filter(Estudiante.semestre == semestre)
    return consulta.all()

def obtener_estudiante(bd: Session, estudiante_id: int):
    estudiante = bd.query(Estudiante).filter(Estudiante.id == estudiante_id).first()
    if not estudiante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudiante no encontrado"
        )
    return estudiante

def obtener_estudiante_con_cursos(bd: Session, estudiante_id: int):
    estudiante = bd.query(Estudiante).filter(Estudiante.id == estudiante_id).first()
    if not estudiante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudiante no encontrado"
        )
    return estudiante

def actualizar_estudiante(bd: Session, estudiante_id: int, estudiante_actualizar: EstudianteActualizar):
    estudiante_bd = obtener_estudiante(bd, estudiante_id)
    
    datos_actualizar = estudiante_actualizar.dict(exclude_unset=True)
    for campo, valor in datos_actualizar.items():
        setattr(estudiante_bd, campo, valor)
    
    bd.commit()
    bd.refresh(estudiante_bd)
    return estudiante_bd

def eliminar_estudiante(bd: Session, estudiante_id: int):
    estudiante_bd = obtener_estudiante(bd, estudiante_id)
    
    # Eliminar matrículas del estudiante (cascada manual)
    bd.execute(
        estudiante_curso.delete().where(estudiante_curso.c.estudiante_id == estudiante_id)
    )
    
    bd.delete(estudiante_bd)
    bd.commit()
    return {"mensaje": "Estudiante eliminado correctamente"}

# CRUD para Cursos
def crear_curso(bd: Session, curso: CursoCrear):
    # Verificar si el código ya existe
    curso_bd = bd.query(Curso).filter(Curso.codigo == curso.codigo).first()
    if curso_bd:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Código de curso ya registrado"
        )
    
    curso_bd = Curso(
        codigo=curso.codigo,
        nombre=curso.nombre,
        creditos=curso.creditos,
        horario=curso.horario
    )
    bd.add(curso_bd)
    bd.commit()
    bd.refresh(curso_bd)
    return curso_bd

def obtener_cursos_creditos_codigo(bd: Session, creditos: int = None, codigo: str = None):
    consulta = bd.query(Curso)
    if creditos:
        consulta = consulta.filter(Curso.creditos == creditos)
    if codigo:
        consulta = consulta.filter(Curso.codigo.ilike(f"%{codigo}%"))
    return consulta.all()

def obtener_curso_id(bd: Session, curso_id: int):
    curso = bd.query(Curso).filter(Curso.id == curso_id).first()
    if not curso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso no encontrado"
        )
    return curso

def obtener_curso_con_estudiantes(bd: Session, curso_id: int):
    curso = bd.query(Curso).filter(Curso.id == curso_id).first()
    if not curso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso no encontrado"
        )
    return curso

def actualizar_curso(bd: Session, curso_id: int, curso_actualizar: CursoActualizar):
    curso_bd = obtener_curso_id(bd, curso_id)
    
    datos_actualizar = curso_actualizar.dict(exclude_unset=True)
    for campo, valor in datos_actualizar.items():
        setattr(curso_bd, campo, valor)
    
    bd.commit()
    bd.refresh(curso_bd)
    return curso_bd

def eliminar_curso(bd: Session, curso_id: int):
    curso_bd = obtener_curso_id(bd, curso_id)
    
    # Eliminar matrículas del curso
    bd.execute(
        estudiante_curso.delete().where(estudiante_curso.c.curso_id == curso_id)
    )
    
    bd.delete(curso_bd)
    bd.commit()
    return {"mensaje": "Curso eliminado correctamente"}

# Gestión de Matrículas
def matricular_estudiante(bd: Session, estudiante_id: int, curso_id: int):
    # Verificar que el estudiante y curso existen
    estudiante = obtener_estudiante(bd, estudiante_id)
    curso = obtener_curso_id(bd, curso_id)
    
    # Verificar si ya está matriculado
    matricula_existente = bd.execute(
        estudiante_curso.select().where(
            (estudiante_curso.c.estudiante_id == estudiante_id) & 
            (estudiante_curso.c.curso_id == curso_id)
        )
    ).first()
    
    if matricula_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El estudiante ya está matriculado en este curso"
        )
    
    # Verificar conflictos de horario
    cursos_estudiante = obtener_cursos_estudiante(bd, estudiante_id)
    horario_curso_actual = curso.horario
    
    for curso_matriculado in cursos_estudiante:
        if curso_matriculado.horario == horario_curso_actual:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El estudiante ya tiene un curso en este horario"
            )
    
    # Realizar la matrícula
    bd.execute(
        estudiante_curso.insert().values(
            estudiante_id=estudiante_id,
            curso_id=curso_id
        )
    )
    bd.commit()
    return {"mensaje": "Estudiante matriculado correctamente"}

def desmatricular_estudiante(bd: Session, estudiante_id: int, curso_id: int):
    # Verificar que la matrícula existe
    matricula = bd.execute(
        estudiante_curso.select().where(
            (estudiante_curso.c.estudiante_id == estudiante_id) & 
            (estudiante_curso.c.curso_id == curso_id)
        )
    ).first()
    
    if not matricula:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El estudiante no está matriculado en este curso"
        )
    
    # Eliminar la matrícula
    bd.execute(
        estudiante_curso.delete().where(
            (estudiante_curso.c.estudiante_id == estudiante_id) & 
            (estudiante_curso.c.curso_id == curso_id)
        )
    )
    bd.commit()
    return {"mensaje": "Estudiante desmatriculado correctamente"}

def obtener_cursos_estudiante(bd: Session, estudiante_id: int):
    estudiante = obtener_estudiante_con_cursos(bd, estudiante_id)
    return estudiante.cursos

def obtener_estudiantes_curso(bd: Session, curso_id: int):
    curso = obtener_curso_con_estudiantes(bd, curso_id)
    return curso.estudiantes