from app import db, create_app, cli
from app.blueprints.authentication.models import User
from app.blueprints.blog.models import Post
from app.blueprints.shop.models import Product, Order, OrderDetails, Cart, Customer

app = create_app()
cli.register(app)

@app.shell_context_processor
def shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Product': Product, 'Customer': Customer, 'Order': Order, 'OrderDetails': OrderDetails, 'Cart': Cart}