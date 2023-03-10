from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()




def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
    db.create_all()
    
class User(db.Model):
    '''User.'''
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    username = db.Column(db.Text, nullable=False, unique=True)
    
    password = db.Column(db.Text, nullable=False)
    
    email = db.Column(db.Text, nullable=False)
    
    first_name = db.Column(db.Text, nullable=False)
    
    last_name = db.Column(db.Text, nullable=False)
    
    @classmethod
    def register(cls, username, email, first_name, last_name, pwd):
        """Register user with hashed password & return user."""

        hashed = bcrypt.generate_password_hash(pwd)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(username=username, email=email, first_name=first_name, last_name=last_name, password=hashed_utf8)
    
    @classmethod
    def authenticate(cls, username, pwd):
        '''Authenticate user with username and password and return user'''
        
        user = User.query.filter_by(username = username).first()
        if user and bcrypt.check_password_hash(user.password, pwd):
            return user
        else:
            return False
        
        
class Feedback(db.Model):
    '''Feedback.'''
    
    __tablename__ = 'feedbacks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, db.ForeignKey('users.username'))
    
    user = db.relationship('User', backref="tweets")