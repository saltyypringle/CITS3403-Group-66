from SukiScan import db
from flask_login import UserMixin, current_user
from sqlalchemy.sql import func

class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    
    def get_id(self):
        return str(self.user_id)
    
    def __repr__(self):
        return f"<User {self.username}"

class Waifu(db.Model):
    __tablename__ = 'Waifu'
    w_char_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50), nullable=True)
    hair_colour = db.Column(db.String(50))
    height = db.Column(db.Integer)
    personality = db.Column(db.String(10))
    profession = db.Column(db.String(100))
    body_type = db.Column(db.String(50))
    
class Husbando(db.Model):
    __tablename__ = 'Husbando'
    h_char_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50), nullable=True)
    hair_colour = db.Column(db.String(50))
    height = db.Column(db.Integer)
    personality = db.Column(db.String(10))
    profession = db.Column(db.String(100))
    body_type = db.Column(db.String(50))

class Other(db.Model):
    __tablename__ = 'Other'
    o_char_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50), nullable=True)
    hair_colour = db.Column(db.String(50))
    height = db.Column(db.Integer)
    personality = db.Column(db.String(10))
    profession = db.Column(db.String(100))
    body_type = db.Column(db.String(50))
    
class WaifuCheck(db.Model):
    __tablename__ = 'Waifu_check'
    wc_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50), nullable=True)
    hair_colour = db.Column(db.String(50))  # Field name fixed
    height = db.Column(db.Integer)
    personality = db.Column(db.String(10))
    profession = db.Column(db.String(100))
    body_type = db.Column(db.String(50))
    submitted_by = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)  # Link to user_id
    submission_date = db.Column(db.DateTime, default=func.now(), nullable=False)  # Auto set current time
    status = db.Column(db.String(20), default='Pending', nullable=False)  # Default 'Pending' status
    mod_notes = db.Column(db.Text, nullable=True)  # Allow mod_notes to be NULL

    user = db.relationship('User', backref=db.backref('waifu_checks', lazy=True))

class HusbandCheck(db.Model):
    __tablename__ = 'Husbando_check'
    hc_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50), nullable=True)  # Allow last name to be nullable
    hair_colour = db.Column(db.String(50))  # Field name fixed
    height = db.Column(db.Integer)
    personality = db.Column(db.String(10))
    profession = db.Column(db.String(100))
    body_type = db.Column(db.String(50))
    submitted_by = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)  # Link to user_id
    submission_date = db.Column(db.DateTime, default=func.now(), nullable=False)  # Auto set current time
    status = db.Column(db.String(20), default='Pending', nullable=False)  # Default 'Pending' status
    mod_notes = db.Column(db.Text, nullable=True)  # Allow mod_notes to be NULL

    user = db.relationship('User', backref=db.backref('husbando_checks', lazy=True))

class OtherCheck(db.Model):
    __tablename__ = 'Other_check'
    oc_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50), nullable=True)  # Allow last name to be nullable
    hair_colour = db.Column(db.String(50))  # Field name fixed
    height = db.Column(db.Integer)
    personality = db.Column(db.String(10))
    profession = db.Column(db.String(100))
    body_type = db.Column(db.String(50))
    submitted_by = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)  # Link to user_id
    submission_date = db.Column(db.DateTime, default=func.now(), nullable=False)  # Auto set current time
    status = db.Column(db.String(20), default='Pending', nullable=False)  # Default 'Pending' status
    mod_notes = db.Column(db.Text, nullable=True)  # Allow mod_notes to be NULL

    user = db.relationship('User', backref=db.backref('other_checks', lazy=True))
