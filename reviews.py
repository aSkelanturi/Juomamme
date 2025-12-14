import db

def find_reviews(query):
    sql = """SELECT id, drink
            FROM reviews
            WHERE drink LIKE ?
            ORDER BY id DESC"""
    return db.query(sql, ["%" + query + "%"])

def get_reviews():
    sql = """SELECT id, drink FROM reviews ORDER BY id DESC"""
    return(db.query(sql))

def get_review(review_id):
    sql = """SELECT reviews.drink,
               reviews.score,
               reviews.id,
               reviews.review,
               users.id AS user_id,
               users.username
        FROM reviews
        JOIN users ON reviews.user_id = users.id
        WHERE reviews.id = ?"""

    result = db.query(sql, [review_id])
    return result[0] if result else None

def add_review(drink, score,review, user_id, classes):
    sql = "INSERT INTO reviews (drink, score, review, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [drink, score, review, user_id])

    review_id = db.last_insert_id()

    sql = "INSERT INTO review_classes (review_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [review_id, title, value])

def get_classes(review_id):
    sql = "SELECT title, value FROM review_classes WHERE review_id = ?"
    return db.query(sql, [review_id])

    
def update_review(review_id, drink, score, review, classes):
    sql = """UPDATE reviews SET drink = ?,
                            score = ?,
                            review = ?
                            WHERE id = ?"""
    db.execute(sql, [drink,score, review, review_id,])


    sql = "DELETE FROM review_classes WHERE review_id = ?"
    db.execute(sql, [review_id])

    sql = "INSERT INTO review_classes (review_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [review_id, title, value])

def remove_review(review_id):
    sql = "DELETE FROM reviews WHERE id = ?"
    db.execute(sql, [review_id])

def add_comment(review_id, user_id, comment):
    sql = "INSERT INTO comments (review_id, user_id, comment) VALUES (?, ?, ?)"
    db.execute(sql, [review_id, user_id, comment])

def get_comments(review_id):
    sql = """SELECT comments.comment, users.id user_id, users.username
             FROM comments, users
             WHERE comments.review_id = ? AND comments.user_id = users.id
             ORDER BY comments.id DESC"""
    return db.query(sql, [review_id])