from flask import Flask,jsonify,request
from flask_pymongo import PyMongo
from bson.json_util import  dumps
from bson.objectid import ObjectId
from send import publish

app = Flask(__name__)
app.secret_key = "secretkey"
#app.config['MONGO_dbname'] = 'orders'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/pizza_house'
mongo = PyMongo(app)


@app.route('/welcome', methods=['GET'])
def welcome():
    return "Welcome to Pizza House"

@app.route('/orderR', methods=['POST'])
def add_order_rabbit_broker():
    _data = request.json
    _order = _data['order']
    publish("Order Created",_order)
    return jsonify({"message": "Order Created"})


@app.route('/order', methods = ['POST'])
def add_order():
    if request.method == 'POST':
        _data = request.json
        _order = _data['order']
        id = mongo.db.orders.insert_one({'order': _order})
        print(id.inserted_id)
        response = jsonify(f"Order Added success, OrderID :- f{id.inserted_id}")
        response.status_code = 200
        return response
    else:
        return jsonify(message="Not Allowed")


@app.route('/getorders', methods = ['GET'])
def get_orders():
    _all_orders = mongo.db.orders.find()
    _all_orders = dumps(_all_orders)
    return _all_orders


@app.route('/getorders/<order_id>', methods = ['GET'])
def get_order(order_id):
    _found_order = mongo.db.orders.find_one({"_id" : ObjectId(order_id)})
    if _found_order is None:
        return jsonify(message="Order Not Found")
    return dumps(_found_order)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105, debug = True, use_reloader = True)