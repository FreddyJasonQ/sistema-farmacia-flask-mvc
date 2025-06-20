from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from forms.forms import LoginForm
from models.usuario_model import Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Si el usuario ya está autenticado, redirigir al dashboard
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    form = LoginForm()  # Crear instancia del formulario
    
    if form.validate_on_submit():  # Validar en POST
        username = form.usuario.data
        password = form.password.data
        user = Usuario.query.filter_by(usuario=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('dashboard.index'))
        
        flash('Credenciales inválidas', 'danger')
    
    # En GET o si hay errores en POST
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('Sesión cerrada exitosamente', 'success')
    return redirect(url_for('auth.login'))