document.addEventListener('DOMContentLoaded', function() {
    // Animación para círculos flotantes
    const circles = document.querySelectorAll('.floating-circle');
    
    circles.forEach(circle => {
        const randomX = (Math.random() - 0.5) * 20;
        const randomY = (Math.random() - 0.5) * 20;
        
        circle.animate(
            [
                { transform: 'translate(0, 0)' },
                { transform: `translate(${randomX}px, ${randomY}px)` },
                { transform: 'translate(0, 0)' }
            ],
            {
                duration: 15000 + Math.random() * 10000,
                iterations: Infinity,
                easing: 'ease-in-out'
            }
        );
    });
    
    // Manejo de mensajes flash
    const flashMessages = document.getElementById('flash-messages');
    if (flashMessages && flashMessages.children.length > 0) {
        setTimeout(() => {
            const alerts = flashMessages.querySelectorAll('.alert');
            alerts.forEach(alert => {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            });
        }, 5000);
    }
});