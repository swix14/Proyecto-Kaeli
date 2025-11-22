import time
from .base import ScrapingStrategy
from .mock_data import MOCK_PRODUCTOS

class SantaIsabelScraping(ScrapingStrategy):
    def extraer_precios(self, producto_nombre):
        time.sleep(0.01)
        producto_key = producto_nombre.lower()
        producto_data = MOCK_PRODUCTOS.get(producto_key)
        if producto_data:
            return {
                "supermercado": "Santa Isabel",
                "producto": producto_data["nombre_generico"],
                "precio": producto_data["precios"]["santa_isabel"]
            }
        return {"supermercado": "Santa Isabel", "producto": producto_nombre, "error": "Producto no encontrado"}
