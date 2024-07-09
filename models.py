"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User"""
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True)
    first_name = db.Column(db.String(30),
                           nullable=False)
    last_name = db.Column(db.String(30),
                          nullable=False)
    image_url = db.Column(db.String(),
                          nullable=False,
                          default="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Windows_10_Default_Profile_Picture.svg/512px-Windows_10_Default_Profile_Picture.svg.png?20221210150350")
    posts = db.relationship('Post', backref='user', cascade='all, delete-orphan')

class Post(db.Model):
    """Post"""
    __tablename__ = "posts"

    id = db.Column(db.Integer, 
                    primary_key=True)
    title = db.Column(db.String(50), 
                    nullable=False)
    content = db.Column(db.String(), 
                        nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tags = db.relationship('Tag', secondary='post_tags', backref='posts')
    
class Tag(db.Model):
    """Tag"""
    __tablename__ = "tags"
    id = db.Column(db.Integer,
                   primary_key=True)
    name = db.Column(db.String(50),
                     nullable=False)

class PostTag(db.Model):
    """Connects posts and tags"""
    __tablename__ = "post_tags"
    post_id = db.Column(db.Integer, 
                        db.ForeignKey("posts.id"),
                        primary_key=True)
    tag_id = db.Column(db.Integer,
                       db.ForeignKey("tags.id"),
                       primary_key=True)
    
