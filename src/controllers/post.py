from http import HTTPStatus

from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError

from app import Post, db

app = Blueprint('post', __name__, url_prefix='/posts')


def _create_post():
    data = request.json
    # if not data or 'title' not in data or 'body' not in data or 'author_id' not in data:
    #     return {"error": "Invalid data"}, HTTPStatus.BAD_REQUEST

    post = Post(
        title=data['title'],
        body=data['body'],
        author_id=data['author_id']
    )
    try:
        db.session.add(post)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR

    return {'message': 'Post criado com sucesso'}, HTTPStatus.CREATED


def _list_posts():
    query = db.select(Post)
    posts = db.session.execute(query).scalars()

    if not posts:
        return {'message': 'No posts found'}

    return [
        {
            'id': post.id,
            'title': post.title,
            'body': post.body,
            'created': post.created,
            'author_id': post.author_id
        }
        for post in posts
    ]


@app.route('/', methods=['GET', 'POST'])
def handle_post():
    if request.method == 'POST':
        response, status_code = _create_post()
        return jsonify(response), status_code
    else:
        return {'posts': _list_posts()}


@app.route('/<int:post_id>')
def get_post(post_id):
    post = db.get_or_404(Post, post_id)
    return [
        {
            'id': post.id,
            'title': post.title,
            'body': post.body,
            'created': post.created,
            'author_id': post.author_id
        }
    ]


@app.route('/<int:post_id>', methods=['PATCH'])
def update_post(post_id):
    data = request.json
    if not data:
        return {'message': 'Invalid Data'}, HTTPStatus.BAD_REQUEST

    post = db.get_or_404(Post, post_id)

    if 'title' in data:
        post.title = data['title']
    if 'body' in data:
        post.body = data['body']
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR

    return {'message': 'Post atualizado com sucesso'}, HTTPStatus.OK


@app.route('/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = db.get_or_404(Post, post_id)
    db.session.delete(post)
    db.session.commit()
    return '', HTTPStatus.NO_CONTENT
