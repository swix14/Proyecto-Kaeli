import os

class ConfiguracionGlobal:
    def __init__(self):
        self.api_key = os.getenv("KAELI_API_KEY", "kaeli_dev")
        
        super_activos_env = os.getenv("SUPER_ACTIVOS")
        if super_activos_env:
            self.supermercados_activos = [s.strip() for s in super_activos_env.split(",")]
        else:
            self.supermercados_activos = ["jumbo", "lider", "santa_isabel"]

        # Base de datos: prioriza DATABASE_URL
        self.SQLALCHEMY_DATABASE_URI = os.getenv(
            "DATABASE_URL",
            "postgresql://postgres:seba1107@localhost:5432/kaeli"
        )

        self.SQLALCHEMY_TRACK_MODIFICATIONS = False

    def mostrar_configuracion(self):
        return {
            "db_uri": self.SQLALCHEMY_DATABASE_URI,
            "supermercados_activos": self.supermercados_activos
        }

config_global = ConfiguracionGlobal()
