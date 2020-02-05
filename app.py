from flask import Flask, redirect, render_template, request, session, flash, url_for 
from models import db, connect_db, User, Feedback
from forms import CreateUserForm, LoginForm, FeedbackForm

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
        # secret no longer exists - fix this
        return redirect(url_for("show_user", username=new_user.username))
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
            # secret no longer exists - fix this
            return redirect(url_for("show_user", username=user.username))

        else:

            form.username.errors = ["Please try your username and password again."]

    return render_template("login.html", form=form)



@app.route("/logout", methods=["GET"])
def logout():
    if "username" in session:
        session.pop("username")

    return redirect("/")

# ####################################################################
# User's route
@app.route("/users/<username>", methods=["GET"])
def show_user(username):

    if "username" not in session:
        flash("you must be logged in to view!")
        return redirect("/")

    user = User.query.get_or_404(username)

    feedback = Feedback.get_user_feedback(user.username)


    return render_template("user.html", user=user, feedback=feedback)


@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """ Delete user. """
    
    user = User.query.get_or_404(username)
    
    if user.username != session["username"]:
        flash(f"you must be {user.username} to delete this account!")
    else:
        session.pop("username")
        db.session.delete(user)
        db.session.commit()

    return redirect("/")

@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_feedback(username):
    """ Add feedback """

    user = User.query.get_or_404(username)
    
    form = FeedbackForm()
    
    if user.username == session["username"]:
        if form.validate_on_submit():
            feedback = Feedback(title=form.title.data, content=form.content.data, username=user.username)
            db.session.add(feedback)
            db.session.commit()

            return redirect(url_for("show_user", username=user.username))  

    return render_template('add_feedback.html', user=user, form=form)


@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):
    """Update feedback."""
    session_username = session["username"]
    feedback = Feedback.query.get_or_404(feedback_id)

    if feedback.username == session_username:
        form = FeedbackForm(obj=feedback)
        if form.validate_on_submit():
            feedback.title = form.title.data
            feedback.content = form.content.data
            db.session.add(feedback)
            db.session.commit()
            return redirect(url_for('show_user', username=feedback.username))
        return render_template('add_feedback.html', form=form)


    flash("You're not the owner of this feedback.")
    return redirect(url_for('show_user', username=feedback.username)) 

@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Delete feedback."""
    session_username = session["username"]
    feedback = Feedback.query.get_or_404(feedback_id)
    if feedback.username == session_username:
        db.session.delete(feedback)
        db.session.commit()

    return redirect(url_for('show_user', username=feedback.username))