from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import shutil
from datetime import datetime
from dotenv import load_dotenv
from typing import Optional

from app.services.product_service import ProductService

load_dotenv()

app = FastAPI(title="Sukata API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

product_service = ProductService()

@app.get("/")
def root():
    return {"message": "Sukata API funcionando", "status": "online"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/api/products")
def get_products():
    """Obtener todos los productos"""
    return product_service.get_all()

@app.get("/api/products/{product_id}")
def get_product(product_id: int):
    """Obtener un producto por ID"""
    product = product_service.get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

@app.post("/api/products")
async def create_product(
    name: str = Form(...),
    category: str = Form("otro"),
    defect: str = Form(...),
    status: str = Form("pendiente"),
    notes: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None)
):
    """Crear un nuevo producto"""
    image_url = None
    if image:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{image.filename}"
        filepath = f"uploads/{filename}"
        
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        
        image_url = f"/uploads/{filename}"
    
    product_id = product_service.create(name, category, defect, status, notes, image_url)
    
    return {"message": "Producto creado", "id": product_id}

@app.put("/api/products/{product_id}")
def update_product(product_id: int, status: str):
    """Actualizar estado de un producto"""
    product = product_service.get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    product_service.update_status(product_id, status)
    return {"message": "Producto actualizado"}

@app.delete("/api/products/{product_id}")
def delete_product(product_id: int):
    """Eliminar un producto"""
    product = product_service.get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    product_service.delete(product_id)
    return {"message": "Producto eliminado"}

@app.get("/api/statistics")
def get_statistics():
    """Obtener estadísticas para dashboard"""
    return product_service.get_statistics()

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