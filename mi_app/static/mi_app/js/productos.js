function mostrarProducto(nombre, descripcion) {
    document.getElementById('modal-nombre').innerText = nombre;
    document.getElementById('modal-descripcion').innerText = descripcion || 'Sin descripción';
    document.getElementById('producto-modal').style.display = 'block';
}

function cerrarModal() {
    document.getElementById('producto-modal').style.display = 'none';
}