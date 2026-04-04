# CrateDigger

DJ transition intelligence engine. Finds optimal song transitions based on BPM, Camelot key, energy, mood, and genre compatibility.

## Stack
- Apache Airflow — pipeline orchestration
- PySpark — data transformation
- Apache Iceberg — table format
- PostgreSQL — metadata + results
- Docker Compose — local environment

## Setup
1. Copy `.env.example` to `.env` and fill in your values
2. `docker compose up`
