# Proyecto Kaeli 🛒
**Tu mejor precio siempre**

## 📖 Descripción
Kaeli es una aplicación web que permite comparar precios de productos de la canasta básica entre distintos supermercados chilenos.  
Los usuarios pueden:
- Buscar productos
- Comparar precios en tiempo real
- Gestionar listas de deseos
- Simular compras en un carrito virtual
- Dejar y votar reseñas
- Recibir recomendaciones personalizadas mediante un asistente inteligente

---

## 🚀 Tecnologías
- **Backend:** Python 3.10+ con Flask
- **Frontend:** HTML, CSS, JavaScript
- **Web Scraping:** BeautifulSoup4, Requests, lxml
- **Base de Datos:** JSON (MVP) / PostgreSQL (futuro)
- **Autenticación:** Flask-JWT-Extended
- **Control de versiones:** Git + GitHub
- **Diagramas UML:** PlantUML / Mermaid

---

## 📂 Estructura del repositorio
│── kaeli-mvp/ # Código fuente (Flask, scraping, lógica de negocio) 

│── tests/ # Pruebas unitarias con pytest 

│── docs/ # Documentación (requirements.md, implementation_plan.md) 

│── diagrams/ # Diagramas UML (clases, casos de uso, despliegue) 

│── data/ # Archivos JSON con precios y logs 

│── README.md # Este archivo 

│── requirements.txt # Dependencias del proyecto

---

## ⚙️ Instalación y Uso
1. Clonar el repositorio:
   ```bash
   git clone https://github.com/swix14/Proyecto-Kaeli.git
   cd Proyecto-Kaeli

2.Crear entorno virtual e instalar dependencias:
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

3.Ejecutar aplicacion
```bash
python run.py
```
4.Acceder desde el navegador:
http://localhost:5000

---

##  👥Equipo
- Sebastián Olguin – Backend, scraping, lógica de comparación, base de datos

- Sebastián Ayenao – Frontend, UX/UI, diseño de interfaz web

- Ambos – Documentación y QA

---

## 📌RoadMap
[x] Registro e inicio de sesión

[ ] Scraping básico (Jumbo, Líder)

[x] Comparación de precios

[x] Carrito de compras simulado

[ ] Sistema de reseñas y votaciones

[x] Asistente IA básico

[x] Migración futura a PostgreSQL

[ ] App móvil

---

## 📜Licencia
Este proyecto es académico y no está destinado a producción comercial. Uso libre para fines educativos.




