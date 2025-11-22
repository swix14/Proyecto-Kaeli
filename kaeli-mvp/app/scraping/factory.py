# app/scraping/factory.py
from .jumbo import JumboScraping
from .lider import LiderScraping
from .santa_isabel import SantaIsabelScraping

class ScrapingFactory:
    def crear_scraper(self, supermercado):
        if supermercado == "jumbo":
            return JumboScraping()
        elif supermercado == "lider":
            return LiderScraping()
        elif supermercado == "santa_isabel":
            return SantaIsabelScraping()
        else:
            raise ValueError("Supermercado no soportado")
