# Requerimientos del Proyecto Kaeli

## 1. Introducción
Kaeli es una aplicación web chilena que permite a los usuarios explorar diversos productos de la canasta básica obtenidos directamente desde las páginas oficiales de supermercados. Los usuarios pueden comparar los distintos precios del mismo producto simultáneamente, buscar opciones alternas al producto que desean, simular compras en un carrito virtual, y recibir recomendaciones personalizadas a través de un asistente inteligente.

El sistema también cuenta con funcionalidades de administración para gestionar usuarios, reseñas y listas de productos.

---

## 2. Requerimientos Funcionales

### Gestión de Usuarios
- **RF01:** El sistema debe permitir el **registro de nuevos usuarios** mediante correo electrónico y contraseña.
- **RF02:** El sistema debe permitir a los usuarios **iniciar sesión**.
- **RF03:** El usuario debe poder **ver y editar su perfil**.
- **RF04:** El usuario debe poder **gestionar su lista de deseos**.

### Gestión de Precios
- **RF05:** El sistema debe obtener información de los precios de los productos vía web scraping.
- **RF06:** El sistema debe mostrar información de cada producto (nombre, tipo, envase, marca).
- **RF07:** El sistema debe permitir buscar productos por nombre, tipo o precios.

### Reseñas y Puntuaciones
- **RF08:** El usuario debe poder **dejar una reseña** a cada producto.
- **RF09:** El usuario debe poder votar (es útil/no es útil) en cada reseña del resto de usuarios.
- **RF10:** El sistema debe **almacenar y mostrar reseñas** asociadas a cada producto.

### Carrito de Compras (simulado)
- **RF11:** El usuario debe poder **agregar productos al carrito de compras**.
- **RF12:** El sistema debe calcular el **total de la compra**.

### Ofertas y Descuentos
- **RF13:** El sistema debe aplicar los **descuentos** de la página web de los supermercados.
- **RF14:** El sistema debe permitir **ver las ofertas vigentes** con sus fechas de inicio y fin.

### Asistente Inteligente
- **RF15:** El sistema debe generar **una lista de compras** a los usuarios según sus preferencias y presupuesto.
- **RF16:** El asistente debe **responder preguntas básicas** sobre los productos.
- **RF17:** El asistente debe permitir **analizar las preferencias** del usuario para mejorar recomendaciones.

### Administración
- **RF18:** El administrador debe poder **gestionar usuarios** (crear, editar, eliminar).
- **RF19:** El administrador debe poder **gestionar productos** (agregar, actualizar, eliminar).
- **RF20:** El administrador debe poder **gestionar reseñas** (aprobar, eliminar reportadas).
- **RF21:** El administrador debe poder **generar reportes** de actividad en la plataforma.
- **RF22:** El administrador debe poder **configurar parámetros del sistema**.

---

## 3. Requerimientos No Funcionales

### Usabilidad
- **RNF1:** La interfaz debe ser **intuitiva y fácil de usar** para cualquier usuario.
- **RNF2:** El sistema debe estar disponible en **idioma español**.

### Rendimiento
- **RNF3:** El sistema debe responder a consultas de productos en un **tiempo menor a 3 segundos**.
- **RNF4:** El sistema debe soportar al menos **100 usuarios concurrentes**.

### Seguridad
- **RNF5:** Las contraseñas deben almacenarse **encriptadas**.
- **RNF6:** Solo usuarios autenticados pueden dejar reseñas de productos.
- **RNF7:** Las sesiones deben expirar después de **30 minutos de inactividad**.

### Compatibilidad
- **RNF8:** El sistema debe ser accesible desde un **navegador web** en PC.
- **RNF9:** El sistema debe ser compatible con **Google Chrome y Mozilla Firefox**.

### Mantenibilidad
- **RNF10:** El código debe estar documentado con comentarios y seguir buenas prácticas.
- **RNF11:** El sistema debe estar diseñado en **arquitectura modular** para facilitar su expansión.

---

## 4. Restricciones
- El sistema depende de la disponibilidad de las páginas web de los supermercados para obtener la información de los productos.
- El carrito de compras es una **simulación**: no se realizan transacciones reales.
- El Asistente IA será una versión inicial basada en reglas, no un modelo avanzado de machine learning.

---

## 5. Priorización
- **Alta prioridad:** Registro, inicio de sesión, comparar productos de 2 supermercados, reseñas, integración con web scraping.
- **Media prioridad:** Carrito, ofertas, recomendaciones básicas.
- **Baja prioridad:** Configuraciones avanzadas de administrador, precios históricos de los productos mostrados en un gráfico.

---

## 6. Futuras Mejoras
- Versión **móvil** de la aplicación.
- Asistente IA con **machine learning** para recomendaciones más precisas.

---
