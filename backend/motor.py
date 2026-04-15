# motor.py - Motor de scoring y recomendación
from dataclasses import dataclass
from typing import List, Dict
import json

@dataclass
class Instrumento:
    nombre: str
    tna: float
    plazo_min: int
    liquidez: int  # 1-5
    riesgo: int    # 1-5
    tipo: str

@dataclass
class PerfilEmpresa:
    nombre: str
    caja_total: float
    reserva_minima: float
    horizonte_dias: int
    perfil_riesgo: str  # conservador, moderado, agresivo

@dataclass
class Recomendacion:
    empresa: str
    instrumento_optimo: str
    tna: float
    monto_invertir: float
    rendimiento_30d: float
    rendimiento_12m: float
    score: float
    ranking: List[Dict]

def calcular_score(instrumento: Instrumento, perfil: PerfilEmpresa) -> float:
    # Peso 60% rendimiento, 25% liquidez, 15% riesgo
    score_rendimiento = (instrumento.tna / 40.0) * 0.6
    score_liquidez = (instrumento.liquidez / 5.0) * 0.25
    
    penalizacion_riesgo = 0
    if perfil.perfil_riesgo == "conservador":
        penalizacion_riesgo = (instrumento.riesgo / 5.0) * 0.15
    elif perfil.perfil_riesgo == "moderado":
        penalizacion_riesgo = (instrumento.riesgo / 5.0) * 0.08
    
    return min(100, (score_rendimiento + score_liquidez - penalizacion_riesgo) * 100)

def recomendar_instrumento(perfil: PerfilEmpresa, instrumentos: List[Instrumento]) -> Recomendacion:
    scores = []
    for i in instrumentos:
        if i.plazo_min <= perfil.horizonte_dias:
            s = calcular_score(i, perfil)
            scores.append({"instrumento": i.nombre, "tna": i.tna, "score": round(s, 1)})
    
    scores.sort(key=lambda x: x["score"], reverse=True)
    optimo = scores[0] if scores else None
    
    if not optimo:
        return None
    
    monto = max(0, perfil.caja_total - perfil.reserva_minima)
    rend_30d = (monto * optimo["tna"] / 100) * (30/365)
    rend_12m = (monto * optimo["tna"] / 100)
    
    return Recomendacion(
        empresa=perfil.nombre,
        instrumento_optimo=optimo["instrumento"],
        tna=optimo["tna"],
        monto_invertir=monto,
        rendimiento_30d=rend_30d,
        rendimiento_12m=rend_12m,
        score=optimo["score"],
        ranking=scores[:5]
    )
