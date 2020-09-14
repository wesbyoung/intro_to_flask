from app import db
from .import bp as main
from flask import render_template, request, redirect, url_for, flash, session
from app.blueprints.authentication.models import User
from app.blueprints.blog.models import Post
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse

@main.route('/')
@login_required
def index():
    # print("Current User:", current_user)
    # print("Active User:", current_user.is_active)
    # print("Anonymous User:", current_user.is_anonymous)
    # print("Authenticated User:", current_user.is_authenticated)
    # print("ID of User:", current_user.get_id())
    if current_user.is_authenticated:
        posts = current_user.followed_posts().all()
    else:
        posts = []
    return render_template('index.html', posts=posts)

@main.route('/about')
@login_required
def about():
    return render_template('about.html')
