from app import db
from flask import request, render_template, flash, redirect, url_for
from .import bp as authentication
from app.models import User
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from .forms import ProfileForm

@authentication.route('/register', methods=['GET', 'POST'])
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
            return redirect(url_for('authentication.login'))
    return render_template('register.html')

@authentication.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        r = request.form
        user = User.query.filter_by(email=r.get('email')).first()
        if user is None or not user.check_password(r.get('password')):
            flash("You have used either an incorrect email or password", 'danger')
            return redirect(url_for('authentication.login'))
        login_user(user, remember=r.get('remember_me'))
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        flash("You have logged in successfully", 'success')
        return redirect(next_page)
    return render_template('login.html')

@authentication.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have successfully logged out", 'info')
    return redirect(url_for('authentication.login'))

@authentication.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = {
        'id': current_user.id,
        'first_name': current_user.first_name,
        'last_name': current_user.last_name,
        'email': current_user.email
    }
    # if request.method == 'POST':
    #     r = request.form
    #     u = User.query.get(user['id'])
        
    #     u.first_name = r.get('first_name')
    #     u.last_name = r.get('last_name')
    #     u.email = r.get('email')

    #     if r.get('password') != '' and r.get('confirm_password') != '':
    #         if r.get('password') == r.get('confirm_password'):
    #             u.password = r.get('password')
    #             u.hash_password(u.password)
    #     db.session.commit()
    #     flash('Your information has been updated successfully', 'info')
    #     return redirect(url_for('authentication.profile'))
    form = ProfileForm()
    form.first_name.data = user['first_name']
    form.last_name.data = user['last_name']
    form.email.data = user['email']

    if form.validate_on_submit():
        u = User.query.get(user['id'])
        
        u.first_name = request.form.get('first_name')
        u.last_name = request.form.get('last_name')
        u.email = request.form.get('email')


        if request.form.get('password') != '' and request.form.get('confirm_password') != '':
            u.password = request.form.get('password')
            u.hash_password(u.password)
        db.session.commit()
        flash('Your information has been updated successfully', 'info')
        return redirect(url_for('authentication.profile'))
    context = {
        'user': user,
        'posts': current_user.posts,
        'users': [user for user in User.query.all() if current_user != user],
        'form': form
    }
    return render_template('profile.html', **context)

@authentication.route('/users/follow')
@login_required
def follow():
    _id = request.args.get('id')
    user = User.query.get(_id)
    current_user.follow(user)
    db.session.commit()
    flash(f'You are now following {user.first_name} {user.last_name}', 'success')
    return redirect(url_for('authentication.users'))

@authentication.route('/users/unfollow')
@login_required
def unfollow():
    _id = request.args.get('id')
    user = User.query.get(_id)
    current_user.unfollow(user)
    db.session.commit()
    flash(f'You have unfollowed {user.first_name} {user.last_name}', 'danger')
    return redirect(url_for('authentication.users'))

@authentication.route('/users')
@login_required
def users():
    return render_template('users.html', users=User.query.all())