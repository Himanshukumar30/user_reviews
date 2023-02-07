from flask import Flask, render_template , redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import RegisterForm

app = Flask(__name__)
app.app_context().push() 

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///reviews_db'
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "abc123"

connect_db(app)
toolbar = DebugToolbarExtension(app)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/Register', methods=['GET', 'POST'] )
def register():
    form = RegisterForm()
    
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        password = form.password.data
        new_user = User.register(username, email, first_name, last_name, password)

        db.session.add(new_user)
        db.session.commit()
        flash('Welcome! Successfully Created Your Account!', "success")
        return redirect('/secret')
    
    return render_template('register.html', form=form)
    
    