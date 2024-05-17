function redirigirARegistrarProducto() {
    window.location.href = "{% url 'registrar_productos/' %}";
}

function redirigirASolicitarProductos() {
    window.location.href = "{% url 'solicitud_almacen_central' %}";
}

function redirigirAInventario() {
    window.location.href = "{% url 'generar_reportes' %}";
}

function redirigirASolicitudAlmacen() {
    window.location.href = "{% url 'solicitud_producto' %}";
}


function mostrarRegistroPersonas() {
    window.location.href = "{% url 'registrar_persona_prototipo' %}";
}

function buscar() {
    var query = document.getElementById("entry_buscador").value;
    // Agregar código para realizar la búsqueda
}
