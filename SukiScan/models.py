from SukiScan import db

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    
    def get_id(self, UserMixin):
        return str(self.user_id)
    
    def __repr__(self):
        return f"<User {self.username}"