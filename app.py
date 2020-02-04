from flask import Flask, redirect, render_template, request, session, flash
from models import db, connect_db, User
from forms import CreateUserForm, LoginForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///flask-feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)
db.create_all()

app.config["SECRET_KEY"] = "secret"


@app.route("/")
def start():
    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = CreateUserForm()

    if form.validate_on_submit():
        new_user = User.register(
            username=form.username.data,
            pwd=form.password.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect("/secret")
    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()
    if form.validate_on_submit():

        user = User.authenticate(username=form.username.data, pwd=form.password.data)

        if user:
            # session["username'] keeps user logged in
            session["username"] = user.username
            return redirect("/secret")

        else:

            form.username.errors = ["Please try your username and password again."]

    return render_template("login.html", form=form)


@app.route("/users/<username>", methods=["GET"])
def show_user(username):

    if "username" not in session:
        flash("you must be logged in to view!")
        return redirect("/")

    user = User.query.get_or_404(username)

    return render_template("user.html", user=user)


@app.route("/logout", methods=["GET"])
def logout():
    if "username" in session:
        session.pop("username")

    return redirect("/")
