from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from .extensions import db
from .models import Usuario,Imagen, Enfermedad
from PIL import Image  # Usar Pillow para procesar la imagen
from flask_login import login_required

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    return render_template('index.html')
@bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['image']
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join('app/static/uploads', filename)
            file.save(file_path)
            
            # Lógica para detectar enfermedad (simulada)
            resultado = detectar_enfermedad(file_path)  # Reemplazar con función real
            flash(f"Resultado: {resultado}")
            
            return redirect(url_for('routes.index'))
    
    return render_template('upload.html')

def detectar_enfermedad(image_path):
    # Implementa la lógica de ML aquí
    # Simulación: Retorna una enfermedad ficticia
    return "Enfermedad Detectada"
