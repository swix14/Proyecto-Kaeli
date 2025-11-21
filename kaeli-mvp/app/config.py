# app/config.py
import os

class ConfiguracionGlobal:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            
            # Configuración básica
            cls._instance.api_key = "kaeli_2024"
            cls._instance.supermercados_activos = ["jumbo", "lider", "santa_isabel"]
            
            # Configuración de BD (Asegúrate que tu contraseña esté bien aquí)
            # Si usas SQLite (archivo local), usa esta línea:
            # cls._instance.SQLALCHEMY_DATABASE_URI = 'sqlite:///kaeli.db'
            
            # Si usas PostgreSQL, usa esta (pon tu contraseña real):
            cls._instance.SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:seba1107@localhost:5432/kaeli'
            
            cls._instance.SQLALCHEMY_TRACK_MODIFICATIONS = False
            
        return cls._instance

    def mostrar_configuracion(self):
        return {
            "db_uri": self.SQLALCHEMY_DATABASE_URI,
            # --- ¡AQUÍ ESTABA EL ERROR! ---
            # Antes decía "supermercados", ahora dice "supermercados_activos"
            "supermercados_activos": self.supermercados_activos
        }

config_global = ConfiguracionGlobal()