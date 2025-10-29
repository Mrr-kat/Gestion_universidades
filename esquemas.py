from pydantic import BaseModel, EmailStr
from typing import Optional, List


class EstudianteBase(BaseModel):
    cedula: str
    nombre: str
    email: EmailStr
    semestre: int

class EstudianteCrear(EstudianteBase):
    pass

class EstudianteActualizar(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    semestre: Optional[int] = None

class Estudiante(EstudianteBase):
    id: int
    class Config:
        from_attributes = True


class CursoBase(BaseModel):
    codigo: str
    nombre: str
    creditos: int
    horario: str

class CursoCrear(CursoBase):
    pass

class CursoActualizar(BaseModel):
    nombre: Optional[str] = None
    creditos: Optional[int] = None
    horario: Optional[str] = None

class Curso(CursoBase):
    id: int
    class Config:
        from_attributes = True


class CursoConEstudiantes(Curso):
    estudiantes: List[Estudiante] = []

class EstudianteConCursos(Estudiante):
    cursos: List[Curso] = []



CursoConEstudiantes.model_rebuild()
EstudianteConCursos.model_rebuild()
