from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

#database: postgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/amazon_api"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class ProductModel(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    amount = db.Column(db.Integer)

    def __init__(self, name, amount):
        self.name = name,
        self.amount = amount


    def __repr__(self):
        return f"<Product {self.name}>"

class OrderModel(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    def __init__(self, name, product_id):
        self.name = name,
        self.product_id = product_id


    def __repr__(self):
        return f"<order {self.name}>"

#show products (or add for postman)
@app.route('/products', methods=['POST', 'GET'])
def handle_product():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_product = ProductModel(name=data['name'], amount=data['amount'])
            db.session.add(new_product)
            db.session.commit()
            return {"message": f"product created successfully."}
        else:
            return {"error": "request not in JSON format"}
    elif request.method == 'GET':
        products = ProductModel.query.all()
        results = [
            {
                "name": product.name,
                "amount": product.amount
            } for product in products]

        return {"count": len(results), "products": results}

@app.route('/orders', methods=['POST', 'GET'])
def handle_orders():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_order = OrderModel(name=data['name'], product_id=data['product_id'])
            db.session.add(new_order)
            db.session.commit()
            return {"message": f"order created successfully."}
        else:
            return {"error": "not in JSON format"}

    elif request.method == 'GET':
        orders = OrderModel.query.all()
        results = [
            {
                "name": order.name,
                "product_id": order.product_id,
            } for order in orders]

        return {"count": len(results), "order": results}

@app.route('/orders/<order_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_order(order_id):
    order = OrderModel.query.get_or_404(order_id)

    if request.method == 'GET':
        response = {
            "name": order.name,
            "product_id": order.product_id
        }
        return {"message": "success", "order": response}

    elif request.method == 'PUT':
        data = request.get_json()
        order.name = data['name']
        order.product_id = data['product_id']
        db.session.add(order)
        db.session.commit()
        return {"message": f"order successfully updated"}

    elif request.method == 'DELETE':
        db.session.delete(order)
        db.session.commit()
        return {"message": f"Order successfully deleted."}

if __name__ == '__main__':
    app.run(debug=True)
