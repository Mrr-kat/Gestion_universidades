from pydantic import BaseModel, EmailStr
from typing import List, Optional

# Esquemas para Estudiantes
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
