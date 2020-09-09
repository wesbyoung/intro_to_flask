from app import db, create_app
from app.models import User, Post

app = create_app()

@app.shell_context_processor
def shell_context():
    return {'db': db, 'User': User, 'Post': Post}