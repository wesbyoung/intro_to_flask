from .import app, db
from flask import render_template, request, redirect, url_for, flash
from app.models import User, Post
from flask_login import login_user, logout_user, current_user

@app.route('/')
def index():
    # print("Current User:", current_user)
    # print("Active User:", current_user.is_active)
    # print("Anonymous User:", current_user.is_anonymous)
    # print("Authenticated User:", current_user.is_authenticated)
    # print("ID of User:", current_user.get_id())
    if current_user.is_authenticated:
        posts = Post.query.filter_by(user_id=current_user.id).order_by(Post.created_on.desc()).all()
    else: 
        posts = []
    context = {
        'posts': posts
    }
    return render_template('index.html', **context)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        r = request.form
        if r.get('confirm_password') == r.get('password'):
            data = {
                'first_name': r.get('first_name'),
                'last_name': r.get('last_name'),
                'email': r.get('email'),
                'password': r.get('password'),
            }
            u = User(first_name=data['first_name'], last_name=data['last_name'], email=data['email'], password=data['password'])
            u.hash_password(u.password)
            db.session.add(u)
            db.session.commit()
            flash("You have registered successfully", 'primary')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        r = request.form
        user = User.query.filter_by(email=r.get('email')).first()
        if user is None or not user.check_password(r.get('password')):
            flash("You have used either an incorrect email or password", 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=r.get('remember_me'))
        flash("You have logged in successfully", 'success')
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    flash("You have successfully logged out", 'info')
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    context = {
        
    }
    return render_template('profile.html', **context)

@app.route('/create-post', methods=['POST'])
def create_post():
    if request.method == 'POST':
        r = request.form
        data = {
            'post_body': r.get('post-body'),
            'author_id': current_user.id,
        }
        p = Post(body=data['post_body'], user_id=data['author_id'])
        db.session.add(p)
        db.session.commit()
        flash("The post was created successfully", 'success')
    return redirect(url_for('index'))