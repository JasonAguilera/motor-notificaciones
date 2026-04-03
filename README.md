# motor-notificaciones
Descripción del Proyecto
Sistema de notificaciones en tiempo real para una red social, capaz de procesar eventos de interacción de usuarios (likes, comentarios, seguidores) y entregarlos al destinatario en menos de 500 ms. El sistema está diseñado para iterar rápidamente sobre nuevas funcionalidades mediante una arquitectura modular y desacoplada.
Arquitectura Seleccionada
Pipeline Híbrido Modular

El sistema se organiza en módulos independientes conectados por un bus de eventos:

Fuentes de Eventos → Kafka/Redis → Flink (Procesamiento) → API Gateway → Clientes

                                                         ↕

                                                    PostgreSQL

Cada módulo puede desplegarse, escalarse y actualizarse de forma independiente, permitiendo que el equipo de producto experimente con nuevas ideas sin afectar la estabilidad del core.
Requisitos y Configuración del Entorno Técnico
Herramienta
Versión
Rol en el proyecto
Git
≥ 2.40
Control de versiones del código fuente
Docker + Docker Compose
Docker ≥ 24, Compose v2
Contenedorización de todos los servicios
Python
3.11+
Workers de procesamiento y APIs
Apache Kafka
3.7 (via Docker)
Bus de eventos principal
Redis
7.x (via Docker)
Streams para notificaciones de baja latencia
Apache Flink
1.18 (via Docker)
Motor de procesamiento de streams
PostgreSQL
15 (via Docker)
Almacenamiento de notificaciones y preferencias
FastAPI
0.111+
Framework para APIs REST y WebSockets
Grafana
10.x (via Docker)
Dashboard de métricas de engagement

Instrucciones de Instalación
# 1. Clonar el repositorio

git clone https://github.com/[usuario]/motor-notificaciones.git

cd motor-notificaciones

# 2. Copiar y configurar variables de entorno

cp .env.example .env

# Editar .env con credenciales de BD, secreto JWT, etc.

# 3. Levantar toda la infraestructura con Docker Compose

docker compose up -d

# 4. Verificar que los servicios estén activos

docker compose ps

# 5. Ejecutar migraciones de base de datos

docker compose exec api python scripts/migrate.py

# 6. Verificar el sistema enviando un evento de prueba

curl -X POST http://localhost:8000/api/eventos/test \

  -H "Content-Type: application/json" \

  -d '{"tipo": "like", "usuario_origen_id": "uuid-1", "usuario_destino_id": "uuid-2"}'
Estructura del Repositorio
motor-notificaciones/

│

├── docker-compose.yml          # Orquestación de todos los servicios

├── .env.example                # Plantilla de variables de entorno

├── README.md                   # Este archivo

│

├── ingesta/                    # Productor de eventos → Kafka

│   ├── producer.py

│   └── Dockerfile

│

├── procesamiento/              # Jobs de Apache Flink

│   ├── flink_job.py            # Lógica de agregación y reglas de negocio

│   ├── reglas/

│   │   ├── likes_handler.py

│   │   ├── comments_handler.py

│   │   └── follows_handler.py

│   └── Dockerfile

│

├── api/                        # API Gateway (FastAPI)

│   ├── main.py

│   ├── routers/

│   │   ├── notificaciones.py

│   │   ├── preferencias.py

│   │   └── websocket.py

│   ├── models/                 # Modelos SQLAlchemy

│   ├── schemas/                # Esquemas Pydantic

│   └── Dockerfile

│

├── db/

│   └── migrations/             # Scripts SQL de migración

│

├── monitoring/

│   └── grafana/

│       └── dashboards/         # Definición de paneles Grafana

│

└── tests/

    ├── test_ingesta.py

    ├── test_procesamiento.py

    └── test_api.py



