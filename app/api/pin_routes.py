from flask import Blueprint, request, abort, jsonify
from app.models import db, Pin
from app.forms.pin_form import PinForm
from app.forms.edit_pin_form import EditPinForm
from flask_login import current_user, login_required
from app.models.comment import Comment

pin_routes = Blueprint("pins", __name__, url_prefix="/pins")

# Get all pins
@pin_routes.route('/', methods=['GET'])
def get_all_pins():
    pins = Pin.query.all()
    return jsonify({pin.id: pin.to_dict() for pin in pins})


# Get one pin
@pin_routes.route('/<int:id>', methods=['GET'])
def get_one_pin(id):
    pin = Pin.query.get(id)
    if not pin:
        abort(404, description="Pin not found.")
    return jsonify({'pin': pin.to_dict()})


# Create a new pin
@pin_routes.route('/add', methods=['POST'])
@login_required
def create_new_pin():
    form = PinForm()
    form["csrf_token"].data = request.cookies.get("csrf_token")

    if form.validate_on_submit():
        data = form.data
        new_pin = Pin(
            user_id=current_user.id,
            title=data['title'],
            media_url=data['media_url'],
            description=data['description']
        )
        db.session.add(new_pin)
        db.session.commit()
        return jsonify(new_pin.to_dict()), 201

    return jsonify({"errors": form.errors}), 400



# Edit an existing pin
@pin_routes.route('/edit/<int:id>', methods=['PATCH'])
@login_required
def edit_pin(id):
    pin = Pin.query.get(id)
    if not pin:
        abort(404, description="Pin not found.")
    if pin.user_id != current_user.id:
        abort(403, description="Unauthorized edit attempt.")

    form = EditPinForm()
    form["csrf_token"].data = request.cookies.get("csrf_token")

    if form.validate_on_submit():
        data = form.data
        pin.title = data['title']
        pin.media_url = data['media_url']
        pin.description = data['description']
        db.session.commit()
        return jsonify(pin.to_dict())

    return jsonify({"errors": form.errors}), 400


# Delete a pin
@pin_routes.route('/delete/<int:id>', methods=['DELETE'])
@login_required
def delete_pin(id):
    pin = Pin.query.get(id)
    if not pin:
        abort(404, description="Pin not found.")
    if pin.user_id != current_user.id:
        abort(403, description="Unauthorized delete attempt.")

    db.session.delete(pin)
    db.session.commit()
    return jsonify({"status": "success", "deleted_pin": pin.to_dict()})


# Like a pin
@pin_routes.route('/<int:pin_id>/likes', methods=['POST'])
@login_required
def like_pin(pin_id):
    pin = Pin.query.get(pin_id)
    if not pin:
        abort(404, description="Pin not found.")
    current_user.like(pin)
    db.session.commit()
    return jsonify({"status": "liked", "pin_id": pin_id})


# Unlike a pin
@pin_routes.route('/<int:pin_id>/likes', methods=['DELETE'])
@login_required
def unlike_pin(pin_id):
    pin = Pin.query.get(pin_id)
    if not pin:
        abort(404, description="Pin not found.")
    current_user.unlike(pin)
    db.session.commit()
    return jsonify({"status": "unliked", "pin_id": pin_id})
