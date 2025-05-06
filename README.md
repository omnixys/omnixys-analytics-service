# 📊 Omnixys Analytics Service

Der **Omnixys Analytics Service** ist ein zentraler Microservice zur Auswertung und Visualisierung geschäftsrelevanter KPIs (Key Performance Indicators). Er ist Teil des modularen **OmnixysSphere**-Ökosystems und wurde mit **FastAPI**, **GraphQL** und **MongoDB** entwickelt. Der Service unterstützt **Tracing, Logging, Kafka-Messaging** und bietet umfassende Exportfunktionen als CSV und Excel inklusive Visualisierung.

---

## 🔍 Features

- 📈 Analyse von KPIs wie Kundenwachstum, Umsatz, Transaktionen, u. v. m.
- 🗓 Zeitbasierte Auswertung (monatlich, jährlich, benutzerdefiniert)
- 📄 Export als CSV/Excel mit interaktiven Diagrammen
- 🔗 GraphQL-API für flexible Abfragen
- 📈 Interaktive Dashboards (für UI-Anbindung)
- 🔍 Vollständig observierbar via **OpenTelemetry**, **Prometheus**, **Tempo**, **Loki**
- 🔐 Sichere Authentifizierung über **Keycloak**
- 📦 Kafka-Publishing & -Consumption für KPI-Events

---

## ⚙️ Tech Stack

| Komponente       | Technologie            |
|------------------|------------------------|
| Backend          | FastAPI + Strawberry   |
| Authentifizierung| Keycloak               |
| Datenbank        | MongoDB (Beanie ODM)   |
| Messaging        | Apache Kafka           |
| Tracing          | OpenTelemetry + Tempo  |
| Logging          | LoggerPlus + Loki      |
| Monitoring       | Prometheus + Grafana   |

---

## 🗃️ Projektstruktur

```
src/
├── graphql/                # Schema & Resolver
├── services/               # Analytics-Logik
├── models/                 # KPI-Modelle (MongoDB)
├── kafka/                  # Kafka Producer & Consumer
├── export/                 # CSV/Excel Export Utilities
├── observability/          # Tracing, Logging
├── fastapi_app.py          # Einstiegspunkt
```

---

## ⚙️ Setup (lokal)

### 1. Klonen & installieren

```bash
git clone https://github.com/omnixys/omnixys-analytics-service.git
cd omnixys-analytics-service
pip install -r requirements.txt
```

### 2. Starten

```bash
uvicorn src.fastapi_app:app --reload
```

> Alternativ via Docker:
```bash
docker-compose up
```

---

## 🧺a Tests

```bash
pytest
```

---

## 📡 GraphQL Playground

Nach dem Start erreichbar unter:

```
http://localhost:7303/graphql
```

---

## 📄 Export API (REST)

- `GET /export/products/<filename>` → CSV/Excel-Datei mit Diagrammen & Logo

---

## 🛡 Sicherheit

Dieser Service verwendet **Keycloak** zur Authentifizierung. Zugriff auf sensible Mutationen ist auf bestimmte Rollen beschränkt (`Admin`, `helper`).

---

## 🧐 Beitrag leisten

Siehe [CONTRIBUTING.md](../CONTRIBUTING.md) für Richtlinien, Branch-Namen und PR-Workflow.

---

## 📜 Lizenz

Dieser Microservice ist lizenziert unter der [GNU GPL v3.0](../LICENSE).

© 2025 **Omnixys** – The Fabric of Modular Innovation.
