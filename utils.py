from flask import current_user

def has_permission(permission_name):
    if not current_user.is_authenticated:
        return False
        
    # Usuario administrador tiene todos los permisos
    if current_user.rol and current_user.rol.tiene_permiso("Administrador"):
        return True
        
    # Verificar permiso específico
    return current_user.rol and current_user.rol.tiene_permiso(permission_name)