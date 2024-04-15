from FakePinterest import database, app
from FakePinterest.models import Usuario, Post
with app.app_context():
    database.create_all()