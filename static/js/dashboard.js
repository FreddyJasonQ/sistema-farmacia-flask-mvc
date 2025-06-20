document.addEventListener('DOMContentLoaded', function() {
  // Animación para las tarjetas de estadísticas
  document.querySelectorAll('.stat-card').forEach(card => {
      card.addEventListener('mouseenter', () => {
          card.style.transform = 'scale(1.05)';
      });
      
      card.addEventListener('mouseleave', () => {
          card.style.transform = 'scale(1)';
      });
  });
  
  // Animación para las barras del gráfico
  document.querySelectorAll('.chart-bar').forEach(bar => {
      bar.addEventListener('mouseenter', () => {
          bar.style.transform = 'scaleY(1.1)';
      });
      
      bar.addEventListener('mouseleave', () => {
          bar.style.transform = 'scaleY(1)';
      });
  });
  
  // Animación para los elementos de productos
  document.querySelectorAll('.product-item').forEach(item => {
      item.addEventListener('mouseenter', () => {
          item.style.transform = 'translateX(8px)';
      });
      
      item.addEventListener('mouseleave', () => {
          item.style.transform = 'translateX(0)';
      });
  });
  
});