from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///videos.db'
db = SQLAlchemy(app)

class Materia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    videos = db.relationship('Video', backref='materia', lazy=True)

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    materia_id = db.Column(db.Integer, db.ForeignKey('materia.id'), nullable=False)

def create_app():
    with app.app_context():
        db.create_all()

# Rutas y funciones de la aplicación
@app.route('/')
def index():
    materias = Materia.query.all()
    return render_template('index.html', materias=materias)

@app.route('/agregar_materia', methods=['POST'])
def agregar_materia():
    nombre_materia = request.form.get('nombre_materia')
    if nombre_materia:
        nueva_materia = Materia(nombre=nombre_materia)
        db.session.add(nueva_materia)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/eliminar_materia/<int:materia_id>', methods=['GET'])
def eliminar_materia(materia_id):
    videos = Video.query.filter_by(materia_id=materia_id).all()
    for video in videos:
        db.session.delete(video)

    materia = Materia.query.get(materia_id)
    db.session.delete(materia)

    db.session.commit()
    return redirect(url_for('index'))

@app.route('/modificar_materia/<int:materia_id>', methods=['POST'])
def modificar_materia(materia_id):
    nueva_nombre = request.form.get('nueva_nombre')
    materia = Materia.query.get(materia_id)
    if materia and nueva_nombre:
        materia.nombre = nueva_nombre
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/agregar_video/<int:materia_id>', methods=['POST'])
def agregar_video(materia_id):
    titulo = request.form.get('titulo')
    url = request.form.get('url')
    if titulo and url:
        nuevo_video = Video(titulo=titulo, url=url, materia_id=materia_id)
        db.session.add(nuevo_video)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/eliminar_video/<int:video_id>', methods=['POST'])
def eliminar_video(video_id):
    materia_id = request.form.get('materia_id')
    video = Video.query.get(video_id)
    if video:
        db.session.delete(video)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    create_app()
    app.run(debug=True)

