document.addEventListener('DOMContentLoaded', function() {
    // Solo se ejecuta si estamos en la página de creación de compra
    if (document.getElementById('compraForm')) {
        const detalleBody = document.getElementById('detalleBody');
        const detalleTemplate = document.getElementById('detalleTemplate');
        const btnAgregar = document.getElementById('btnAgregarProducto');
        
        // Función para agregar nueva fila
        function agregarFila() {
            const nuevaFila = detalleTemplate.content.cloneNode(true);
            detalleBody.appendChild(nuevaFila);
            
            // Configurar eventos para la nueva fila
            const fila = detalleBody.lastElementChild;
            const productoSelect = fila.querySelector('.producto-select');
            const cantidadInput = fila.querySelector('.cantidad');
            const costoInput = fila.querySelector('.costo');
            const btnEliminar = fila.querySelector('.btn-eliminar');
            
            // Evento para cargar precio al seleccionar producto
            if (productoSelect) {
                productoSelect.addEventListener('change', function() {
                    const precio = this.options[this.selectedIndex]?.dataset.precio || 0;
                    if (costoInput) costoInput.value = precio;
                    calcularSubtotal(fila);
                });
            }
            
            // Eventos para calcular subtotal
            if (cantidadInput) cantidadInput.addEventListener('input', () => calcularSubtotal(fila));
            if (costoInput) costoInput.addEventListener('input', () => calcularSubtotal(fila));
            
            // Evento para eliminar fila
            if (btnEliminar) {
                btnEliminar.addEventListener('click', function() {
                    fila.remove();
                    calcularTotales();
                });
            }
            
            calcularTotales();
        }
        
        // Calcular subtotal por fila
        function calcularSubtotal(fila) {
            const cantidadInput = fila.querySelector('.cantidad');
            const costoInput = fila.querySelector('.costo');
            const subtotalItem = fila.querySelector('.subtotal-item');
            
            if (!cantidadInput || !costoInput || !subtotalItem) return;
            
            const cantidad = parseFloat(cantidadInput.value) || 0;
            const costo = parseFloat(costoInput.value) || 0;
            const subtotal = cantidad * costo;
            
            subtotalItem.textContent = subtotal.toFixed(2);
            calcularTotales();
        }
        
        // Calcular totales generales
        function calcularTotales() {
            let subtotal = 0;
            document.querySelectorAll('.subtotal-item').forEach(item => {
                subtotal += parseFloat(item.textContent) || 0;
            });
            
            const descuentoInput = document.getElementById('descuento');
            const descuento = descuentoInput ? parseFloat(descuentoInput.value) || 0 : 0;
            const total = subtotal - descuento;
            
            const subtotalElement = document.getElementById('subtotal');
            const totalElement = document.getElementById('total');
            
            if (subtotalElement) subtotalElement.textContent = subtotal.toFixed(2);
            if (totalElement) totalElement.textContent = total.toFixed(2);
        }
        
        // Evento para descuento
        const descuentoInput = document.getElementById('descuento');
        if (descuentoInput) {
            descuentoInput.addEventListener('input', calcularTotales);
        }
        
        // Evento para agregar producto
        if (btnAgregar) {
            btnAgregar.addEventListener('click', agregarFila);
        }
        
        // Agregar primera fila al cargar
        agregarFila();
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('compraForm');
    
    form.addEventListener('submit', function(e) {
        let isValid = true;
        
        // Validar laboratorio
        if (!form.laboratorio_id.value) {
            alert('Seleccione un laboratorio');
            isValid = false;
        }
        
        // Validar detalles
        const productos = document.querySelectorAll('select.producto-select');
        if (productos.length === 0) {
            alert('Debe agregar al menos un producto');
            isValid = false;
        }
        
        productos.forEach((select, index) => {
            if (!select.value) {
                alert(`Fila ${index + 1}: Seleccione un producto`);
                isValid = false;
            }
            
            const cantidad = select.closest('tr').querySelector('.cantidad');
            if (!cantidad.value || parseInt(cantidad.value) < 1) {
                alert(`Fila ${index + 1}: Cantidad inválida`);
                isValid = false;
            }
            
            const costo = select.closest('tr').querySelector('.costo');
            if (!costo.value || parseFloat(costo.value) <= 0) {
                alert(`Fila ${index + 1}: Costo inválido`);
                isValid = false;
            }
        });
        
        if (!isValid) {
            e.preventDefault();
        }
    });
});