from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class ForumPostForm(FlaskForm):
    title = StringField(
        'Post Title',
        validators=[DataRequired(message="Title is required."), Length(max=120)]
    )
    content = TextAreaField(
        'Content',
        validators=[DataRequired(message="Content cannot be empty.")]
    )
    submit = SubmitField('Submit Post')

class ForumCommentForm(FlaskForm):
    content = TextAreaField(
        'Comment',
        validators=[DataRequired(message="Comment cannot be empty.")]
    )
    submit = SubmitField('Submit Comment')
