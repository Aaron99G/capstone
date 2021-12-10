from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Food
from . import db
import json, requests
from nutritionix import Nutritionix


nix = Nutritionix(app_id="04b71d53", api_key="08f87b4f27027cab3c442495b012f3f4")
views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        food = request.get('food')

        new_food = food(data=food, user_id=current_user.id)
        db.session.add(new_food)
        db.session.commit()
        flash('Food added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-food', methods=['POST'])
def delete_food():
    food = json.loads(request.data)
    foodId = food['foodId']
    food = Food.query.get(foodId)
    if food:
        if food.user_id == current_user.id:
            db.session.delete(food)
            db.session.commit()

    return jsonify({})


def get_food(food):
    res = nix.search(food).json()
    
    return res