from flask import Flask
from config import Config
from .auth.routes import bp as auth_bp  # Corrección aquí: usa auth_bp en lugar de ath_bp
from .models import Usuario, Imagen, Enfermedad
from .extensions import db, migrate, login_manager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar las extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Define la función user_loader
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))  # Usa el modelo de Usuario para cargar al usuario

    # Crear las tablas de la base de datos si no existen
    with app.app_context():
        db.create_all()  # Crea todas las tablas de acuerdo a los modelos

    # Importar y registrar rutas
    from .routes import bp as main_bp
    from .auth.routes import bp as auth_bp  # Ya se ha corregido aquí
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    return app
