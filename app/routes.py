import os
import uuid
from app import app, db, ckeditor
from app.forms import LoginForm, RegisterForm, PostForm
from app.models import Post, User
from flask import render_template, url_for, redirect, send_from_directory, request
from flask_login import login_user, logout_user, login_required, current_user
from flask_ckeditor import upload_success, upload_fail

@app.route('/')
@app.route('/index')
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).all()

    return render_template(
        'index.html', posts=posts
    )

@app.route('/publish', methods=['GET', 'POST'])
@login_required
def publish():
    form = PostForm()

    if form.validate_on_submit():
        post = Post.query.filter_by(title=form.title.data).first()
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
        'publish.html', title='New Post', form=form
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

@app.route('/post/<post_id>/<slug>')
def post(post_id, slug):
    post = Post.query.get(post_id)
    return render_template(
        'post.html', post=post
    )

@app.route('/files/<filename>')
def uploaded_files(filename):
    path = app.config['UPLOADED_PATH']
    return send_from_directory(path, filename)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('upload')
    extension = file.filename.split('.')[-1].lower()
    if extension not in app.config['ALLOWED_EXTENSIONS']:
        return upload_fail(message='Image only!')
    filename = uuid.uuid4().hex + '.' + extension
    file.save(os.path.join(app.config['UPLOADED_PATH'], filename))
    url = url_for('uploaded_files', filename=filename)
    return upload_success(url=url)