from app import app, db
from app.forms import LoginForm, RegisterForm, PostForm
from app.models import Post, User
from flask import render_template, url_for, redirect
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = PostForm()
    posts = Post.query.order_by(Post.id).all()

    if form.validate_on_submit():

        post = Post.query.filter_by(title=form.title.data)
        if post is None:
            post = Post(
                title=form.title.data, 
                body=form.body.data,
                author=current_user
            )
            db.session.add(post)
            db.session.commit()
        return redirect(url_for('index'))

    return render_template(
        'index.html', form=form, posts=posts
    )

@app.route('/about')
@login_required
def about():
    return render_template('about.html', title='About')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))

    return render_template(
        'login.html', title='Log In', form=form
    )

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template(
        'register.html', title='Sign Up', form=form
    )