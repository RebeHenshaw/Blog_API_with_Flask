from flask import Flask, jsonify, request
from sqlite3 import Connection as SQLite3Connection
from datetime import datetime
from sqlalchemy import event
from sqlalchemy.engine import Engine
from flask_sqlalchemy import SQLAlchemy
import random
import custom_q
import linked_list
import hash_table
import binary_search_tree
import stack

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlitedb.file"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = 0


# configure SQLite to enforce foreign keys
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


# connects object relational mapper (ORM) with app instance
db = SQLAlchemy(app)


class User(db.Model):
    """Create table called user in the database file."""
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    posts = db.relationship("BlogPost", cascade="all, delete")


class BlogPost(db.Model):
    """Create table called blog_post in the database file."""
    __tablename__ = "blog_post"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.String(200))
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


# These are url routes to field incoming requests. When a request is made to the below urls,
# the function will run if method matches.
@app.route("/user", methods=["POST"])
def create_user():
    """
    Create a new database table entry for user with user-provided details.

    Example of request to be received in body of request: '{
    "name": "Rebe",
    "email": "rlhenshaw@yahoo.com",
    "address": "123 Test Street",
    "phone": "36098762345"
    }'.

    Return a success message.
    """
    data = request.get_json()
    new_user = User(
        name=data["name"],
        email=data["email"],
        address=data["address"],
        phone=data["phone"]
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"Message": "User created"}), 200


@app.route("/user/descending_id", methods=["GET"])
def get_all_users_descending():
    """Get a list of users by id number (pk) in descending order.
    Demonstrates practical use of a linked list."""
    users = User.query.all()
    all_users_ll = linked_list.LinkedList()

    for user in users:
        all_users_ll.insert_first(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone,
            }
        )

    return jsonify(all_users_ll.to_list()), 200


@app.route("/user/ascending_id", methods=["GET"])
def get_all_users_ascending():
    """Get a list of users by id number (pk) in ascending order.
        Demonstrates practical use of a linked list."""
    users = User.query.all()
    all_users_ll = linked_list.LinkedList()

    for user in users:
        all_users_ll.insert_last(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone,
            }
        )

    return jsonify(all_users_ll.to_list()), 200


@app.route("/user/<user_id>", methods=["GET"])
def get_one_user(user_id):
    """Get a single user's information by adding user-id into the request url."""
    users = User.query.all()
    all_users_ll = linked_list.LinkedList()

    for user in users:
        all_users_ll.insert_first(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone,
            }
        )

    user = all_users_ll.get_user_by_id(user_id)
    return jsonify(user), 200


@app.route("/user/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Delete a user from the database by id."""
    user = User.query.filter_by(id=int(user_id)).first()
    db.session.delete(user)
    db.session.commit()
    return jsonify({"deleted": user_id}), 200


@app.route("/blog_post/<user_id>", methods=["POST"])
def create_blog_post(user_id):
    """
    Create a new database table entry for blog_post with user-provided details.
    Demonstrate practical use of a hash-map.
    'Title' and 'body' come from request, user_id comes from url and date is set variable.

    Example of body of request to be received: '{
    "title": "Post 1",
    "body": "This is a test post.",

    Return a success message.
    """
    data = request.get_json()
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"message": "User doesn't exist"}), 400

    now = datetime.now()
    ht = hash_table.HashTable(10)
    ht.add_key_value("title", data["title"])
    ht.add_key_value("body", data["body"])
    ht.add_key_value("date", now)
    ht.add_key_value("user_id", user_id)

    new_blog_post = BlogPost(
        title=ht.get_value("title"),
        body=ht.get_value("body"),
        date=ht.get_value("date"),
        user_id=ht.get_value("user_id"),
    )
    db.session.add(new_blog_post)
    db.session.commit()

    return jsonify({"message": "new post created"}), 200

# routes
@app.route("/blog_post/<blog_post_id>", methods=["GET"])
def get_one_blog_post(blog_post_id):
    """
    Get one blog post by blog_post_id (pk). Demonstrate practical use of a binary search tree.
    Return post or error message
    """
    blog_posts = BlogPost.query.all()
    random.shuffle(blog_posts) # increases efficacy of binary search tree since posts are ordered by ID

    bst = binary_search_tree.BinarySearchTree()
    for post in blog_posts:
        bst.insert({
            "id": post.id,
            "title": post.title,
            "body": post.body,
            "user_id": post.user_id
        })
    post = bst.search(blog_post_id)
    if not post:
        return jsonify({"message": "Post not found"})
    return jsonify(post)


@app.route("/blog_post/numeric_body", methods=["GET"])
def get_numeric_post_bodies():
    """
    Get all entries with body converted into a numeric digit.
    Demonstrate practical use of queues.
    """
    blog_posts = BlogPost.query.all()
    q = custom_q.Queue()

    for post in blog_posts:
        q.enqueue(post)

    return_list = []

    for _ in range(len(blog_posts)):
        post = q.dequeue()
        numeric_body = 0
        for char in post.data.body:
            numeric_body += ord(char)
        post.data.body = numeric_body
        return_list.append({
            "id": post.data.id,
            "title": post.data.title,
            "body": post.data.body,
            "user_id": post.data.user_id
        })

    return jsonify(return_list)


@app.route("/blog_post/delete_last", methods=["DELETE"])
def delete_last_10():
    """Delete last 10 posts by post id (pk). Demonstrate practical use of a stack."""
    blog_posts = BlogPost.query.all()
    s = stack.Stack()

    for post in blog_posts:
        s.push(post)

    for _ in range(10):
        post_deleted = s.pop()
        db.session.delete(post_deleted.data)
        db.session.commit()

    return jsonify({"message": "success"})


if __name__ == "__main__":
    app.run(debug=True)

