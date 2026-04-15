# db.py - Base de datos SQLModel con 4 tablas
from sqlmodel import SQLModel, Field, create_engine, Session
from typing import Optional
from datetime import datetime, date
import json

# Tabla 1: Empresas
class Empresa(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    supabase_uid: str = Field(index=True, unique=True)  # UUID de Supabase
    nombre: str
    caja_total: float
    reserva_minima: float
    horizonte_dias: int  # 7, 30, 90, 180
    perfil_riesgo: str  # conservador, moderado, agresivo
    creado_en: datetime = Field(default_factory=datetime.now)
    actualizado_en: datetime = Field(default_factory=datetime.now)

# Tabla 2: Recomendaciones
class Recomendacion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    empresa_id: int = Field(foreign_key="empresa.id")
    instrumento_optimo: str
    tna: float
    monto_invertir: float
    rendimiento_30d: float
    rendimiento_12m: float
    score: float
    ranking_json: str  # JSON con top 5 alternativas
    creado_en: datetime = Field(default_factory=datetime.now)

# Tabla 3: Historial de Tasas
class HistorialTasa(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    instrumento: str
    tna: float
    fuente: str  # "BCRA API v4" o "fallback"
    fecha_dato: date
    plazo_min: int
    liquidez: int
    riesgo: int
    tipo: str
    creado_en: datetime = Field(default_factory=datetime.now)

# Tabla 4: Alertas
class Alerta(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    empresa_id: int = Field(foreign_key="empresa.id")
    tipo: str  # CAJA_OCIOSA, VENCIMIENTO, REBALANCEO
    mensaje: str
    monto_afectado: Optional[float] = None
    resuelta: bool = Field(default=False)
    creado_en: datetime = Field(default_factory=datetime.now)
    resuelta_en: Optional[datetime] = None

# Engine y creación de tablas
DATABASE_URL = "sqlite:///./robo_advisor.db"
engine = create_engine(DATABASE_URL, echo=False)

def init_db():
    """Crea todas las tablas si no existen"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Retorna una nueva sesión de base de datos"""
    return Session(engine)

if __name__ == "__main__":
    init_db()
    print("✅ Base de datos inicializada")
    print("✅ Tablas: Empresa, Recomendacion, HistorialTasa, Alerta")
