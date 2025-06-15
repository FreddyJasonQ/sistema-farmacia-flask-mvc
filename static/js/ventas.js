document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('ventaForm')) {
        const detalleBody = document.getElementById('detalleBody');
        const detalleTemplate = document.getElementById('detalleTemplate');
        const btnAgregar = document.getElementById('btnAgregarProducto');
        
        function agregarFila() {
            const nuevaFila = detalleTemplate.content.cloneNode(true);
            detalleBody.appendChild(nuevaFila);
            
            const fila = detalleBody.lastElementChild;
            const productoSelect = fila.querySelector('.producto-select');
            const cantidadInput = fila.querySelector('.cantidad');
            const precioInput = fila.querySelector('.precio');
            const btnEliminar = fila.querySelector('.btn-eliminar');
            
            if (productoSelect) {
                productoSelect.addEventListener('change', function() {
                    const precio = this.options[this.selectedIndex]?.dataset.precio || 0;
                    const stock = this.options[this.selectedIndex]?.dataset.stock || 0;
                    
                    if (precioInput) precioInput.value = precio;
                    if (cantidadInput) cantidadInput.max = stock;
                    
                    calcularSubtotal(fila);
                });
            }
            
            if (cantidadInput) cantidadInput.addEventListener('input', () => calcularSubtotal(fila));
            if (precioInput) precioInput.addEventListener('input', () => calcularSubtotal(fila));
            
            if (btnEliminar) {
                btnEliminar.addEventListener('click', function() {
                    fila.remove();
                    calcularTotales();
                });
            }
            
            calcularTotales();
        }
        
        function calcularSubtotal(fila) {
            const cantidad = parseFloat(fila.querySelector('.cantidad').value) || 0;
            const precio = parseFloat(fila.querySelector('.precio').value) || 0;
            const subtotal = cantidad * precio;
            fila.querySelector('.subtotal-item').textContent = subtotal.toFixed(2);
            calcularTotales();
        }
        
        function calcularTotales() {
            let total = 0;
            document.querySelectorAll('.subtotal-item').forEach(item => {
                total += parseFloat(item.textContent) || 0;
            });
            
            const descuento = parseFloat(document.getElementById('descuento').value) || 0;
            const total_neto = total - descuento;
            
            document.getElementById('total').textContent = total.toFixed(2);
            document.getElementById('total_neto').textContent = total_neto.toFixed(2);
        }
        
        document.getElementById('descuento').addEventListener('input', calcularTotales);
        btnAgregar.addEventListener('click', agregarFila);
        
        agregarFila();
    }
});