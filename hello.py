from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, InputRequired, StopValidation

from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '1004112177'

boostrap = Bootstrap(app)
moment = Moment(app)



class EmailValidator(DataRequired):
    field_flags = ('optional', )

    def __call__(self, form, field):
        if field.data != '' and '@' not in field.data:
            message = field.gettext('Please include an \'@\' in the email address. \'%s\' is missing an \'@\'.' % field.data)

            field.errors[:] = []
            raise StopValidation(message)

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = StringField('What is your UofT Email address?', validators=[EmailValidator()])
    submit = SubmitField('Submit')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        old_email = session.get('email')

        if old_name is not None and old_name != form.name.data:
            flash('Looks like you changed your name!')
        if old_email is not None and old_email != form.email.data:
            flash('Looks like you changed your email!')

        session['name'] = form.name.data
        session['email'] = form.email.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), email=session.get('email'))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name, current_time=datetime.utcnow())

if __name__ == '__main__':
    app.run(debug=True)
