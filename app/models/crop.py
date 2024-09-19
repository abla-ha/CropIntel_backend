from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Crop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    area_size = db.Column(db.Float, nullable=False)
    number_of_sensors = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Crop {self.name}>'
