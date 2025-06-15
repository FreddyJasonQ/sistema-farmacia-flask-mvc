document.addEventListener('DOMContentLoaded', function () {
    // Activar submenú si estás en la sección "Administración > Roles"
    const adminMenu = document.querySelector('#adminMenu');
    if (adminMenu && window.location.pathname.includes('/roles')) {
        const submenu = new bootstrap.Collapse(adminMenu, { toggle: false });
        submenu.show();
    }
});
