from flask import Blueprint, render_template, redirect, request, abort, jsonify
from app.models import db
from app.models.board import Board
from app.models.pin import Pin
from app.forms.new_board_form import NewBoardForm
from app.forms.edit_board_form import EditBoardForm
from flask_login import current_user

board_routes = Blueprint('boards', __name__, url_prefix='/boards')


# Get all boards 
@board_routes.route('/')
def get_boards():
    boards = Board.query.filter_by(user_id=current_user.id).all()
    return jsonify({board.id: board.to_dict() for board in boards})


# Get single board
@board_routes.route('/<int:id>')
def get_one_board(id):
    board = Board.query.get(id)
    if not board:
        abort(404, description="Board not found")
    if board.user_id != current_user.id:
        abort(403, description="Unauthorized access to this board.")
    return jsonify(board.to_dict())


# Delete a single board
@board_routes.route('/delete/<int:id>', methods=['DELETE'])
def delete_board(id):
    board = Board.query.get(id)
    if not board:
        abort(404, description="Board not found")
    if board.user_id != current_user.id:
        abort(403, description="Unauthorized deletion attempt.")
    
    db.session.delete(board)
    db.session.commit()
    return jsonify({"status": "success", "deleted_board": board.to_dict()})


# Create a new board
@board_routes.route('/new', methods=['POST'])
def add_new_board():
    form = NewBoardForm()
    form["csrf_token"].data = request.cookies.get("csrf_token")
    if form.validate_on_submit():
        new_board = Board(
            user_id=current_user.id,
            title=form.data['title'],
            description=form.data['description'],
            private=False
        )
        db.session.add(new_board)
        db.session.commit()
        return jsonify({"status": "success", "board": new_board.to_dict()})
    return jsonify({"status": "error", "errors": form.errors}), 400


# Edit a single board
@board_routes.route('/edit/<int:id>', methods=['PATCH'])
def edit_board(id):
    board = Board.query.get(id)
    if not board:
        abort(404, description="Board not found")
    if board.user_id != current_user.id:
        abort(403, description="Unauthorized edit attempt.")

    form = EditBoardForm()
    form["csrf_token"].data = request.cookies.get("csrf_token")
    if form.validate_on_submit():
        board.title = form.data['title']
        board.description = form.data['description']
        board.private = False
        db.session.commit()
        return jsonify({"status": "success", "board": board.to_dict()})
    return jsonify({"status": "error", "errors": form.errors}), 400


# Add a pin to a board
@board_routes.route('/add-pin-board/<int:boardid>/<int:pinid>', methods=['POST'])
def add_pin_to_board(boardid, pinid):
    board = Board.query.get(boardid)
    pin = Pin.query.get(pinid)

    if not board or not pin:
        abort(404, description="Board or Pin not found.")
    if board.user_id != current_user.id:
        abort(403, description="Unauthorized pin add attempt.")

    board.pins.append(pin)
    db.session.commit()
    return jsonify({"status": "success", "board": board.to_dict()})


# Remove a pin from a board
@board_routes.route('/remove-pin-board/<int:boardid>/<int:pinid>', methods=['POST'])
def remove_pin_from_board(boardid, pinid):
    board = Board.query.get(boardid)
    pin = Pin.query.get(pinid)

    if not board or not pin:
        abort(404, description="Board or Pin not found.")
    if board.user_id != current_user.id:
        abort(403, description="Unauthorized pin removal attempt.")

    board.pins.remove(pin)
    db.session.commit()
    return jsonify({"status": "success", "board": board.to_dict()})
