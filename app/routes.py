from .import db
from flask import current_app as app, render_template, request, redirect, url_for, flash, session
from app.models import Post
from app.blueprints.authentication.models import User
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse



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