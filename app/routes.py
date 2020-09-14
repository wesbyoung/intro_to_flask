from .import db
from flask import current_app as app, render_template, request, redirect, url_for, flash, session
from app.models import Post
from app.blueprints.authentication.models import User
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse

@app.route('/users/follow')
@login_required
def follow():
    _id = request.args.get('id')
    user = User.query.get(_id)
    current_user.follow(user)
    db.session.commit()
    flash(f'You are now following {user.first_name} {user.last_name}', 'success')
    return redirect(url_for('users'))

@app.route('/users/unfollow')
@login_required
def unfollow():
    _id = request.args.get('id')
    user = User.query.get(_id)
    current_user.unfollow(user)
    db.session.commit()
    flash(f'You have unfollowed {user.first_name} {user.last_name}', 'danger')
    return redirect(url_for('users'))

@app.route('/users')
@login_required
def users():
    return render_template('users.html', users=User.query.all())

@app.context_processor
def cart_stuff():
    if 'cart' not in session:
        session['cart'] = {
            'items': [],
            'cart_total': 0
        }
    # Reset cart total to 0 before recounting price of all items in cart
    session['cart']['cart_total'] = 0
    for i in session['cart'].get('items'):
        session['cart']['cart_total'] += i['price']    
    return {'cart': session['cart']}