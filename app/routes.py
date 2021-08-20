from functools import wraps
import os
import uuid

from app import app, db, ckeditor
from app.forms import LoginForm, RegisterForm, PostForm
from app.models import Post, User
from flask import render_template, url_for, redirect, send_from_directory, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from flask_ckeditor import upload_success, upload_fail

def editor_required(func):
    @wraps(func)
    def check(*args, **kwargs):
        if not current_user.is_editor:
            flash('You are not an editor!', 'alert alert-danger')
            return redirect(url_for('index'))
        return func(*args, **kwargs)
    return check

@app.route('/')
@app.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)

    return render_template(
        'index.html', posts=posts
    )

@app.route('/publish', methods=['GET', 'POST'])
@login_required
@editor_required
def publish():
    form = PostForm()

    if form.validate_on_submit():
        post = Post.query.filter_by(title=form.title.data).first()

        if post is not None:
            flash('A post with the same title already exists.', 'alert alert-danger')
            return redirect(url_for('publish'))

        post = Post(
            title=form.title.data, 
            body=form.body.data,
            author=current_user
        )
        db.session.add(post)
        db.session.commit()
        flash('The post has been successfully published!', 'alert alert-success')
        return redirect(url_for('index'))     

    return render_template(
        'publish.html', title='New Post', form=form
    )

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in.', 'alert alert-danger')
        return redirect(url_for('index'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(
                'The user probably does not exist or the entered password is incorrect!', 
                'alert alert-danger'
            )
            return redirect(url_for('login'))
        login_user(user)
        flash('You have successfully logged in.', 'alert alert-success')
        return redirect(url_for('index'))

    return render_template(
        'login.html', title='Log In', form=form
    )

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully logged out of your account.', 'alert alert-success')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash(
            'You are already registered. Please, log out if you want to create a new account.', 
            'alert alert-danger'
        )
        return redirect(url_for('index'))

    form = RegisterForm()

    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(
            'You have successfully registered! Log in to your account.', 
            'alert alert-success'
        )
        return redirect(url_for('login'))

    return render_template(
        'register.html', title='Sign Up', form=form
    )

@app.route('/post/<post_id>/<slug>')
def post(post_id, slug):
    post = Post.query.get(post_id)
    return render_template(
        'post.html', title=post.title, post=post
    )

@app.route('/files/<filename>')
def uploaded_files(filename):
    path = app.config['UPLOADED_PATH']
    return send_from_directory(path, filename)

@app.route('/upload', methods=['POST'])
@login_required
def upload():
    file = request.files.get('upload')
    extension = file.filename.split('.')[-1].lower()
    if extension not in app.config['ALLOWED_EXTENSIONS']:
        return upload_fail(message='Image only!')
    filename = uuid.uuid4().hex + '.' + extension
    file.save(os.path.join(app.config['UPLOADED_PATH'], filename))
    url = url_for('uploaded_files', filename=filename)
    return upload_success(url=url)

@app.route('/post/delete/<post_id>')
@login_required
@editor_required
def delete(post_id):
    post = Post.query.get(post_id)
    if post is None:
        flash('There is no such post!', 'alert alert-danger')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('The post has been successfully deleted.', 'alert alert-success')
    return redirect(url_for('index'))

@app.route('/post/edit/<post_id>', methods=['GET', 'POST'])
@login_required
@editor_required
def edit(post_id):
    form = PostForm()
    post = Post.query.get(post_id)

    if post is None:
        flash('There is no such post!', 'alert alert-danger')
        return redirect(url_for('index'))

    if form.validate_on_submit():
        same_post = Post.query.filter_by(title=form.title.data).first()
        
        if same_post is not None and form.title.data != post.title:
            flash('A post with the same title already exists.', 'alert alert-danger')
            return redirect(url_for('edit', post_id=post_id))

        post.title = form.title.data
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        flash('The post has been successfully edited!', 'alert alert-success')
        return redirect(url_for('post', post_id=post_id, slug=post.slugified_title))

    return render_template(
        'edit.html', title=f'Edit | {post.title}', 
        form=form, post=post
    )