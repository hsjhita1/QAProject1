from flask import render_template, redirect, url_for
from application import app, db, bcrypt
from application.models import Posts, Users
from application.forms import PostForm, RegistrationForm

@app.route('/')
@app.route('/home')

def home():
    postData = Posts.query.all()
    return render_template('home.html', title='Home Page', posts=postData)

@app.route('/login')
def login():
    return render_template('login.html', title='Login Page')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pass = bcrypt.generate_password_hash(form.password.data)
        user = Users(
            user_name = form.user_name.data,
            first_name = form.first_name.data,
            last_name = form.last_name.data,
            email = form.email.data,
            password = hash_pass
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('post'))
    return render_template('register.html', title='Register Page', form = form)


@app.route('/post', methods=['GET', 'POST'])
def post():
    form = PostForm()
    if form.validate_on_submit():
        postData = Posts(
            user_name = form.user_name.data,
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