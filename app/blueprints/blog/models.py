from app import db
from datetime import datetime
# from app.blueprints.authentication.models import User

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime)
    user_id = db.Column(db.ForeignKey('user.id'))

    def __repr__(self):
        return f"<Post: {self.body[:20]}..."

    def to_dict(self):
        data = {
            'id': self.id,
            'body': self.body,
            'created_on': self.created_on,
            'updated_on': self.updated_on,
            'user': User.query.get(self.user_id).email
        }
        return data

    def from_dict(self, data):
        for field in ['body', 'user_id']:
            if field in data:
                if field == 'user_id':
                    user_id = User.query.filter_by(email=data[field].lower()).first().id
                    setattr(self, field, user_id)
                else:
                    setattr(self, field, data[field])