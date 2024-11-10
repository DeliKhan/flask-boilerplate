from flask import abort, Blueprint
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.menu import MenuLink
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

db = SQLAlchemy()
    
class UserSecurityQuestions(db.Model):
    username = db.Column(db.String(1), nullable=False, primary_key=True)
    questionid = db.Column(db.Integer(2), nullable=False, primary_key=True)
    question = db.Column(db.String(255), nullable=False)

    def __init__(self, username, questionid, question):
        self.username = username
        self.questionid = questionid
        self.question = question

    def __repr__(self):
        return f"<UserSecurityQuestions {self.username} - {self.questionid}>"
    
class FollowRequest(db.Model):
    username = db.Column(db.String(1), primary_key=True)
    followerusername = db.Column(db.String(1), primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.String(100), nullable=False)

    def __init__(self, username, followerusername, question, answer):
        self.username = username
        self.followerusername = followerusername
        self.question = question
        self.answer = answer

    def __repr__(self):
        return f"<FollowRequest {self.username} -> {self.followerusername}>"
    
# FLASK_ADMIN CONFIGURATION
class DefaultModelView(ModelView):
    restricted = True

    def __init__(self, model, session, name=None, category=None, endpoint=None, url=None, **kwargs):
        self.column_default_sort = ('id', True)
        super(DefaultModelView, self).__init__(model, session, name=name, category=category, endpoint=endpoint, url=url)

    def is_accessible(self):
        return current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        abort(401)
# ---------------------------------------------------------------------------- #