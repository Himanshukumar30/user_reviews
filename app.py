from flask import Flask, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm

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
    '''Homepage'''
    
    return render_template('index.html')

@app.route('/Register', methods=['GET', 'POST'] )
def register():
    '''Show User registration form'''
    
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
        session['user_id'] = new_user.id
        flash('Welcome! Successfully Created Your Account!', "success")
        return redirect(f'/users/{new_user.username}')
    
    return render_template('register.html', form=form)
    
    
@app.route('/login', methods = ['GET', 'POST'])
def login():
    '''Show login form'''
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome back, {user.username}!", 'primary')
            session['user_id'] = user.id
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Invalid username/password.']
    
    return render_template('login.html', form = form)

@app.route('/users/<username>')
def user_info(username):
    '''Show user details page'''
    
    user = User.query.filter_by(username = username).first()
    feedbacks = Feedback.query.filter_by(username = username)
    return render_template('user.html', user = user, feedbacks = feedbacks)

@app.route('/logout')
def logout():
    '''Logout user'''
    
    session.pop('user_id')
    flash("Goodbye!", "info")
    return redirect('/')


@app.route('/users/<username>/delete')
def delete_user(username):
    if(session['user_id']):
        user = User.query.filter_by(username = username).first()
        feedback = Feedback.query.filter_by(username = username)
        db.session.delete(user)
        db.session.commit()
        session.pop('user_id')
        flash(f'User: {username} deleted!')
    return redirect('/')

@app.route('/users/<username>/feedback/add', methods = ['GET', 'POST'])
def add_feedback(username):
    
    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(
            title=title,
            content=content,
            username=username,
        )

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    return render_template("add_feedback.html", form=form)