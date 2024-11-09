from app import create_app
from app.models import create_db

app = create_app()

# Crear la base de datos si no existe
with app.app_context():
    create_db()

if __name__ == "__main__":
    app.run(debug=True)
