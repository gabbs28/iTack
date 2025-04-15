from flask import Blueprint, request, abort, jsonify
from app.models import db
from app.models.comment import Comment
from app.forms.new_comment_form import NewCommentForm
from app.forms.edit_comment_form import EditCommentForm
from flask_login import current_user

comment_routes = Blueprint('comments', __name__, url_prefix='/comments')


# Get all comments 
@comment_routes.route('/')
def get_comments():
    comments = Comment.query.all()
    return jsonify({comment.id: comment.to_dict() for comment in comments})


# Edit a single comment
@comment_routes.route('/edit/<int:comment_id>', methods=['PATCH'])
def edit_one_comment(comment_id):
    comment = Comment.query.get(comment_id)

    if not comment:
        abort(404, description="Comment not found.")
    if comment.user_id != current_user.id:
        abort(403, description="Unauthorized edit attempt.")

    form = EditCommentForm()
    form["csrf_token"].data = request.cookies.get("csrf_token")

    if form.validate_on_submit():
        comment.content = form.data['content']
        db.session.commit()
        return jsonify({"status": "success", "comment": comment.to_dict()})
    
    return jsonify({"status": "error", "errors": form.errors}), 400


# Create a new comment
@comment_routes.route('/new', methods=['POST'])
def create_new_comment():
    form = NewCommentForm()
    form["csrf_token"].data = request.cookies.get("csrf_token")

    if form.validate_on_submit():
        new_comment = Comment(
            user_id=current_user.id,
            pin_id=form.data['pin_id'],
            content=form.data['content'],
            notified=form.data['notified']
        )
        db.session.add(new_comment)
        db.session.commit()
        return jsonify({"status": "success", "comment": new_comment.to_dict()})
    
    return jsonify({"status": "error", "errors": form.errors}), 400


# Delete a comment
@comment_routes.route('/delete/<int:id>', methods=['DELETE'])
def delete_comment(id):
    comment = Comment.query.get(id)

    if not comment:
        abort(404, description="Comment not found.")
    if comment.user_id != current_user.id:
        abort(403, description="Unauthorized deletion attempt.")

    db.session.delete(comment)
    db.session.commit()
    return jsonify({"status": "success", "deleted_comment": comment.to_dict()})
