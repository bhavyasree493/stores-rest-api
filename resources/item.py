from flask_restful import  Resource,reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    # This parser.add_argument part added to make sure that only required arguments 'price -here' are passed in the payload
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This filed cannotbe empty!!'
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help='Every item needs a store id.'
                        )


    @jwt_required()                             # So where ever we place this(post, dlete) decorator, it will provide authorization
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404


    def post(self, name):
        if ItemModel.find_by_name(name):
            return f"An item with name: {name} already exists", 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)                                  #item = ItemModel(name, data['price'], data['store_id'])
        try:
            item.save_to_db()
        except:
            return {'message': 'An error occured during insteting item.'},500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, **data)                          #item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price= data['price']

        item.save_to_db()

        return item.json()

class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}                   # or {'items': list(map(lambda x: x.json()  ,ItemModel.query.all()))}
