"""Blogly application."""
from flask import Flask, request, render_template, redirect, flash, session
from models import db, connect_db, User, Post
import datetime
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


@app.route("/users/<user_id>")
def get_user(user_id):

    user = User.query.get(user_id)
    print("User id is", user)


    image_url = user.image_url

    posts = Post.query.filter_by(user_id=user_id).all()

    return render_template("profile.html", user=user, image_url=image_url, posts=posts,id=user.id)


@app.route("/users/<user_id>/edit")
def edit_user(user_id):
    print("TEST", user_id)
    return render_template("edit_user.html", user_id=user_id)


@app.route("/users/<user_id>/edit", methods=["POST"])
def edit_user_submit(user_id):

    first_name = request.form.get("first_name", "")
    last_name = request.form.get("last_name", "")
    image_url = request.form.get("image_url", "")

    # user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    user = User.query.get(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<user_id>/delete", methods=["POST"])
def delete_user(user_id):

    # first_name = request.form.get("first_name", "")
    # last_name = request.form.get("last_name", "")
    # image_url = request.form.get("image_url", "")

    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<user_id>/posts/new")
def new_post(user_id):

    user = User.query.get(user_id)

    return render_template("new_post.html", user=user)


@app.route("/users/<user_id>/posts", methods=["POST"])
def submit_post(user_id):

    title = request.form.get("title", "")
    content = request.form["content"]
    time = datetime.datetime.now()

    post = Post(title=title, content=content, created_at=time, user_id=user_id)
    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route("/posts/<post_id>")
def post_page(post_id):

    post = Post.query.get(post_id)

    return render_template("post_detail.html", post=post)


@app.route("/posts/<post_id>/edit")
def edit_post(post_id):
    
    post = Post.query.get(post_id)
    return render_template("post_edit.html", post=post)

@app.route("/posts/<post_id>/edit", methods=["POST"])
def submit_edit(post_id):
    
    title = request.form.get("title", "")
    content = request.form["content"]
    time = datetime.datetime.now()
    post = Post.query.get(post_id)

    post.title = title
    post.content = content
    post.created_at = time

    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post_id}")

@app.route("/posts/<post_id>/delete", methods=["POST"])
def delete_post(post_id):

    post = Post.query.get(post_id)
    user_id = post.user.id

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")