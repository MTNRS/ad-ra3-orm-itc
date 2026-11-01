"""Mapeo de las tablas SQLite creadas en C++ en RA2."""
from pathlib import Path
from sqlalchemy import create_engine, ForeignKey, String, select, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

class Base(DeclarativeBase):
    pass

class Cliente(Base):
    __tablename__ = 'clientes'
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    estado: Mapped[str] = mapped_column(String, nullable=False)
    proyectos: Mapped[list['Proyecto']] = relationship(back_populates='cliente')

class Proyecto(Base):
    __tablename__ = 'proyectos'
    id: Mapped[int] = mapped_column(primary_key=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey('clientes.id'))
    nombre: Mapped[str] = mapped_column(String)
    estado: Mapped[str] = mapped_column(String)
    cliente: Mapped[Cliente] = relationship(back_populates='proyectos')

def conectar(ruta):
    return create_engine('sqlite:///' + str(Path(ruta).resolve()))

def listar(engine):
    with Session(engine) as sesion:
        return [(c.id, c.nombre, c.email, len(c.proyectos)) for c in sesion.scalars(select(Cliente).order_by(Cliente.nombre))]

def alta(engine, nombre, email):
    with Session(engine) as sesion, sesion.begin():
        cliente = Cliente(nombre=nombre, email=email, estado='prospecto')
        cliente.proyectos.append(Proyecto(nombre='Estudio inicial', estado='pendiente'))
        sesion.add(cliente)

def resumen_sql(engine):
    with engine.connect() as conexion:
        return conexion.execute(text('SELECT estado, COUNT(*) FROM clientes GROUP BY estado')).all()
