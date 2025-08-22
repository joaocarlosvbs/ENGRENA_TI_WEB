
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Week(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    week_number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    video_link = db.Column(db.String(200), nullable=True)
    materials_link = db.Column(db.String(200), nullable=True)
    photo_filename = db.Column(db.String(100), nullable=True)

    def __init__(self, week_number, title):
        self.week_number = week_number
        self.title = title
        self.description = "Descrição pendente..."
        self.video_link = "#"
        self.materials_link = "#"
        self.photo_filename = "default.jpg" # Uma imagem padrão