from flask_login import LoginManager

login_manager = LoginManager()

login_manager.init_app(app)

#login_manager.session_protection = "strong"

@login_manager.user_loader
def load_user(userid):
    return User.get(userid)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # login and validate the user...
        login_user(user)
        flash("Logged in successfully.")
        return redirect(request.args.get("next") or url_for("index"))
    return render_template("login.html", form=form)


@app.route("/settings")
@login_required
def settings():
    pass


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(somewhere)


@login_manager.unauthorized_handler
def unauthorized():
    # do stuff
    return a_response
