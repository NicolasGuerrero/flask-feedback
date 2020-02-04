from flask import Flask, redirect, render_template, request
from models import db, connect_db, User
from forms import CreateUserForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask-feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "secret"


@app.route("/")
def start():
    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register_user():
    form = CreateUserForm()

    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            password=form.password.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/secret")
    else:
        return render_template('register.html', form=form)


# @app.route("/login", methods=["GET", "POST"])
# def show_login():



@app.route("/secret", methods=["GET"])
def show_secret():

    return "You made it!"