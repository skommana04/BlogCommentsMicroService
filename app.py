from datetime import datetime
import os
from flask import Flask, jsonify,request, g
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_cors import CORS
from extensions import db
from models.models1 import Comment, Like
from utils.token_verification import token_required

#load_dotenv()

migrate = Migrate()


def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # It's a good practice to disable this to save resources

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from models.models1 import BlogPost,Comment
        db.create_all()


    @app.route('/')
    def index():
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return f'Comment Service is up and running as of {current_time}'

    @app.route('/api/posts/<int:post_id>/likes', methods=['POST'])
    @token_required
    def save_like(post_id):
        user_name = g.username
        like = Like(post_id=post_id, user_name=user_name)
        db.session.add(like)
        db.session.commit()
        return jsonify({'message': 'Like saved successfully'}), 201

    @app.route('/api/posts/<int:post_id>/comments', methods=['POST'])
    @token_required
    def save_comment(post_id):
        author = g.username
        content = request.json.get('content')
        comment = Comment(post_id=post_id, author=author, content=content)
        db.session.add(comment)
        db.session.commit()
        return jsonify({'message': 'Comment saved successfully'}), 201

    @app.route('/api/posts/<int:post_id>/likes/count', methods=['GET'])
    def get_all_likes_count_for_post(post_id):
        likes_count = Like.query.filter_by(post_id=post_id).count()
        return jsonify({'total_likes': likes_count})

    @app.route('/api/posts/<int:post_id>/comments', methods=['GET'])
    def get_all_comments_for_post(post_id):
        comments = Comment.query.filter_by(post_id=post_id).all()
        comments_data = [{'author': comment.author, 'content': comment.content,'created_at': comment.created_at} for comment in comments]
        return jsonify(comments_data)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', debug=False, port=5000)
