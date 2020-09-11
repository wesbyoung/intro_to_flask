from .import bp as shop
from flask import flash, request, render_template, redirect, url_for, session
from app.blueprints.shop.models import Product

@shop.route('/')
def get_products():
    if 'cart' not in session:
        session['cart'] = []
    context = {
        'products': Product.query.all()
    }
    return render_template('marketplace.html', **context)

@shop.route('/add')
def add_to_cart():
    _id = int(request.args.get('id'))
    p = Product.query.get(_id)
    item = {
        'id': p.id,
        'name': p.name,
        'price': p.price,
        'image': p.image,
        'in_stock': p.in_stock,
        'description': p.description
    }
    session['cart'].append(item)
    print(item['name'])
    flash(f'{p.name} has been added to your cart', 'success')
    return redirect(url_for('shop.get_products'))