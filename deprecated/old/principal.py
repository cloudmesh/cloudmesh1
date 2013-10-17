from flask import Flask, current_app, request, session
from flask.ext.login import LoginManager, login_user, logout_user, \
     login_required, current_user, UserMixin
from flask import Flask, session, redirect, url_for, abort, render_template, flash

from flask.ext.wtf import Form, validators, TextField, TextAreaField, PasswordField, SubmitField, DataRequired, ValidationError

from flask.ext.principal import Principal, Identity, AnonymousIdentity, \
     identity_changed
from flask import render_template, flash, send_from_directory

from cloudmesh.user.cm_userLDAP import cm_userLDAP

SECRET_KEY = 'development key'

app = Flask(__name__)
app.debug = True
app.secret_key = SECRET_KEY

Principal(app)

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(userid):
    # Return an instance of the User model
    return get_user_object(userid)


class UserClass(UserMixin):
     def __init__(self, name, id, active=True):
          self.name = name
          self.id = id
          self.active = active

     def is_active(self):
         return self.active

def get_user_object(userid):

     # query database (again), just so we can pass an object to the callback
     # db_check = users_collection.find_one({ 'userid' : userid })
     # UserObject = UserClass(db_check['username'], userid, active=True)
     # if userObject.id == userid:
     #     return UserObject
     # else:
     #     return None

     return UserClass('gregor', '1')

class LoginForm(Form):

    username = TextField('Username')
    password = PasswordField('Password')


    idp = cm_userLDAP ()
    idp.connect("fg-ldap", "ldap")

    user = None

    def validate(self):
        print "validate"

        self.user = self.idp.find_one({'cm_user_id': self.username.data})

        print "UUU", self.user

        # user = User.query.filter_by(
        #    username=self.username.data).first()

        if self.user is None:
            print "user is None"
            self.error = 'Unknown user'
            return False
        else:
            print "user not None"

        if self.user['cm_user_id'] != self.username.data:
            print "username invalid"
            self.error = 'Invalid username'
            return False
        else:
            print "user found"

            # if not self.user['password'] == self.password.data:

        test = self.idp.authenticate(self.username.data, self.password.data)
        if not test:
            print "password invalid"
            self.error = 'Invalid password'
            return False
        else:
            print "password found"

        return True

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # A hypothetical login form that uses Flask-WTF
    form = LoginForm()

    print "DDD", form.__dict__
    print "UUU", form.user

    if form.validate_on_submit():
        flash(u'Successfully logged in as %s' % form.username.data)
        session['user_id'] = form.user["cm_user_id"]

        return redirect(url_for('index'))

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    # Remove the user information from the session
    logout_user()

    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())

    return redirect(request.args.get('next') or '/')

if __name__ == "__main__":
    app.run()
