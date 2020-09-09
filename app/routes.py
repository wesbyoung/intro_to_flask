from .import app, db
from flask import render_template, request, redirect, url_for, flash
from app.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse

@app.route('/')
@login_required
def index():
    # print("Current User:", current_user)
    # print("Active User:", current_user.is_active)
    # print("Anonymous User:", current_user.is_anonymous)
    # print("Authenticated User:", current_user.is_authenticated)
    # print("ID of User:", current_user.get_id())
    if current_user.is_authenticated:
        posts = current_user.followed_posts().all()
    else:
        posts = []
    return render_template('index.html', posts=posts)

@app.route('/about')
@login_required
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

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        flash("You have logged in successfully", 'success')
        return redirect(next_page)
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    flash("You have successfully logged out", 'info')
    return redirect(url_for('login'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = {
        'id': current_user.id,
        'first_name': current_user.first_name,
        'last_name': current_user.last_name,
        'email': current_user.email
    }
    if request.method == 'POST':
        r = request.form
        u = User.query.get(user['id'])
        
        u.first_name = r.get('first_name')
        u.last_name = r.get('last_name')
        u.email = r.get('email')

        if r.get('password') != '' and r.get('confirm_password') != '':
            if r.get('password') == r.get('confirm_password'):
                u.password = r.get('password')
                u.hash_password(u.password)
        db.session.commit()
        flash('Your information has been updated successfully', 'info')
        return redirect(url_for('profile'))

    context = {
        'user': user,
        'posts': current_user.posts
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

# @app.route('/blog/<int:id>')
# @login_required
# def get_post(id):
#     p = Post.query.get(id)
#     return render_template('post-single.html', post=p)
    
@app.route('/blog')
@login_required
def get_post():
    _id = request.args.get('id')
    p = Post.query.get(_id)
    return render_template('post-single.html', post=p)

