from application import db
from application.models import Posts
first_name = input("Enter first name: ")
last_name = input("Enter last name: ")
title = input("Enter post title: ")
game = input("Enter game name: ")
content = input("Enter content: ")

post1 = Posts(first_name = first_name, last_name = last_name, title = title, game = game, content = content)
db.session.add(post1)
db.session.commit()