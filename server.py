import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client

# --- CONFIGURACIÓN SUPABASE ---
# Reemplaza con tus credenciales reales de Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://jrmeoeozxavnpaljmbhq.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpybWVvZW96eGF2bnBhbGptYmhxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODYxNTY0ODEsImV4cCI6MjEwMTczMjQ4MX0.GeQ1jP2vHZcmRib3EfsE348sm3JUjh8blM1DkJw8DGQ")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- APLICACIÓN FASTAPI ---
app = FastAPI(
    title="Web Scraping REST API",
    description="Backend para persistencia e integración entre Web Scraper y Frontend",
    version="1.0.0"
)

# Permitir CORS para la interfaz Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODELOS DE DATOS (Pydantic) ---
class ItemCreate(BaseModel):
    nombre: str
    precio: Optional[str] = None
    precio_lista: Optional[str] = None
    url: Optional[str] = None
    imagen: Optional[str] = None

class ItemResponse(ItemCreate):
    id: int
    created_at: str

# --- ENDPOINTS ---

@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "API RESTful operativa"}


# Endpoint POST /api/items (Recepción e Inserción Masiva o Individual)
@app.post("/api/items", status_code=status.HTTP_201_CREATED, tags=["Items"])
def guardar_items(payload: List[ItemCreate]):
    """
    Recibe el payload en formato JSON desde scraper.py y
    ejecuta la insercion masiva en Supabase.
    """
    if not payload:
        raise HTTPException(status_code=400, detail="El payload no puede estar vacío")
    
    # Convertir Pydantic a lista de diccionarios
    items_dict = [item.model_dump() for item in payload]
    
    try:
        response = supabase.table("scraped_items").insert(items_dict).execute()
        return {
            "mensaje": f"Se insertaron {len(response.data)} registros exitosamente.",
            "registros_insertados": response.data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al insertar en Supabase: {str(e)}")


# Endpoint GET /api/items (Consulta Cronológica para Frontend)
@app.get("/api/items", response_model=List[ItemResponse], tags=["Items"])
def obtener_items():
    """
    Consulta Supabase y retorna todos los registros ordenados cronologicamente (ultimos primero).
    """
    try:
        response = (
            supabase.table("scraped_items")
            .select("*")
            .order("created_at", desc=True)
            .execute()
        )
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar Supabase: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)