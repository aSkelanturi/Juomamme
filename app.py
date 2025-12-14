import sqlite3, secrets
from flask import Flask
from flask import abort, redirect, render_template, request, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
import db
import config
import reviews
import users

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

#Main page
@app.route("/")
def index():
    all_reviews = reviews.get_reviews()
    return render_template("index.html", all_reviews = all_reviews)

#Making new accounts
@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if len(username) < 3 or len(username) > 25:
        return "VIRHE: käyttäjätunnus tulee olla 3-25 merkkiä"
    if len(password1) < 8:
        return "VIRHE: salasanan tulee olla vähintään 8 merkkiä pitkä"
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return redirect("/")

#Login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])
        
        if not result:
            return "VIRHE: väärä tunnus tai salasana"
        
        user_id = result[0]["id"]
        password_hash = result[0]["password_hash"]
        
        if check_password_hash(password_hash, password):
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

#Logout page
@app.route("/logout")
def logout():
    require_login()
    del session["username"]
    del session["user_id"]
    return redirect("/")

#Adding new reviews
@app.route("/new_drink")
def new_drink():
    require_login()
    return render_template("new_drink.html")

@app.route("/create_drink", methods=["POST"])
def create_drink():
    require_login()
    check_csrf()
    drink = request.form["drink"]
    score = request.form["score"]
    review = request.form["review"]
    user_id = session["user_id"]

    classes = []

    drink_type = request.form["drink_type"]
    if drink_type:
        classes.append(("Juoma", drink_type))

    if len(drink) < 1 or len(drink) > 100:
        return "VIRHE: juoman nimi tulee olla 1-100 merkkiä pitkä"
    try:
        score_float = float(score)
        if score_float < 0 or score_float > 5:
            return "VIRHE: arvosanan tulee olla 0-5 välillä"
    except ValueError:
        return "VIRHE: arvosanan tulee olla numero"
    if len(review) > 4000:
        return "VIRHE: arvostelu voi olla enintään 4000 merkkiä pitkä"
    if not drink_type:
        return "VIRHE: valitse juoman tyyppi"

    reviews.add_review(drink, score, review, user_id, classes)

    return redirect("/")

#Review editing
@app.route("/edit_review/<int:review_id>")
def edit_review(review_id):
    review = reviews.get_review(review_id)
    require_login()
    if not review:
        abort(404)
    if review["user_id"] != session["user_id"]:
        abort(403)

    classes = reviews.get_classes(review_id)
    current_type = ""
    for title, value in classes:
        if title == "Juoma":
            current_type = value
            break

    return render_template("edit_review.html", review = review, current_type = current_type)

@app.route("/update_review", methods=["POST"])
def update_review():
    require_login()
    check_csrf()
    review_id = request.form["review_id"]
    drink = request.form["drink"]
    score = request.form["score"]
    review = request.form["review"]

    classes = []

    drink_type = request.form["drink_type"]
    if drink_type:
        classes.append(("Juoma", drink_type))

    if len(drink) < 1 or len(drink) > 100:
        return "VIRHE: juoman nimi tulee olla 1-100 merkkiä pitkä"
    try:
        score_float = float(score)
        if score_float < 0 or score_float > 5:
            return "VIRHE: arvosanan tulee olla 0-5 välillä"
    except ValueError:
        return "VIRHE: arvosanan tulee olla numero"
    if len(review) > 4000:
        return "VIRHE: arvostelu voi olla enintään 4000 merkkiä pitkä"
    if not drink_type:
        return "VIRHE: valitse juoman tyyppi"
    
    reviews.update_review(review_id, drink, score, review, classes)

    return redirect("/review/" + str(review_id))

#Review Deleting
@app.route("/remove_review/<int:review_id>", methods = ["GET", "POST"])
def remove_review(review_id):
    review = reviews.get_review(review_id)
    require_login()
    if not review:
        abort(404)
    if review["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_review.html", review = review)
    
    if request.method == "POST":
        check_csrf()
        if "remove" in request.form:
            reviews.remove_review(review_id)
            return redirect("/")
        else:
            return redirect("/review/" + str(review_id))
        

#Review page
@app.route("/review/<int:review_id>")
def show_review(review_id):
    review = reviews.get_review(review_id)
    if not review:
        abort(404)
    comments = reviews.get_comments(review_id)
    classes = reviews.get_classes(review_id)
    return render_template("show_review.html", review = review, comments = comments, classes = classes)

@app.route("/create_comment", methods=["POST"])
def create_comment():
    require_login()
    check_csrf()
    comment = request.form["comment"]
    review_id = request.form["review_id"]
    review = reviews.get_review(review_id)
    if not review:
        abort(403)

    if len(comment) < 1 or len(comment) > 1000:
        return "VIRHE: kommentin tulee olla 1-1000 merkkiä pitkä"

    user_id = session["user_id"]

    reviews.add_comment(review_id, user_id, comment)

    return redirect("/review/" + str(review_id))

#User page
@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    reviews = users.get_reviews(user_id)
    average_score = users.get_average_score(user_id)

    return render_template("show_user.html", user = user, reviews = reviews, average_score = average_score)

#Search page
@app.route("/find_review")
def find_reviews():
    query = request.args.get("query")
    if query:
        if len(query) > 100:
            return "VIRHE: hakusana voi olla enintään 100 merkkiä pitkä"
        results = reviews.find_reviews(query)
    else:
        query = ""
        results = []
    return render_template("find_review.html", query=query, results=results)