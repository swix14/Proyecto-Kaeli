from abc import ABC, abstractmethod

class ScrapingStrategy(ABC):
    @abstractmethod
    def extraer_precios(self, producto_nombre):
        pass
