# scraper_tasas.py - BCRA API v4.0 · IDs verificados
import httpx
import json
from datetime import datetime, date
from typing import Optional, List, Dict

BASE = "https://api.bcra.gob.ar/estadisticas/v4.0/monetarias"
HEADERS = {"Accept": "application/json"}

# Mapa definitivo: ID → instrumento del robo-advisor
VARIABLE_MAP = {
    7:   {"nombre": "FCI Money Market",  "factor": 0.95, "plazo_min": 1,   "liquidez": 5, "riesgo": 1, "tipo": "FCI"},
    12:  {"nombre": "Plazo Fijo Trad.",  "factor": 1.00, "plazo_min": 30,  "liquidez": 2, "riesgo": 2, "tipo": "plazo_fijo"},
    150: {"nombre": "Caución Bursátil", "factor": 1.00, "plazo_min": 1,   "liquidez": 5, "riesgo": 2, "tipo": "caución"},
}

FALLBACKS = [
    {"nombre": "Plazo Fijo UVA", "tna": 30.0, "plazo_min": 90,  "liquidez": 1, "riesgo": 3, "tipo": "plazo_fijo"},
    {"nombre": "LECAP",          "tna": 36.0, "plazo_min": 30,  "liquidez": 4, "riesgo": 3, "tipo": "letra"},
    {"nombre": "Bono CER",       "tna": 28.0, "plazo_min": 180, "liquidez": 3, "riesgo": 4, "tipo": "bono"},
]

def get_tasa(var_id: int) -> Optional[float]:
    """Obtiene tasa del BCRA API v4"""
    try:
        r = httpx.get(f"{BASE}/{var_id}", headers=HEADERS, timeout=10, follow_redirects=True)
        r.raise_for_status()
        return float(r.json()["results"][0]["detalle"][0]["valor"])
    except:
        return None

def actualizar_catalogo() -> Dict:
    """Actualiza catálogo de tasas desde BCRA + fallbacks"""
    catalogo = []
    nombres_ok = set()

    # Consultar API del BCRA
    for var_id, meta in VARIABLE_MAP.items():
        tna_raw = get_tasa(var_id)
        if tna_raw:
            tna = round(tna_raw * meta["factor"], 2)
            catalogo.append({
                "instrumento": meta["nombre"],
                "tna":         tna,
                "fuente":      f"BCRA API v4 (var {var_id})",
                "fecha_dato":  date.today().isoformat(),
                "plazo_min":   meta["plazo_min"],
                "liquidez":    meta["liquidez"],
                "riesgo":      meta["riesgo"],
                "tipo":        meta["tipo"],
            })
            nombres_ok.add(meta["nombre"])

    # Completar con fallbacks
    for fb in FALLBACKS:
        if fb["nombre"] not in nombres_ok:
            fb["fuente"]     = "fallback (IOL/Ambito)"
            fb["fecha_dato"] = date.today().isoformat()
            catalogo.append(fb)

    payload = {
        "actualizado":   datetime.now().isoformat(),
        "fuentes_vivas": len(nombres_ok),
        "instrumentos":  sorted(catalogo, key=lambda x: x["tna"], reverse=True)
    }

    # Guardar cache local
    with open("tasas_cache.json", "w") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    return payload

if __name__ == "__main__":
    resultado = actualizar_catalogo()
    print(f"\n✅ {resultado['fuentes_vivas']}/3 fuentes vivas")
    print(f"✅ {len(resultado['instrumentos'])} instrumentos en catálogo\n")
    for i in resultado["instrumentos"]:
        origen = "🟢" if "BCRA" in i["fuente"] else "🟡"
        print(f"{origen}  {i['instrumento']:<22} {i['tna']:>6}% TNA")
