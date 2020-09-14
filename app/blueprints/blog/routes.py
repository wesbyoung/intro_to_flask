from .import bp as blog
from flask import request,  url_for, redirect, flash, render_template
from app import db
from app.blueprints.blog.models import Post
from app.blueprints.authentication.models import User
from flask_login import current_user, login_required

@blog.route('/create-post', methods=['POST'])
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
    return redirect(url_for('main.index'))
    
@blog.route('/blog')
@login_required
def get_post():
    _id = request.args.get('id')
    p = Post.query.get(_id)
    return render_template('post-single.html', post=p)


@blog.route('/users/follow')
@login_required
def follow():
    _id = request.args.get('id')
    user = User.query.get(_id)
    current_user.follow(user)
    db.session.commit()
    flash(f'You are now following {user.first_name} {user.last_name}', 'success')
    return redirect(url_for('blog.users'))

@blog.route('/users/unfollow')
@login_required
def unfollow():
    _id = request.args.get('id')
    user = User.query.get(_id)
    current_user.unfollow(user)
    db.session.commit()
    flash(f'You have unfollowed {user.first_name} {user.last_name}', 'danger')
    return redirect(url_for('blog.users'))

@blog.route('/users')
@login_required
def users():
    return render_template('users.html', users=User.query.all())