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
               users.id user_id,
               users.username
        FROM reviews
        JOIN users ON reviews.user_id = users.id
        WHERE reviews.id = ?"""

    result = db.query(sql, [review_id])
    return result[0] if result else None

def add_review(drink, score,review, user_id):
    sql = "INSERT INTO reviews (drink, score, review, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [drink, score, review, user_id])

    
def update_review(review_id, drink, score, review):
    sql = """UPDATE reviews SET drink = ?,
                            score = ?,
                            review = ?
                        WHERE id = ?"""
    db.execute(sql, [drink,score,review,review_id])

def remove_review(review_id):
    sql = "DELETE FROM reviews WHERE id = ?"
    db.execute(sql, [review_id])