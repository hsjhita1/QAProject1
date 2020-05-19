from flask import render_template, redirect, url_for, request
from application import app, db, bcrypt
from application.models import Posts, Users, Games, Market, UserGames
from application.forms import PostForm, RegistrationForm, LoginForm, NewGame, UpdateAccountForm, SellItem, AddGameCol
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
@app.route('/home')
def home():
    postData = Posts.query.all()
    return render_template('home.html', title='Home Page', posts=postData)

@app.route('/market')
def market():
    marketData = Market.query.all()
    return render_template('market.html', title = 'Market', sell = marketData)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
    return render_template('login.html', title='Login Page', form = form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
@login_required
def post():
    form = PostForm()
    allgames = Games.query.all()
    gameExists = Games.query.filter_by(id = form.game.data).first()
    if form.validate_on_submit():
        postData = Posts(
            title = form.title.data,
            game = form.game.data,
            content = form.content.data,
            author = current_user
        )
        if not gameExists:
            return redirect(url_for('addgame'))   
        db.session.add(postData)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        print(form.errors)
    return render_template('post.html', title="Post", form=form, games = allgames)

@app.route('/sellgame', methods=['GET', 'POST'])
def sellgame():
    form = SellItem()
    allSell = Market.query.all()
    if form.validate_on_submit():
        sell = Market(
            game = form.game.data,
            description = form.description.data,
            price = form.price.data,
            seller = current_user.user_name
        )

        db.session.add(sell)
        db.session.commit()
        return redirect(url_for('market'))
    else:
        print(form.errors)
    return render_template('sell_item.html', title = 'Sell', sell = allSell )

@app.route('/addgame', methods=['GET', 'POST'])
@login_required
def addgame():
    form = NewGame()
    gameExists = Games.query.filter_by(game_name = form.game.data).first()
    if not gameExists:
        if form.validate_on_submit():
            gameData = Games(
                game_name = form.game.data,
                description = form.description.data
            )
            db.session.add(gameData)
            db.session.commit()
            return redirect(url_for('home'))
        else:
            print(form.errors)
    else:
        print('Game already exists')
        return redirect(url_for('home'))
    return render_template('new_game.html', title='Add Game', form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/games')
def games():
    games = Games.query.all()
    return render_template('games.html', title="Games", games = games)

@app.route('/games/<name>')
def gameName(name):
    gameID = Games.query.filter_by(game_name = name).first()
    id = gameID.id
    post = Posts.query.filter_by(game = id).all()
    return render_template('one_game.html', title = name, posts = post)

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name        
        form.email.data = current_user.email        
    return render_template('account.html', title='Update Account', form=form)


@app.route('/account/delete', methods=['GET', 'POST'])
@login_required
def account_delete():
    user = current_user.id
    account = Users.query.filter_by(id = user).first()
    posts = Posts.query.filter_by(user_id = user)
    for post in posts:
        db.session.delete(post)
    logout_user()
    db.session.delete(account)
    db.session.commit()
    return redirect(url_for('register'))

@app.route('/collection')
@login_required
def collection():
    user_name = current_user.user_name
    games = UserGames.query.filter_by(user = user_name)
    return render_template('collection.html', title='Collection', games = games)

@app.route('/addgamecol', methods=['GET', 'POST'])
@login_required
def add_collection():
    form = AddGameCol()
    allgames = Games.query.all()
    gameExists = Games.query.filter_by(id = form.game.data).first()
    if form.validate_on_submit():
        addCol = UserGames(
            game = form.game.data,
            user = current_user.user_name
        )
        if not gameExists:
            return redirect(url_for('addgame'))
        db.session.add(addCol)
        db.session.commit()
        return redirect(url_for('collection'))
    else:
        print(form.errors)
    return render_template('addcol.html', title = 'Add to Collection', form = form, games = allgames)