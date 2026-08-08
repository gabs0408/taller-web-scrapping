# Taller Web Scraping, API REST, Supabase & Frontend

Este proyecto implementa una arquitectura completa para la extracción, almacenamiento y visualización de datos web.

## Estructura del Repositorio
- `/api`: Servidor Backend RESTful en FastAPI conectado a Supabase (PostgreSQL).
- `/frontend`: Dashboard interactivo en HTML + TailwindCSS.
- `/scripts`: Web Scraper en Python para extracción automatizada de productos.

## Pasos para Ejecutar

### 1. Backend API
```bash
cd api
pip install -r requirements.txt
python server.py
```
### 2. web scrapper
```bash
cd scripts
python scrapper.py
```
### 3.Frontend
Abrir el archivo index.html en cualquier navegador web.
