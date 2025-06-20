from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, FloatField, TextAreaField, SelectField, DateField,IntegerField, FieldList, FormField
from wtforms.validators import DataRequired, EqualTo,Length, NumberRange, Optional, Regexp, Email, ValidationError
from models.usuario_model import Usuario


# Validaciones para formulario login
class LoginForm(FlaskForm):
    usuario = StringField('Usuario', validators=[
        DataRequired(message="El usuario es obligatorio"),
        Length(min=3, max=20, message="El usuario debe tener entre 3-20 caracteres")
    ])
    
    password = PasswordField('Contraseña', validators=[
        DataRequired(message="La contraseña es obligatoria"),
        Length(min=5, max=40, message="La contraseña debe tener entre 6-40 caracteres")
    ])
    
    remember_me = BooleanField('Mantener sesión iniciada')

# Validaciones para formulario de la caja
class CajaForm(FlaskForm):
    descripcion = StringField('Descripción', validators=[
        DataRequired(message="La descripción es obligatoria"),
        Length(min=3, max=100, message="La descripción debe tener entre 3-100 caracteres")
    ])
    
    monto_apertura = FloatField('Monto de Apertura', validators=[
        DataRequired(message="El monto de apertura es obligatorio"),
        NumberRange(min=0, message="El monto no puede ser negativo")
    ])
 
# Validaciones para formulario categoria   
class CategoriaForm(FlaskForm):
    categoria = StringField('Nombre de la Categoría', validators=[
        DataRequired(message="El nombre de la categoría es obligatorio"),
        Length(min=3, max=50, message="El nombre debe tener entre 3-50 caracteres")
    ])
    
    descripcion = TextAreaField('Descripción', validators=[
        Length(max=200, message="La descripción no puede exceder 200 caracteres")
    ])
    
    estado = BooleanField('Categoría Activa')
    
# Validaciones para formulario clientes
class ClienteForm(FlaskForm):
    nombre = StringField('Nombre', validators=[
        DataRequired(message="El nombre es obligatorio"),
        Length(min=3, max=100, message="El nombre debe tener entre 3-100 caracteres")
    ])
    
    tipo_documento = SelectField('Tipo de Documento', choices=[
        ('', 'Seleccione tipo'),
        ('CI', 'Cédula de Identidad'),
        ('NIT', 'NIT'),
        ('Pasaporte', 'Pasaporte'),
        ('Otro', 'Otro')
    ], validators=[
        DataRequired(message="Seleccione un tipo de documento")
    ])
    
    documento = StringField('Documento', validators=[
        DataRequired(message="El documento es obligatorio"),
        Length(min=3, max=20, message="El documento debe tener entre 5-20 caracteres"),
        Regexp(r'^[a-zA-Z0-9-]+$', message="Documento solo puede contener letras, números y guiones")
    ])
    
    complemento = StringField('Complemento', validators=[
        Optional(),
        Length(max=10, message="El complemento no puede exceder 3 caracteres")
    ])
    
    telefono = StringField('Teléfono', validators=[
        DataRequired(message="El teléfono es obligatorio"),
        Length(min=5, max=15, message="El teléfono debe tener entre 7-10 caracteres"),
        Regexp(r'^[0-9+()-]+$', message="Teléfono solo puede contener números y símbolos +()-")
    ])
    
    estado = BooleanField('Estado', default=True)
    
# Validaciones para formulario compras
class CompraForm(FlaskForm):
    laboratorio_id = SelectField('Laboratorio', validators=[
        DataRequired(message="Debe seleccionar un laboratorio")
    ])
    
    fecha = DateField('Fecha', validators=[
        DataRequired(message="La fecha es obligatoria")
    ], format='%Y-%m-%d')
    
    comprobante_tipo = SelectField('Tipo de Comprobante', choices=[
        ('Factura', 'Factura'),
        ('Boleta', 'Boleta'),
        ('Ticket', 'Ticket')
    ], validators=[
        DataRequired(message="Seleccione el tipo de comprobante")
    ])
    
    comprobante_numero = StringField('Número de Comprobante', validators=[
        DataRequired(message="El número de comprobante es obligatorio")
    ])
    
    descuento = FloatField('Descuento (%)', validators=[
        NumberRange(min=0, max=100, message="El descuento debe ser entre 0-100%")
    ], default=0)
    
