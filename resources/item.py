from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, request
from models.item import ItemModel

# api works with resources and every resource has to be a class.
class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    # Whenever we create an item model, we are going to pass 
    # in the store_id. There here in the post we are creating
    # a new item. The data that is parsed from the parse args
    # method is now going to contain a stor_id that we need to
    # pass in. Similarly in the put method.
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item need a store id."
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        else:
            return {'message': "Item not found"}, 404

    def post(self, name):
        # you can use Item.find_by_name()
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()
        # **data = data['price'], data['store_id']
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            # 500 means internal server error
            return {"message": "An error occurred inserting the item"}, 500

        # the item here is the piece of json data.
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):
        data  = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            # **data = data['price'], data['store_id']
            item = ItemModel(name, **data)
        else:
            # this item is uniquely identified by the id
            item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        # ItemModel.query.all(), .all returns all the objects in a database.
        # 'items' : [item.json for item in ItemModel.query.all()]
        # 'items' :list(map(lambda x: x.json(), ItemModel.query.all()))
        # This maps function to the objects.
        return {'items': [item.json for item in ItemModel.query.all()]}
