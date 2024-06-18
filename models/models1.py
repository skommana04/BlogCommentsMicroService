from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from extensions import db

class BlogPost(db.Model):
    __tablename__ = 'blog_posts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.Text)
    content = db.Column(db.Text, nullable=False)
    posted_by = db.Column(db.String(255))

    likes = db.relationship('Like', back_populates='post', lazy='dynamic')
    comments = db.relationship('Comment', back_populates='post', lazy='dynamic')

class Like(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id'), nullable=False)
    user_name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    post = db.relationship('BlogPost', back_populates='likes')

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id'), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    post = db.relationship('BlogPost', back_populates='comments')
