"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User table."""

    __tablename__ = "users"

    id = db.Column(db.Integer,
        primary_key=True,
        autoincrement=True)
    first_name = db.Column(db.String(50),
        nullable=False)
    last_name = db.Column(db.String(50),
        nullable=False)                 
    image_url = db.Column(db.String(100), nullable=False, default="https://store.playstation.com/store/api/chihiro/00_09_000/container/US/en/99/UP1477-CUSA07022_00-AV00000000000007//image?_version=00_09_000&platform=chihiro&w=720&h=720&bg_color=000000&opacity=100")


    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"