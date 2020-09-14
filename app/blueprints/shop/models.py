from app import db
from datetime import datetime

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    image = db.Column(db.String)
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    in_stock = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"{self.name} | {self.price}"


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    cart = db.relationship('Cart', backref='cart', lazy='dynamic')

    def to_dict(self):
        data = {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        }
        return data

    def from_dict(self, data):
        for field in ['id', 'first_name', 'last_name', 'email']:
            if field in data:
                setattr(self, field, data[field])

    def __repr__(self):
        return f"<Customer: {self.first_name} {self.last_name} | {self.email}>"


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    def __repr__(self):
        return f"<Cart: {self.customerId}, {self.product_id}>"


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)


class OrderDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer)