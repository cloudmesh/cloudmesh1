"""

terminal 1>

    fab manage.mongo

terimal 2>

     cd cloudmesh_web python a.py

view:

     http://127.0.0.1:5000/post

"""
from flask.ext.mongoengine.wtf import model_form
from mongoengine import connect
from mongoengine import *
from flask import Flask, current_app, request, session, Flask, render_template

db = connect('tttt', port=27777)


class User(Document):
    email = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)

# class Content(EmbeddedDocument):
#    class Meta:
#        csrf = False
#            text = StringField()
#    lang = StringField(max_length=3)
#    gregor = StringField()


class Post(Document):
    title = StringField(max_length=120, required=True)
    author = ReferenceField(User)
    tags = ListField(StringField(max_length=30))
#    content = EmbeddedDocumentField(Content)
    lang = StringField(max_length=3)
    gregor = StringField()

PostForm = model_form(Post)


DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config["SECRET_KEY"] = "notsosecret"
app.debug = DEBUG


@app.route('/post', methods=['POST', 'GET'])
def add_post():

    form = PostForm(request.form)
    print request.method
    if request.method == 'POST':  # and form.validate():
        data = dict(request.form)
        for key in data:
            data[key] = data[key][0]

        print data
        # demonstrate accessing an add value
        print data['tags-add']
        print 70 * "="

    return render_template('post.html',
                           fields=[
                               'title', 'author', 'tags', 'lang', 'gregor'],
                           form=form, states=["submit"])

if __name__ == "__main__":
    app.run()
