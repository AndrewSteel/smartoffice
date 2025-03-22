
# 🧠 SmartOffice

SmartOffice ist eine modulare, KI-gestützte Plattform zur digitalen Verwaltung von Dokumenten, Bildern und anderen relevanten Informationen – lokal, hybrid oder in der Cloud.
Ziel ist es, ein vollständig integriertes, intelligentes System für das papierlose Büro der Zukunft zu schaffen – technisch schlank, erweiterbar und datenschutzfreundlich.

---

## 🚀 Komponenten

| Dienst          | Funktion                                     |
|-----------------|----------------------------------------------|
| `backend`        | FastAPI-Server zum Hochladen & Steuern      |
| `ollama-client`  | Subscribt per MQTT und generiert Bildbeschreibung mit Ollama |
| `ollama`         | LLM-Modellserver (z. B. mit LLaVA)           |
| `mqtt` (Mosquitto) | Message Broker zur Verarbeitung             |
| `mongo`          | Speicherung der Metadaten                   |

---

## ⚙️ Setup & Start

### 🔁 Voraussetzung

- **Docker & Docker Compose** installiert
- Optional: **NVIDIA GPU + Container Toolkit** für GPU-Beschleunigung

### 📂 Verzeichnisstruktur

```text
.
├── docker-compose.yml
├── .env
├── backend/
├── ollama-client/
├── frontend/        # optional
├── mosquitto/
│   └── config/mosquitto.conf
├── shared/uploads/
```

---

## 🐳 Docker starten

```bash
docker compose up -d
```

**Wichtig:** Stelle sicher, dass dein NVIDIA-Toolkit korrekt installiert ist, falls du die GPU nutzen möchtest (siehe unten).

---

## 🧠 GPU-Nutzung mit Ollama

### Voraussetzung

Damit der `ollama`-Container die GPU nutzen kann, muss **das NVIDIA Container Toolkit** installiert sein:

👉 Anleitung:  
<https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html>

### Prüfung

```bash
docker info | grep -i nvidia
```

### Docker Compose Konfiguration (auszug)

```yaml
  ollama:
    runtime: nvidia
    deploy:
      resources:
        reservations:
          devices:
            - capabilities: [gpu]
```

💡 Bei Problemen kannst du die Zeilen `runtime` und `deploy` auch auskommentieren, um Ollama nur mit CPU laufen zu lassen.

---

## 🌐 API-Endpunkte

- `POST /upload/` – Bild hochladen
- `GET /images/` – Liste aller Bilder mit Beschreibung

(Frontend-UI folgt)

---

## 🛰️ MQTT Topics

| Topic                            | Zweck                          |
|----------------------------------|---------------------------------|
| `smartoffice/image/uploaded`     | Wird vom Backend gesendet       |
| `smartoffice/image/described`    | Wird vom Ollama-Client veröffentlicht |

---

## 📦 Versionierung

Aktuelle Version: **v0.1 – Rapid Prototype**

Geplant:

- [ ] Frontend (Upload + Vorschau)
- [ ] Ähnlichkeitsanalyse (FAISS)
- [ ] Automatisches Tagging
- [ ] Videoverarbeitung

---

## 🧪 Test

Nach dem Start erreichst du das Backend unter:  
📍 <http://localhost:8000/docs> (Swagger-UI für API-Test)

---

## 🧊 Kontakt / Weiterentwicklung

Ziel ist eine modulare, lokale oder cloudbasierte SmartOffice-Lösung für Einzelanwender und KMU.  
Fragen, Ideen oder Erweiterungen?
