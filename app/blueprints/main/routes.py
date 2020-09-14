from flask import current_app as app, render_template
from flask_login import current_user, login_required

@app.route('/')
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

@app.route('/about')
@login_required
def about():
    return render_template('about.html')