from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Food,User
from . import db
import json, requests
from nutritionix import Nutritionix


nix = Nutritionix(app_id="04b71d53", api_key="08f87b4f27027cab3c442495b012f3f4")
views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        food = request.form.get('food')

        food_search = nix.search().nxql(
        filters={
            "nf_calories": {
                "lte": 500
            },
            "nf_total_fat": {
                "lte": 500
            },
            "nf_total_carbohydrate": {
                "lte": 500
            },
            "nf_protein": {
                "lte": 500
            }
        },
        fields=[food, "item_id", "brand_name", "nf_calories", "nf_total_fat",
                "nf_protein", "nf_total_carbohydrate"],
        offset=0,
        limit=1
        ).json()

        fats = food_search['hits'][0]['fields']['nf_total_fat']
        proteins = food_search['hits'][0]['fields']['nf_protein']
        carbs = food_search['hits'][0]['fields']['nf_total_carbohydrate']
        calories = food_search['hits'][0]['fields']['nf_calories']
        
        new_food = Food(data=food, user_id=current_user.id, calories=calories,
                        protein=proteins, carbs=carbs, fats=fats, total_cals =+ calories)
        total_kals = 0 + calories
        db.session.add(new_food)
        db.session.execute("""insert into food(total_cals) select sum(calories)
            from food """)
        db.session.commit()
        flash('Food added!', category='success')

        return render_template("home.html", user=current_user, food=total_kals)

    else:
        return render_template("home.html", user=current_user, food=0)


@views.route('/delete-food', methods=['GET', 'POST'])
def delete_food():
    food = json.loads(request.data)
    foodId = food['foodId']
    food = Food.query.get(foodId)
    if food:
        if food.user_id == current_user.id:
            db.session.delete(food)
            db.session.commit()

    return jsonify({})

@views.route('/history', methods=['GET', 'POST'])
def history():
    return render_template("history.html")