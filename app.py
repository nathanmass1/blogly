"""Blogly application."""
from flask import Flask, request, render_template, redirect, flash, session
from models import db, connect_db, User
# from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "Secret_key"

connect_db(app)
db.create_all()

# debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


@app.route("/")
def home_page():

    return redirect("/users")


@app.route("/users")
def user_page():

    users = User.query.order_by('last_name')
    print("TESTTTT")
    print("User Query is", User.query)

    return render_template("users.html", users=users)


@app.route("/users/new")
def new_user_page():

    return render_template("add_user.html")


@app.route("/users",  methods=["POST"])
def create_user():

    first_name = request.form.get("first_name", "")
    last_name = request.form.get("last_name", "")
    image_url = request.form.get("image_url", "")
    # print(first_name, last_name, image_url)
    # print("LOOK AT ME")
    user = User(first_name=first_name,
                last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<id>")
def get_user(id):

    user = User.query.get(id)
   #  print(id)
   #  print("LOOK AT ME")
   #  first_name = user.first_name
   #  last_name = user.last_name
    image_url = user.image_url

    return render_template("profile.html", user=user, image_url=image_url, id=id)


@app.route("/users/<id>/edit")
def edit_user(id):
    print("TEST", id)
    return render_template("edit_user.html", id=id)


@app.route("/users/<id>/edit", methods=["POST"])
def edit_user_submit(id):

    first_name = request.form.get("first_name", "")
    last_name = request.form.get("last_name", "")
    image_url = request.form.get("image_url", "")

    # user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    user = User.query.get(id)
    user.first_name = first_name
    user.last_name = last_name
    user.last_Name = image_url

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<id>/delete", methods=["POST"])
def delete_user(id):

    # first_name = request.form.get("first_name", "")
    # last_name = request.form.get("last_name", "")
    # image_url = request.form.get("image_url", "")

    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")
