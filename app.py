from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, Week
import os

# --- CONFIGURAÇÃO ---
app = Flask(__name__)
app.config['SECRET_KEY'] = 'uma-chave-secreta-muito-forte'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'images', 'week_photos')

# Credenciais do Admin
ADMIN_USER = "admin"
ADMIN_PASS = "Engrena-TI@FEMA2025"

db.init_app(app)

# --- ROTAS PÚBLICAS ---
@app.route('/')
def index():
    all_weeks = Week.query.order_by(Week.week_number).all()
    return render_template('index.html', weeks=all_weeks)

# --- ROTAS DE ADMINISTRAÇÃO ---
@app.route('/login', methods=['POST'])
def login():
    if request.form['username'] == ADMIN_USER and request.form['password'] == ADMIN_PASS:
        session['logged_in'] = True
        flash('Login realizado com sucesso!', 'success')
        return redirect(url_for('admin'))
    else:
        flash('Credenciais inválidas. Tente novamente.', 'error')
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('index'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('logged_in'):
        return redirect(url_for('index'))

    if request.method == 'POST':
        # Processar a atualização dos dados
        for i in range(8): # São 8 semanas
            week_id = request.form.get(f'week_id_{i}')
            week_to_update = Week.query.get(week_id)
            
            if week_to_update:
                week_to_update.description = request.form.get(f'description_{i}')
                week_to_update.video_link = request.form.get(f'video_link_{i}')
                week_to_update.materials_link = request.form.get(f'materials_link_{i}')
                
                photo = request.files.get(f'photo_{i}')
                if photo and photo.filename != '':
                    # Salva a nova foto e atualiza o nome no banco
                    filename = f'week_{week_to_update.week_number}.' + photo.filename.rsplit('.', 1)[1].lower()
                    photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    week_to_update.photo_filename = filename
        
        db.session.commit()
        flash('Informações das semanas atualizadas com sucesso!', 'success')
        return redirect(url_for('admin'))

    # Se for GET, apenas mostra o painel
    all_weeks = Week.query.order_by(Week.week_number).all()
    return render_template('admin_dashboard.html', weeks=all_weeks)

# --- INICIALIZAÇÃO E SETUP ---
def setup_database(app_context):
    with app_context:
        db.create_all()
        # Verifica se as semanas já existem
        if Week.query.count() == 0:
            themes = [
                "Primeiros Passos na Lógica e Programação",
                "Estruturas Repetitivas e Introdução à Eletrônica",
                "Algoritmos de Organização e Estruturas de Dados",
                "Introdução à Computação Gráfica",
                "Controladores e Conectividade",
                "Visão Computacional e IA na Computação Gráfica",
                "Preparação para o Projeto Final",
                "Projeto Final e Apresentações"
            ]
            for i, theme in enumerate(themes):
                new_week = Week(week_number=i+1, title=theme)
                db.session.add(new_week)
            db.session.commit()
            print("Banco de dados inicializado com os temas das 8 semanas.")

if __name__ == '__main__':
    setup_database(app.app_context())
    app.run(debug=True)