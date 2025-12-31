/* MODAL PRODUCTO */

function mostrarProducto(nombre, descripcion) {
    document.getElementById('modal-nombre').innerText = nombre;
    document.getElementById('modal-descripcion').innerText = descripcion || 'Sin descripción';
    document.getElementById('producto-modal').style.display = 'block';
}

function cerrarModal() {
    document.getElementById('producto-modal').style.display = 'none';
}

/* MODO OSCURO */

const btnModoOscuro = document.getElementById('modoOscuro');

// Al cargar la página, restaurar preferencia
if (localStorage.getItem('dark-mode') === 'true') {
  document.body.classList.add('dark-mode');
  if (btnModoOscuro) {
    btnModoOscuro.textContent = '☀️ Modo Claro';
  }
}

if (btnModoOscuro) {
  btnModoOscuro.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');

    const activo = document.body.classList.contains('dark-mode');
    localStorage.setItem('dark-mode', activo);

    btnModoOscuro.textContent = activo
      ? '☀️ Modo Claro'
      : '🌙 Modo Oscuro';
  });
}