from flask import Flask, jsonify, request, abort

app = Flask(__name__)

recipes = [{
    "id": 1,
    "name":"rice",
    "description":"A carbohydrate dish prepared in various parts of the world."
    },{
    "id": 2,
    "name":"beans",
    "description":"A proteinous dish prepared in various parts of the world."
    },]

@app.route("/recipes/", methods=["GET"])
def get_recipies():
    return jsonify({"data": recipes}), 200

@app.route("/recipes/<int:recipe_id>/", methods=["GET"])
def get_recipe(recipe_id):
    recipe = next((recipe for recipe in recipes if recipe["id"]==recipe_id),
                  None)
    if not recipe:
        return jsonify({"messgae":"No recipe with this ID"}), 404
    return jsonify({"recipe": recipe})

@app.route("/recipes", methods=["POST"])
def post_recipe():
    recipe = request.get_json()
    if recipe.get('name') == None or recipe.get("description") == None:
        return jsonify(
            {"message": "both name field and description file are needed"}
            )
    new_recipe = {"id": len(recipes) + 1,
                  "name": recipe["name"],
                  "description": recipe["description"]}
    recipes.append(new_recipe)
    return jsonify(new_recipe), 201
    
@app.route("/recipes/<int:recipe_id>", methods=["PATCH"])
def update_recipe(recipe_id):
    recipe = next((recipe for recipe in recipes if recipe["id"] == recipe_id),
                  None)
    if not recipe:
        return jsonify(
            {"message":"No recipe with this ID"},
        ), 404
    
    recipe_data = request.get_json()
    if not recipe_data:
        return jsonify(
            {"message":"No change was made"}
        )
    if recipe_data.get('name'):
        recipe.update({"name":recipe_data.get("name")})

    if recipe_data.get("description"):
        recipe.update({"description":recipe_data.get("description")})
    
    
    return jsonify(
        {"message":f"the recipe with ID {recipe_id} has been updated"},
        recipes[recipe_id - 1]
    ), 200
    
@app.route("/recipes/<int:recipe_id>", methods=["DELETE"])
def delete_recipe(recipe_id):
    recipe = next((recipe for recipe in recipes if recipe["id"] == recipe_id),
                  None)
    if not recipe:
        return jsonify(
            {"message":"No change was made"}
        ), 404
    del recipes[recipe_id - 1]
    return jsonify(
        {"message":f"recipe with ID {recipe_id} has  been deleted"}
    ), 200
        
if __name__ == "__main__":
    app.run(debug=True)