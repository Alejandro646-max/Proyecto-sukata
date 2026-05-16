"""
SUKATA - Backend Principal
Sistema de Registro de Defectos de Equipos
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Crear la aplicación FastAPI
app = FastAPI(
    title="Sukata API",
    description="API para el sistema de registro de defectos de equipos",
    version="1.0.0"
)

# Configurar CORS (permite que Flutter hable con el backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear carpeta uploads si no existe
os.makedirs("uploads", exist_ok=True)

# Montar carpeta para archivos estáticos (imágenes)
try:
    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
except Exception as e:
    print(f"Error montando uploads: {e}")

# ============================================
# ENDPOINTS BÁSICOS
# ============================================

@app.get("/")
def root():
    """Endpoint principal - verifica que el API funciona"""
    return {
        "message": "🚀 Sukata API funcionando correctamente",
        "version": "1.0.0",
        "status": "online"
    }

@app.get("/health")
def health_check():
    """Endpoint para verificar que el servidor está vivo"""
    return {
        "status": "healthy",
        "database": "pending"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("API_PORT", 8000))
    print(f"🎯 Iniciando Sukata API en http://localhost:{port}")
    print(f"📖 Documentación en http://localhost:{port}/docs")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )