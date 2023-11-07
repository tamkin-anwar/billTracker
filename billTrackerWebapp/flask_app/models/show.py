from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_bcrypt import Bcrypt


class Show:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.network = data['network']
        self.release_date = data['release_date']
        self.description = data['description']
        self.created_at = data['created_at']
        self.user_id = data['user_id']
        self.user = None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM shows;"
        results = connectToMySQL('shows').query_db(query)
        shows = []
        for u in results:
            shows.append( cls(u) )
        return shows

    @classmethod
    def save(cls, data):
        query = "INSERT INTO shows (title,network,release_date, description) VALUES (%(title)s,%(network)s,%(release_date)s,%(description)s);"

        result = connectToMySQL('shows').query_db(query,data)
        return result

    @classmethod
    def get_one(cls,data):
        query  = "SELECT * FROM shows WHERE id = %(id)s";
        result = connectToMySQL('shows').query_db(query,data)
        return cls(result[0])

    @classmethod
    def update(cls,data):
        query = "UPDATE shows SET title=%(title)s,network=%(network)s,release_date=%(release_date)s,description=%(description)s, updated_at=NOW() WHERE id = %(id)s;"""
        return connectToMySQL('shows').query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query  = "DELETE FROM shows WHERE id = %(id)s;"
        return connectToMySQL('shows').query_db(query,data)

    @staticmethod
    def validate_show(show):
        is_valid = True
        query = "SELECT * FROM shows WHERE title = %(title)s AND network = %(network)s AND description = %(description)s;"
        results = connectToMySQL('shows').query_db(query,show)
        if len(show['title']) < 3:
            flash("Title must be at least 3 characters","create")
            is_valid= False
        if len(show['network']) < 3:
            flash("Location must be at least 3 characters","create")
            is_valid= False
        if len(show['description']) < 3:
            flash("Description must be at least 3 characters","create")
            is_valid= False
        return is_valid


    @classmethod
    def get_all_shows_with_user(cls):
        query = "SELECT * FROM shows JOIN users ON shows.user_id = users.id;"
        results = connectToMySQL('shows').query_db(query)
        all_shows = []
        for row in results:
            one_show = cls(row)
            one_shows_user_info = {
                "id": row['users.id'], 
                "title": row['title'],
                "network": row['network'],
                "release_date": row['release_date'],
                "description": row['description'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            user = user.User(one_shows_user_info)
            one_show.user = user
            all_shows.append(one_show)
        return all_shows

