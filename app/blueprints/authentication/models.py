# from app import db, login
# from datetime import datetime
# from flask_login import UserMixin
# from werkzeug.security import generate_password_hash, check_password_hash

# followers = db.Table(
#     'followers',
#     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
#     db.Column('followed_id', db.Integer, db.ForeignKey('user.id')),
#     extend_existing=True
#     )

# class User(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String)
#     last_name = db.Column(db.String)
#     email = db.Column(db.String, unique=True)
#     password = db.Column(db.String)
#     created_on = db.Column(db.DateTime, default=datetime.utcnow)
#     posts = db.relationship('Post', backref='user', lazy=True)
#     followed = db.relationship(
#         'User', 
#         secondary=followers,
#         primaryjoin=(followers.c.follower_id == id),
#         secondaryjoin=(followers.c.followed_id == id),
#         backref=db.backref('followers', lazy='dynamic'),
#         lazy='dynamic'
#     )

#     def followed_posts(self):
#         followed_posts = Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == self.id).order_by(Post.created_on.desc())
#         my_posts = Post.query.filter_by(user_id=self.id)
#         return followed_posts.union(my_posts).order_by(Post.created_on.desc())

#     def follow(self, user):
#         if not self.is_following(user):
#             self.followed.append(user)

#     def unfollow(self, user):
#         if self.is_following(user):
#             self.followed.remove(user)

#     def is_following(self, user):
#         return self.followed.filter(followers.c.followed_id == user.id).count() > 0

#     def hash_password(self, original_password):
#         self.password = generate_password_hash(original_password)

#     def check_password(self, original_password):
#         return check_password_hash(self.password, original_password)

#     def __repr__(self):
#         return f"<User: {self.email}>"

# @login.user_loader
# def login_user(id):
#     return User.query.get(int(id))

    