
# 🚀 Pravah — LLMOps-Driven AI Travel Planner *(Early-Stage Foundation)*

**Pravah** is an **early-stage, production-ready foundation** for an AI-powered travel planning platform.
It combines **LLM intelligence**, **real-time maps**, and **deep observability** to demonstrate how a **scalable, reliable AI system** can be built and monitored in practice.

> ⚠️ This project represents the **initial, foundational version of Pravah**, intentionally designed as a **strong technical baseline** rather than a feature-complete product.

---

## 🌍 What Pravah Does (Current Scope)

### 🧭 Travel Planning & Navigation

* User selects **source & destination** using Google Places Autocomplete
* Visualizes **real driving routes** on Google Maps
* Displays **distance & ETA**
* Generates **AI-recommended intermediate stops** (food, nature, heritage, rest)
* Places **accurate markers directly on the route**
* Presents a clean **itinerary summary UI**

> The current focus is correctness, reliability, and observability — **not feature overload**.

---

## 🤖 AI Intelligence (Gemini)

* Uses **Gemini 2.5 Flash** for itinerary generation
* Structured **JSON-only responses** for reliability
* Intelligent stop placement logic (semantic match + fallback)
* Graceful error handling and retries

This layer is intentionally instrumented for **LLMOps observability**, making it suitable for real-world AI deployment scenarios.

---

## 🔍 Observability-First Architecture (Datadog)

Pravah is designed with **production observability as a first-class concern**, even at this early stage.

### 📊 Metrics Emitted

**Backend & API**

* `pravah.api.request.count`
* `pravah.api.request.latency_ms`
* `pravah.api.request.error`
* `pravah.journey.started`
* `pravah.journey.completed`

**LLM (Gemini)**

* `pravah.llm.request.count`
* `pravah.llm.latency_ms`
* `pravah.llm.response.success`
* `pravah.llm.response.failure`

**AI Output Quality**

* `pravah.ai.itinerary.stop.count`
* `pravah.ai.fallback.used`

---

### 🚨 Detection Rules Implemented

* High API error rate
* High LLM latency
* LLM agent error spikes
* Silent failures (no successful LLM calls)
* Integration health monitoring

Each alert is **actionable** and tagged by environment and service.

---

### 📈 Datadog Dashboards

The dashboards surface:

* API performance and reliability
* Journey funnel (start → completion)
* LLM latency and success/failure
* AI output behavior
* Container-level CPU metrics (Docker)

These dashboards reflect **how early AI platforms should be monitored in production**.

---

## 🏗️ Architecture Overview

```
React Frontend (Vite)
        |
        v
FastAPI Backend (Python)
        |
        +--> Google Maps APIs
        |
        +--> Gemini LLM
        |
        +--> Datadog Metrics & Monitoring
```

All services are orchestrated via **Docker Compose**.

---

## 🐳 Dockerized Deployment

### Prerequisites

* Docker Desktop
* Datadog API key
* Google Maps API key
* Gemini API key

---

### Environment Setup (`.env`)

Create a `.env` file locally (never committed):

```env
# Datadog
DD_API_KEY=your_datadog_api_key
DD_SITE=us5.datadoghq.com

# Gemini
GEMINI_API_KEY=your_gemini_api_key

# Google Maps
VITE_GOOGLE_MAPS_API_KEY=your_google_maps_key
```

---

### Run the Application

```bash
docker-compose up --build
```

---

### Access

| Service                | URL                                                      |
| ---------------------- | -------------------------------------------------------- |
| Frontend               | [http://localhost:5173](http://localhost:5173)           |
| Backend (FastAPI Docs) | [http://localhost:8000/docs](http://localhost:8000/docs) |
| Datadog                | [https://app.datadoghq.com](https://app.datadoghq.com)   |

---

##  How to Run This

1. Clone the repository
2. Create a `.env` file
3. Run `docker-compose up --build`
4. Use the web UI
5. Observe live metrics and alerts in Datadog

This workflow mirrors **real production onboarding**.

---

## 🔐 Security & Best Practices

* Secrets stored only in environment variables
* `.env` excluded via `.gitignore`
* No hard-coded credentials
* Reproducible Docker-based setup

---

## 🧠 Why This Project Matters (Even at an Early Stage)

✔ Shows **engineering discipline from day one**
✔ Demonstrates **LLMOps & observability**, not just AI output
✔ Designed for scale and monitoring, not demos
✔ Clean separation of concerns
✔ Strong foundation for future expansion

---

## 🔮 Planned Future Evolution

Pravah is intentionally positioned as a **starting point** for a larger platform:

* Voice-based trip planning
* Real-time navigation updates
* Personalization and memory
* Cost-aware LLM routing
* Distributed tracing (APM)
* Multi-agent planning and feedback loops

---

## 👨‍💻 Author

Built as a **foundational prototype** to demonstrate how modern AI systems should be designed, observed, and deployed from the very beginning.



