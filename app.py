"""Flask app for Cupcakes"""

from flask import Flask, render_template, request, redirect, jsonify
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///cupcakes"
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'sage123'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
app.app_context().push()


@app.route("/")
def view_index():
    return render_template("index.html")


@app.route("/api/cupcakes", methods=['GET'])
def return_all_cupcakes():
    """returns all cupcakes in the database"""

    cupcakes = Cupcake.query.all()
    serialized = [serialize_cupcake(cupcake) for cupcake in cupcakes]

    return jsonify(cupcakes=serialized)


@app.route("/api/cupcakes/<int:cupcake_id>", methods=['GET'])
def return_one_cupcake(cupcake_id):
    """returns a specific cupcake in the database"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = serialize_cupcake(cupcake)

    return jsonify(cupcake=serialized)


@app.route("/api/cupcakes", methods=['POST'])
def add_cupcake():
    """add a new cupcake to the database"""

    data = request.get_json()

    flavor = data.get("flavor")
    size = data.get("size")
    rating = data.get("rating")
    image = data.get("image", 'https://tinyurl.com/demo-cupcake')
    

    cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    db.session.add(cupcake)
    db.session.commit()

    return (jsonify(cupcake=serialize_cupcake(cupcake)), 201 )


@app.route("/api/cupcakes/<int:cupcake_id>", methods=['PATCH'])
def update_cupcake(cupcake_id):
    """add a new cupcake to the database"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.query(Cupcake).filter_by(id=cupcake_id).update(request.json)
    
    db.session.commit()

    return jsonify(cupcake=serialize_cupcake(cupcake))


@app.route("/api/cupcakes/<int:cupcake_id>", methods=['DELETE'])
def delete_cupcake(cupcake_id):
    """delete a cupcake"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    message = {"message": f"deleted cupcake with id:{cupcake.id}"}
    db.session.query(Cupcake).filter_by(id=cupcake_id).delete()
    
    db.session.commit()

    return jsonify(message)


def serialize_cupcake(cupcake):
    """serialize cupcake SQLAchemy object to json"""

    return {
        'id': cupcake.id,
        'flavor': cupcake.flavor,
        'size': cupcake.size,
        'rating': cupcake.rating,
        'image': cupcake.image
    }