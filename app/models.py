import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .extensions import db  # Cambia esta línea para importar db de extensions.py
from flask import current_app

class Usuario(UserMixin, db.Model):  # Asegúrate de que la clase se llama "Usuario"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Enfermedad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)

class Imagen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ruta = db.Column(db.String(200), nullable=False)
    fecha_carga = db.Column(db.DateTime, default=db.func.current_timestamp())
    enfermedad_id = db.Column(db.Integer, db.ForeignKey('enfermedad.id'))
    enfermedad = db.relationship('Enfermedad')

# Función para crear la base de datos si no existe
def create_db():
    # Verifica si la base de datos PostgreSQL existe y, si no, crea la base de datos
    DATABASE_URL = current_app.config['SQLALCHEMY_DATABASE_URI']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    conn.autocommit = True
    cursor = conn.cursor()

    # Obtener el nombre de la base de datos
    db_name = DATABASE_URL.split('/')[-1]

    # Verificar si la base de datos existe
    cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}';")
    exists = cursor.fetchone()
    
    # Si la base de datos no existe, créala
    if not exists:
        cursor.execute(f"CREATE DATABASE {db_name};")
        print(f"Base de datos {db_name} creada exitosamente.")
    
    cursor.close()
    conn.close()

    # Crear las tablas en la base de datos
    with current_app.app_context():
        db.create_all()
