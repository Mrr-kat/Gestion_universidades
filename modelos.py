from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Tabla intermedia estudiante-curso
estudiante_curso = Table(
    'estudiante_curso',
    Base.metadata,
    Column('estudiante_id', Integer, ForeignKey('estudiantes.id'), primary_key=True),
    Column('curso_id', Integer, ForeignKey('cursos.id'), primary_key=True)
)

class Estudiante(Base):
    __tablename__ = "estudiantes"
    
    id = Column(Integer, primary_key=True, index=True)
    cedula = Column(String, unique=True, index=True, nullable=False)
    nombre = Column(String, nullable=False)
    email = Column(String, nullable=False)
    semestre = Column(Integer, nullable=False)
    
    # Relación con cursos
    cursos = relationship("Curso", secondary=estudiante_curso, back_populates="estudiantes")

class Curso(Base):
    __tablename__ = "cursos"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, index=True, nullable=False)
    nombre = Column(String, nullable=False)
    creditos = Column(Integer, nullable=False)
    horario = Column(String, nullable=False)
    
    # Relación con estudiantes
    estudiantes = relationship("Estudiante", secondary=estudiante_curso, back_populates="cursos")