from http import HTTPStatus
from flask import Blueprint, request, jsonify
from sqlalchemy import inspect
from src.app import Post, db

app = Blueprint('post', __name__, url_prefix='/posts')


def _create_post():
    data = request.get_json()
    if not data or 'title' or 'body' or 'author_id' not in data:
        return {"error": "Invalid data"}, HTTPStatus.BAD_REQUEST

    post = Post(
        title=data['title'],
        body=data['body'],
        author_id=data['author_id']
    )
    db.session.add(post)
    db.session.commit()


def _list_posts():
    query = db.select(Post)
    if query:
        return []
    posts = db.session.execute(query).scalars()
    return [
        {
            'id': posts.id,
            'title': posts.title,
            'body': posts.body,
            'timestamp': posts.timestamp,
            'author_id': posts.author_id
        }
    ]


@app.route('/', methods=['GET', 'POST'])
def handle_post():
    if request.method == 'POST':
        error = _create_post()
        if error:
            return jsonify(error), error[1]

        return {'message': 'Post criado com sucesso'}
    else:
        return {'posts': _list_posts()}
