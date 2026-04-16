# repositorios.py - CRUD completo para todas las entidades
from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
import json

from db import Empresa, Recomendacion, HistorialTasa, Alerta, get_session

# Repositorio de Empresas
class EmpresaRepo:
    @staticmethod
    def crear(empresa: Empresa) -> Empresa:
        with get_session() as session:
            session.add(empresa)
            session.commit()
            session.refresh(empresa)
            return empresa
    
    @staticmethod
    def listar() -> List[Empresa]:
        with get_session() as session:
            return session.exec(select(Empresa)).all()
    
    @staticmethod
    def por_id(empresa_id: int) -> Optional[Empresa]:
        with get_session() as session:
            return session.get(Empresa, empresa_id)
    
    @staticmethod
    def por_supabase_uid(uid: str) -> Optional[Empresa]:
        with get_session() as session:
            return session.exec(select(Empresa).where(Empresa.supabase_uid == uid)).first()
    
    @staticmethod
    def actualizar(empresa: Empresa) -> Empresa:
        with get_session() as session:
            empresa.actualizado_en = datetime.now()
            session.add(empresa)
            session.commit()
            session.refresh(empresa)
            return empresa

# Repositorio de Recomendaciones
class RecomendacionRepo:
    @staticmethod
    def crear(rec: Recomendacion) -> Recomendacion:
        with get_session() as session:
            session.add(rec)
            session.commit()
            session.refresh(rec)
            return rec
    
    @staticmethod
    def ultima_por_empresa(empresa_id: int) -> Optional[Recomendacion]:
        with get_session() as session:
            return session.exec(
                select(Recomendacion)
                .where(Recomendacion.empresa_id == empresa_id)
                .order_by(Recomendacion.creado_en.desc())
            ).first()
    
    @staticmethod
    def historial(empresa_id: int, limit: int = 10) -> List[Recomendacion]:
        with get_session() as session:
            return session.exec(
                select(Recomendacion)
                .where(Recomendacion.empresa_id == empresa_id)
                .order_by(Recomendacion.creado_en.desc())
                .limit(limit)
            ).all()

# Repositorio de Historial de Tasas
class HistorialTasaRepo:
    @staticmethod
    def crear(tasa: HistorialTasa) -> HistorialTasa:
        with get_session() as session:
            session.add(tasa)
            session.commit()
            session.refresh(tasa)
            return tasa
    
    @staticmethod
    def ultimas_tasas() -> List[HistorialTasa]:
        """Retorna las últimas tasas de cada instrumento"""
        with get_session() as session:
            # Subconsulta para obtener la fecha más reciente por instrumento
            subq = (
                select(HistorialTasa.instrumento, HistorialTasa.fecha_dato.label("max_fecha"))
                .group_by(HistorialTasa.instrumento)
            )
            
            return session.exec(
                select(HistorialTasa)
                .order_by(HistorialTasa.creado_en.desc())
                .limit(10)
            ).all()
    
    @staticmethod
    def por_instrumento(nombre: str, dias: int = 30) -> List[HistorialTasa]:
        with get_session() as session:
            return session.exec(
                select(HistorialTasa)
                .where(HistorialTasa.instrumento == nombre)
                .order_by(HistorialTasa.fecha_dato.desc())
                .limit(dias)
            ).all()

# Repositorio de Alertas
class AlertaRepo:
    @staticmethod
    def crear(alerta: Alerta) -> Alerta:
        with get_session() as session:
            session.add(alerta)
            session.commit()
            session.refresh(alerta)
            return alerta
    
    @staticmethod
    def pendientes(empresa_id: int) -> List[Alerta]:
        with get_session() as session:
            return session.exec(
                select(Alerta)
                .where(Alerta.empresa_id == empresa_id, Alerta.resuelta == False)
                .order_by(Alerta.creado_en.desc())
            ).all()
    
    @staticmethod
    def resolver(alerta_id: int) -> Optional[Alerta]:
        with get_session() as session:
            alerta = session.get(Alerta, alerta_id)
            if alerta:
                alerta.resuelta = True
                alerta.resuelta_en = datetime.now()
                session.add(alerta)
                session.commit()
                session.refresh(alerta)
            return alerta
    
    @staticmethod
    def todas_pendientes() -> List[Alerta]:
        """Para el scheduler"""
        with get_session() as session:
            return session.exec(
                select(Alerta)
                .where(Alerta.resuelta == False)
                .order_by(Alerta.creado_en.desc())
            ).all()
