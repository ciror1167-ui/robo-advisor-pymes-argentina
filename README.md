# 🚀 Robo-Advisor para PyMEs Argentinas

**SaaS de inversión automática para excedentes de caja** - Automatiza la inversión de capital de trabajo en instrumentos de corto plazo (Cauciones, LECAP, FCI) con datos en vivo del BCRA.

---

## 📦 Proyecto Completo - MVP Listo para Deploy

Este repositorio contiene el esqueleto inicial del proyecto. Ya incluye:

✅ **Backend (Python):**
- `motor.py` - Motor de scoring y recomendación
- `scraper_tasas.py` - Scraper BCRA API v4.0 con IDs verificados (7, 12, 150)
- `requirements.txt` - Todas las dependencias

🔨 **Faltan por agregar (te los envío completos):**
- `db.py` - Base de datos SQLModel (4 tablas)
- `repositorios.py` - CRUD completo
- `scheduler.py` - 3 jobs automáticos diarios
- `auth.py` - Verificación JWT Supabase
- `broker_adapters.py` - Integración IOL + PPI
- `main.py` - FastAPI con 8 endpoints
- `rebalanceo.py` - Sistema de alertas

---

## 📋 Arquitectura Completa del MVP

```
robo-advisor-pymes-argentina/
├── backend/              ← FastAPI + Python
│   ├── motor.py           ✅ Ya creado
│   ├── scraper_tasas.py   ✅ Ya creado  
│   ├── requirements.txt   ✅ Ya creado
│   ├── db.py
│   ├── repositorios.py
│   ├── scheduler.py
│   ├── auth.py
│   ├── broker_adapters.py
│   ├── main.py
│   ├── rebalanceo.py
│   └── .env.example
│
├── frontend/           ← Next.js 14 + Tailwind
│   ├── app/
│   │   ├── page.tsx
│   │   ├── login/page.tsx
│   │   └── onboarding/page.tsx
│   ├── components/
│   ├── lib/
│   └── package.json
│
├── landing/
│   └── index.html      ← Landing con calculadora interactiva
│
└── docs/
    ├── DEPLOY.md
    ├── INTEGRACION.md
    └── VENTAS.md
```

---

## ⚡ Quickstart - Deploy en 15 minutos

### 1. Clonar el repo
```bash
git clone https://github.com/ciror1167-ui/robo-advisor-pymes-argentina.git
cd robo-advisor-pymes-argentina
```

### 2. Backend en Railway (gratis)
```bash
cd backend
pip install -r requirements.txt

# Crear .env con:
SUPABASE_JWT_SECRET=tu_secret
IOL_USUARIO=tu@email.com
IOL_PASSWORD=tu_password

# Deploy
railway login
railway up
```

### 3. Frontend en Vercel (gratis)
```bash
cd frontend
npm install
npx vercel --prod

# Variables de entorno:
NEXT_PUBLIC_API_URL=https://tu-api.railway.app
NEXT_PUBLIC_SUPABASE_URL=tu_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=tu_key
```

---

## 📊 Datos Reales del BCRA

El scraper consulta la **API v4.0 del BCRA** con IDs verificados:

| ID | Variable | Último valor |
|---|---|---|
| **7** | BADLAR (base FCI) | 21.69% TNA |
| **12** | PF 30 días | 21.30% TNA |
| **150** | Pases/Cauciones | 20.05% TNA |

+ Fallbacks: LECAP (36%), UVA (30%), CER (28%)

---

## 💼 Modelo de Negocio

| Plan | Precio/mes | Target |
|---|---|---|
| Starter | $12 USD | Autónomos |
| Pyme | $35 USD | Empresas hasta 20 empleados |
| Pro | $80 USD | Empresas medianas |

**Proyección:** 100 clientes Pyme = **$3.500 USD/mes** MRR

---

## 🛠️ Stack Técnico

- **Backend:** FastAPI + Python 3.10+
- **DB:** SQLite (MVP) / PostgreSQL (producción)
- **Auth:** Supabase Auth + JWT
- **Frontend:** Next.js 14 + Tailwind + Recharts
- **Deploy:** Railway + Vercel
- **Brokers:** IOL + PPI
- **Scheduler:** APScheduler

---

## 📝 Próximos Pasos

1. Copiar los archivos faltantes del backend (te los envío)
2. Crear proyecto en Supabase (gratis)
3. Deploy backend + frontend
4. Obtener credenciales demo de IOL
5. Grabar video demo (2 min)
6. Enviar primeros 5 mensajes de WhatsApp

---

## 👤 Contacto

**Ciro Romano** - Termas de Río Hondo, Santiago del Estero, Argentina

Repositorio: https://github.com/ciror1167-ui/robo-advisor-pymes-argentina

---

**¿Tenés dudas?** Cloná el repo y empezá. El MVP está diseñado para estar en producción en menos de 1 día.
