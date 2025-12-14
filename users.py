import db

def get_user(user_id):
    sql = """SELECT id, username
        FROM users
        WHERE id = ?"""
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_reviews(user_id):
    sql = """SELECT id, drink FROM reviews WHERE user_id = ? ORDER BY id DESC"""
    return db.query(sql, [user_id])

def get_average_score(user_id):
    sql = """SELECT AVG(score) AS average_score, COUNT(*) AS review_count
             FROM reviews
             WHERE user_id = ?"""
    result = db.query(sql, [user_id])
    if result and result[0]["review_count"] > 0:
        return round(result[0]["average_score"], 2)
    return None