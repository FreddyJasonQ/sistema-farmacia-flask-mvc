from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Debe iniciar sesión para acceder a esta página', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def permission_required(*permission_names, require_all=False):
    """
    Decorador que verifica múltiples permisos con opción OR/AND
    Args:
        permission_names: Uno o más nombres de permisos
        require_all: True = requiere TODOS los permisos (AND)
                    False = requiere AL MENOS UN permiso (OR)
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Verificación de autenticación
            if not current_user.is_authenticated:
                flash('Debe iniciar sesión para acceder a esta página', 'warning')
                return redirect(url_for('auth.login'))
            
            # Acceso directo para administradores
            if current_user.is_admin():
                return f(*args, **kwargs)
            
            # Verificación de permisos
            has_access = False
            
            if require_all:
                # Requiere TODOS los permisos (AND)
                has_access = all(current_user.has_permission(perm) for perm in permission_names)
            else:
                # Requiere AL MENOS UN permiso (OR)
                has_access = any(current_user.has_permission(perm) for perm in permission_names)
            
            # Control de acceso
            if has_access:
                return f(*args, **kwargs)
            else:
                if len(permission_names) > 1:
                    required = " o ".join(permission_names) if not require_all else " y ".join(permission_names)
                    flash(f'Requiere permisos: {required}', 'danger')
                else:
                    flash('No tiene permisos para acceder a esta sección', 'danger')
                
                return redirect(url_for('dashboard.index'))
                
        return decorated_function
    return decorator

