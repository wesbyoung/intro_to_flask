from app import db
from flask import current_app as app, session
from flask_login import current_user
from app.blueprints.shop.models import Customer, Cart

@app.context_processor
def cart_stuff():
    if 'cart' not in session:
        session['cart'] = {
            'items': [],
            'cart_total': 0
        }
    session['cart']['cart_total'] = 0
    for i in session['cart'].get('items'):
        session['cart']['cart_total'] += i['price']    
    return {'cart': session['cart']}

@app.context_processor
def create_customer():
    customer = Customer.query.get(current_user.id)
    if customer is None:
        new_customer = Customer(id=current_user.id, first_name=current_user.first_name, last_name=current_user.last_name, email=current_user.email)
        db.session.add(new_customer)
        db.session.commit()
        customer = new_customer
    return dict()