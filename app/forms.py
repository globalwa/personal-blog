from app.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError

class LoginForm(FlaskForm):
    username = StringField(
        label='Username:', validators=[DataRequired()]
    )
    password = PasswordField(
        label='Password:', validators=[DataRequired()]
    )
    submit = SubmitField(label='Log In')

class RegisterForm(FlaskForm):
    username = StringField(
        label='Username:', validators=[DataRequired(), Length(min=4, max=48)]
    )
    password = PasswordField(
        label='Password:', validators=[DataRequired(), Length(min=6, max=48)]
    )
    password_repeat = PasswordField(
        label='Repeat Password:', validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField(label='Sign Up')

    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if user is not None:
            raise ValidationError(
                message='This user already exists. Enter another nickname.'
            )

class PostForm(FlaskForm):
    title = StringField(
        label='Title:',
        validators=[DataRequired(), Length(min=4, max=64)]
    )
    body = CKEditorField(
        label='Text:',
        validators=[DataRequired()]
    )
    submit = SubmitField(label='Publish')

class CommentForm(FlaskForm):
    body = CKEditorField(
        label='Text:',
        validators=[DataRequired()]
    )
    submit = SubmitField(label='Comment')
        




