# Plan de Implementación - Kaeli

## 1. Objetivo
Este documento describe el plan de implementación del proyecto **Kaeli**, una página web que utiliza web scraping para mostrar los diversos precios de un mismo producto, reseñas de usuarios y recomendaciones personalizadas mediante un asistente inteligente.

---

## 2. Equipo y Roles
- **Líder/Coordinador**: Sebastian Olguin
  - Gestiona plazos, organización y entregas.  
- **Analista de Requisitos**: Sebastian Olguin  
  - Documenta casos de uso y requisitos.  
- **Diseñador UML**: Sebastian Ayenao  
  - Crea y mantiene los diagramas de clases y casos de uso.  
- **Planificador / Dev Lead**: Sebastian Olguin  
  - Asigna tareas y coordina el desarrollo.  
- **Presentador / QA**: Sebastian Ayenao  
  - Prepara las slides, la demo y asegura la calidad del sistema.  

---

## 3. Tecnologías
- **Lenguaje principal**: Python 3.10+ (Flask)
- **Frontend**: HTML, CSS, JavaScript  
- **Web Scraping**: BeautifulSoup4, Requests
- **Base de Datos**: JSON (MVP)
- **Autenticación**: Flask-JWT-Extended
- **Gestión de dependencias**: pip (requirements.txt)
- **Control de versiones**: Git + GitHub  
- **Diagramas UML**: PlantUML / Draw.io  
- **Documentación**: Markdown (.md)  

---

## 4. Mapeo Casos de Uso → Clases

| Caso de Uso               | Clases Principales Involucradas |
|---------------------------|----------------------------------|
| Registrar usuario          | Usuario                        |
| Iniciar sesión             | Usuario                        |
| Buscar productos           | Producto, Comparador           |
| Comparar precios           | Producto, Precio, Supermercado, Comparador |
| Agregar al carrito         | Usuario, Carrito, Producto     |
| Dejar reseña               | Usuario, Reseña, Producto      |
| Votar reseña               | Usuario, Reseña                |
| Ver perfil                 | Usuario                        |
| Gestionar lista de deseos  | Usuario, Producto, ListaDeseos |
| Ver ofertas                | Producto, Oferta, Supermercado |
| Recibir recomendaciones    | AsistenteIA, Usuario, Producto |
| Actualizar precios         | ScrapingService, Producto, Precio, Supermercado |
| Gestionar usuarios         | Administrador, Usuario         |
| Gestionar productos        | Administrador, Producto        |
| Gestionar reseñas          | Administrador, Reseña          |
| Generar reportes           | Administrador, Usuario, Producto |
| Configurar sistema         | Administrador                  |

---

## 5. Tareas de Implementación

### 5.1. Fase 1 - Preparación (Oct 2025)
- Crear repositorio en GitHub.  
- Definir roles del equipo y alcance.  
- Elaborar **requisitos iniciales** (requirements.md).  
- Crear **diagramas de casos de uso** (usecases.puml, .png).  

### 5.2. Fase 2 - Diseño (Oct 2025)
- Elaborar **diagrama de clases** (classes.puml, .png).  
- Definir estructura de base de datos JSON.  
- Establecer convenciones de codificación (PEP 8).  

### 5.3. Fase 3 - Implementación Inicial (Nov 2025)
- Implementar módulo de **usuarios** (registro, login).  
- Implementar **web scraping básico** de 2 supermercados.  
- Implementar **búsqueda y comparación de precios**.  
- Subir **primer prototipo funcional**.  

### 5.4. Fase 4 - Funcionalidades Avanzadas (Nov 2025)
- Implementar **reseñas y sistema de votación**.  
- Implementar **carrito de compras simulado**.  
- Implementar **lista de deseos**.  
- Implementar **ofertas y descuentos**.  
- Implementar **asistente IA básico** para sugerencias.  

### 5.5. Fase 5 - Administración y QA (Nov 2025)
- Implementar panel de **administración** (usuarios, productos, reseñas).  
- Generación de reportes.  
- Pruebas unitarias y de integración.  
- Documentar criterios de aceptación.  

### 5.6. Fase 6 - Presentación Final (Nov 2025)
- Preparar **slides de la presentación** (slides/presentation.pdf).  
- Ensayo de presentación en clase.  
- Entrega final del proyecto (26/11/2025).  

---

## 6. Cronograma (Fechas Reales)
- **8 oct 2025** → Confirmación de equipo y proyecto (README).  
- **15 oct 2025** → Documento de requisitos inicial (requirements.md).  
- **22 oct 2025** → Borrador diagrama de casos de uso.  
- **29 oct 2025** → Borrador diagrama de clases.  
- **5 nov 2025** → Mapping casos de uso → clases + plan de implementación.  
- **12 nov 2025** → Revisión por pares.  
- **19 nov 2025** → Versión final de diagramas y plan.  
- **25 nov 2025** → Subida de slides.  
- **26 nov 2025** → Presentación final.  

---

## 7. Criterios de Aceptación
- Los diagramas (clases y casos de uso) están completos y legibles.  
- Todos los requisitos funcionales principales (registro, comparación de precios, reseñas, carrito) están implementados.  
- El sistema puede extraer precios reales mediante web scraping de al menos 2 supermercados.  
- Existe documentación clara (README, requirements.md, implementation_plan.md).  
- La presentación explica el diseño y plan de implementación en máximo 12 minutos.  

---

## 8. Riesgos y Mitigaciones
- **Sitios web de supermercados cambian estructura** → Implementar scraping robusto con múltiples selectores y logs de errores.  
- **Falta de tiempo en el equipo** → Priorizar funciones críticas (scraping, comparación, registro, carrito).  
- **Problemas de integración** → Pruebas incrementales y commits frecuentes.  

---

## 9. Próximos Pasos
- Completar diagramas UML.  
- Avanzar en implementación inicial.  
- Preparar presentación.  
- Documentar feedback recibido en revisión por pares.  

---

