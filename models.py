from app import db
from datetime import datetime
import flask.ext.login as flask_login
from flask.ext.bcrypt import Bcrypt

class User(db.Model, flask_login.UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(20), nullable=False)

    role = db.Column(db.String(20), default="user")

    created_at = db.Column(db.DateTime, default=datetime.utcnow())

    def get_id(self):
        return self.id

    @property
    def is_admin(self):
        return self.role == 'admin'
    def set_password(self, password):
        bcrypt = Bcrypt()
        self.password = bcrypt.generate_password_hash(password, 12)
    def verify_password(self, password):
        bcrypt = Bcrypt()
        return bcrypt.check_password_hash(self.password, password)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow())
