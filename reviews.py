import db

def find_reviews(query):
    sql = """SELECT id, drink
            FROM reviews
            WHERE drink LIKE ?
            ORDER BY id DESC"""
    return db.query(sql, ["%" + query + "%"])