# Validaciones para formulario laboratorios
class LaboratorioForm(FlaskForm):
    nombre_lab = StringField('Nombre del Laboratorio*', validators=[
        DataRequired(message="El nombre es obligatorio"),
        Length(min=3, max=100, message="El nombre debe tener 3-100 caracteres"),
        Regexp(r'^[\w\sáéíóúñÁÉÍÓÚÑ.,-]+$', 
               message="Solo letras, números y signos .,- permitidos")
    ])
    
    direccion = StringField('Dirección', validators=[
        Optional(),
        Length(max=200, message="Máximo 200 caracteres"),
        Regexp(r'^[\w\sáéíóúñÁÉÍÓÚÑ#.,-]+$', 
               message="Caracteres no válidos en la dirección")
    ])
    
    responsable = StringField('Responsable', validators=[
        Optional(),
        Length(max=100, message="Máximo 100 caracteres"),
        Regexp(r'^[a-zA-ZáéíóúñÁÉÍÓÚÑ\s\'-]+$', 
               message="Solo letras y apóstrofes permitidos")
    ])
    
    telefono = StringField('Teléfono', validators=[
        Optional(),
        Length(max=20, message="Máximo 20 caracteres"),
        Regexp(r'^[0-9+()\s-]+$', 
               message="Formato inválido (solo números, +, (), -)")
    ])
    
# Validaciones para formulario usuarios
class BaseUsuarioForm(FlaskForm):
    nombres = StringField('Nombres', validators=[DataRequired()])
    apellidos = StringField('Apellidos', validators=[DataRequired()])
    carnet = StringField('Carnet', validators=[DataRequired()])
    nacimiento = DateField('Nacimiento', format='%Y-%m-%d', validators=[DataRequired()])
    telefono = StringField('Teléfono', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    usuario = StringField('Usuario', validators=[DataRequired()])
    imagen = StringField('Imagen (URL)', validators=[Optional()])
    rol_id = SelectField('Rol', coerce=int, validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[
        DataRequired(),
        Length(min=8, message="La contraseña debe tener al menos 8 caracteres")
    ])

    def validate_carnet(self, field):
        # Validación que se usará en creación y edición
        usuario_existente = Usuario.query.filter_by(carnet=field.data).first()
        if hasattr(self, 'usuario_actual') and self.usuario_actual:
            if usuario_existente and usuario_existente.id != self.usuario_actual.id:
                raise ValidationError('Este carnet ya está registrado')
        elif usuario_existente:
            raise ValidationError('Este carnet ya está registrado')

    def validate_usuario(self, field):
        usuario_existente = Usuario.query.filter_by(usuario=field.data).first()
        if hasattr(self, 'usuario_actual') and self.usuario_actual:
            if usuario_existente and usuario_existente.id != self.usuario_actual.id:
                raise ValidationError('Este usuario ya está registrado')
        elif usuario_existente:
            raise ValidationError('Este usuario ya está registrado')

    def validate_email(self, field):
        usuario_existente = Usuario.query.filter_by(email=field.data).first()
        if hasattr(self, 'usuario_actual') and self.usuario_actual:
            if usuario_existente and usuario_existente.id != self.usuario_actual.id:
                raise ValidationError('Este email ya está registrado')
        elif usuario_existente:
            raise ValidationError('Este email ya está registrado')

class UsuarioCreateForm(BaseUsuarioForm):
    confirm_password = PasswordField('Confirmar Contraseña', validators=[
        DataRequired(),
        EqualTo('password', message='Las contraseñas no coinciden')
    ])

class UsuarioEditForm(BaseUsuarioForm):
    password = PasswordField('Nueva Contraseña (dejar en blanco para no cambiar)', validators=[
        Optional(),
        Length(min=8, message="La contraseña debe tener al menos 8 caracteres")
    ])