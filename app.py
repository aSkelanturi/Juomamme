import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import db
import config
import reviews


app = Flask(__name__)
app.secret_key = config.secret_key

#Main page
@app.route("/")
def index():
    all_reviews = reviews.get_reviews()
    return render_template("index.html", reviews = all_reviews)


#Check login
def require_login():
    if "user_id" not in session:
        abort(403)

#Making new accounts
@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"

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
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

#Logout page
@app.route("/logout")
def logout():
    del session["username"]
    del session["user_id"]
    return redirect("/")

#Adding new reviews
@app.route("/new_drink")
def new_drink():
    return render_template("new_drink.html")

@app.route("/create_drink", methods=["POST"])
def create_drink():
    drink = request.form["drink"]
    score = request.form["score"]
    review = request.form["review"]
    user_id = session["user_id"]

    reviews.add_review(drink,score,review,user_id)

    return redirect("/")

#Review editing
@app.route("/edit_review/<int:review_id>")
def edit_review(review_id):
    review = reviews.get_review(review_id)
    return render_template("edit_review.html", review = review)

@app.route("/update_review", methods=["POST"])
def update_review():
    review_id = request.form["review_id"]
    drink = request.form["drink"]
    score = request.form["score"]
    review = request.form["review"]

    reviews.update_review(review_id, drink, score, review)

    return redirect("/review/" + str(review_id))

#Review Deleting
@app.route("/remove_review/<int:review_id>", methods = ["GET", "POST"])
def remove_review(review_id):
    if request.method == "GET":
        review = reviews.get_review(review_id)
        return render_template("remove_review.html", review = review)
    
    if request.method == "POST":
        if "remove" in request.form:
            reviews.remove_review(review_id)
            return redirect("/")
        else:
            return redirect("/review/" + str(review_id))
        

#Review page
@app.route("/review/<int:review_id>")
def show_review(review_id):
    review = reviews.get_review(review_id)
    return render_template("show_review.html", review = review)

#Search page
@app.route("/find_review")
def find_chug():
    query = request.args.get("query")
    if query:
        results = reviews.find_reviews(query)
    else:
        query = ""
        results = []
    return render_template("find_review.html", query=query, results=results)