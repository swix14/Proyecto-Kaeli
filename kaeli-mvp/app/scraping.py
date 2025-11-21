# app/scraping.py (Versión MOCK - Garantizada)

from abc import ABC, abstractmethod
import time 

# --- BASE DE DATOS SIMULADA DE PRECIOS ---
MOCK_PRODUCTOS = {
    "arroz": {
        "nombre_generico": "Arroz Grado 1, 1kg (Simulado)",
        "precios": {
            "lider": 1150,
            "jumbo": 1200,
            "santa_isabel": 1180
        }
    },
    "fideos": {
        "nombre_generico": "Fideos N°5, 400g (Simulado)",
        "precios": {
            "lider": 990,
            "jumbo": 1050,
            "santa_isabel": 1020
        }
    },
    "azucar": {
        "nombre_generico": "Azúcar Blanca, 1kg (Simulado)",
        "precios": {
            "lider": 1300,
            "jumbo": 1350,
            "santa_isabel": 1320
        }
    },
    "sal": {
        "nombre_generico": "Sal de Mesa, 1kg (Simulado)",
        "precios": {
            "lider": 800,
            "jumbo": 820,
            "santa_isabel": 810
        }
    },
    "cafe": {
        "nombre_generico": "Café Nescafé Clásico, 170g (Simulado)",
        "precios": {
            "lider": 4500,
            "jumbo": 4700,
            "santa_isabel": 4600
        }
    }
}

class ScrapingStrategy(ABC):
    @abstractmethod
    def extraer_precios(self, producto_nombre):
        pass

class LiderScraping(ScrapingStrategy):
    def extraer_precios(self, producto_nombre):
        time.sleep(0.01)
        producto_key = producto_nombre.lower()
        producto_data = MOCK_PRODUCTOS.get(producto_key)
        if producto_data:
            return { 
                "supermercado": "Líder", # Con tilde para que se vea bonito
                "producto": producto_data["nombre_generico"], 
                "precio": producto_data["precios"]["lider"]
            }
        return {"supermercado": "Líder", "producto": producto_nombre, "error": "Producto no encontrado"}

class JumboScraping(ScrapingStrategy):
    def extraer_precios(self, producto_nombre):
        time.sleep(0.01)
        producto_key = producto_nombre.lower()
        producto_data = MOCK_PRODUCTOS.get(producto_key)
        if producto_data:
            return { 
                "supermercado": "Jumbo", 
                "producto": producto_data["nombre_generico"], 
                "precio": producto_data["precios"]["jumbo"]
            }
        return {"supermercado": "Jumbo", "producto": producto_nombre, "error": "Producto no encontrado"}

class SantalsabelScraping(ScrapingStrategy):
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

class ScrapingFactory:
    def crear_scraper(self, supermercado):
        if supermercado == "jumbo": return JumboScraping()
        elif supermercado == "lider": return LiderScraping()
        elif supermercado == "santa_isabel": return SantalsabelScraping()
        else: raise ValueError("Supermercado no soportado")