from flask import Blueprint
from flask import request, render_template
from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, SelectField
from flask.ext.login import login_required

register_module = Blueprint('register_module', __name__)

class RegisterForm(Form):
    username = TextField()
    password = PasswordField()
    cloud_server = SelectField()
    def validate_on_submit(self):
        return True
    def initialize_form(self):
        self.username.data = "dummy username" # dummy username -read from session
        self.password.data = ""
        self.cloud_server.choices = choices = [('india_openstack_essex','india_openstack_essex'),('sierra_openstack_grizzly','sierra_openstack_grizzly')]


@register_module.route('/cm/register', methods=['GET', 'POST'])
def render_register():
    # A hypothetical register form that uses Flask-WTF
    
    form = RegisterForm()
    if form.validate_on_submit():
        form.error = None                
        if form.username.data is None:
            form.initialize_form()
            return render_template("register.html", form = form)
        else:
            
            return register(form);

def register(form):
    data_dict = {}
    data_dict['cloud'] = form.cloud_server.data
    data_dict['username'] = form.username.data
    data_dict['password'] = form.password.data
    return str(data_dict)
    
    
