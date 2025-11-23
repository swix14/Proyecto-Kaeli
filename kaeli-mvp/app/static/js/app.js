document.addEventListener("DOMContentLoaded", () => {
  loadAllProducts();
});

function extractPrice(info) {
  if (info == null) return null;
  if (typeof info === "number") return info;
  if (typeof info === "object") {
    if (typeof info.precio === "number") return info.precio;
    if (typeof info.precio_min === "number") return info.precio_min;
    const firstNumeric = Object.values(info).find(v => typeof v === "number");
    return typeof firstNumeric === "number" ? firstNumeric : null;
  }
  return null;
}

function formatPrice(n) {
  if (typeof n !== "number") return "N/D";
  return `$${n.toLocaleString("es-CL")}`;
}

async function loadAllProducts(){
  const resultsGrid = document.getElementById("results-grid");
  resultsGrid.innerHTML = "<p>Cargando productos...</p>";

  try {
    const res = await fetch("/api/productos");
    const data = await res.json();

    resultsGrid.innerHTML = "";
    Object.entries(data).forEach(([key, producto]) => {
      const precios = Object.values(producto.precios)
        .map(extractPrice)
        .filter(p => typeof p === "number");

      const precioMin = precios.length ? Math.min(...precios) : null;

      const card = document.createElement("div");
      card.className = "product-card";
      card.innerHTML = `
        <h3>${producto.nombre_generico}</h3>
        <p>Desde ${formatPrice(precioMin)}</p>
        <a href="/detalle/${key}">Ver detalle</a>
      `;
      resultsGrid.appendChild(card);
    });
  } catch(err){
    resultsGrid.innerHTML = "<p>Error al cargar productos.</p>";
    console.error(err);
  }
}
