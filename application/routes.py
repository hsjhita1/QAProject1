from flask import render_template, redirect, url_for
from application import app
from application.models import Posts
from application.forms import PostForm
from application import db

@app.route('/')
@app.route('/home')

def home():
    postData = Posts.query.all()
    return render_template('home.html', title='Home Page', posts=postData)

@app.route('/login')
def login():
    return render_template('login.html', title='Login Page')

@app.route('/register')
def register():
    return render_template('register.html', title='Register Page')

@app.route('/post', methods=['GET', 'POST'])
def post():
    form = PostForm()
    if form.validate_on_submit():
        postData = Posts(
            first_name = form.first_name.data,
            last_name = form.last_name.data,
            title = form.title.data,
            game = form.game.data,
            content = form.content.data
        )

        db.session.add(postData)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        print(form.errors)
    return render_template('post.html', title="Post", form=form)