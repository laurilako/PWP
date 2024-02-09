from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from datetime import datetime
from bson import ObjectId
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.schemas.products import NewProductListingSchema
from app.models.models import ProductListing, User, PurchasedProductListing

products_blb = Blueprint("products", __name__, url_prefix="/products")

@products_blb.route("/")
class Products(MethodView):
    def get(self):
        # Get all products
        products = ProductListing.get_all()
        print(products)
        return jsonify(products), 200
    
# Create a new product
@products_blb.route("/", methods=["POST"])
class Products(MethodView):
    @jwt_required()
    def post(self):
        try:
            current_date =  datetime.now().isoformat()
            # get user that is accessing the endpoint from the token
            user = get_jwt_identity()
            # get user object from the database
            user_object = User.objects.get(username=user)
            # get product data from body of request
            product = request.json
            # add timestamp to product
            product["created_at"] = current_date
            product["updated_on"] = current_date
            # add username to product owner field
            product["owner"] = user_object.username

            # Validate data with marshmallow
            product_create_schema = NewProductListingSchema()
            validated_data = product_create_schema.load(product)

            # Create the new product
            prod = ProductListing(
                _id = ObjectId(),
                **validated_data
            )
            saved = prod.save()
            # add product to user's created products
            user_object.created_products.append(prod.to_dbref())
            # update user object
            user_object.save()
            return jsonify(saved), 201
        except Exception as e:
            print(e)
            return jsonify({"error": "Error creating new product"}), 400

# Get a single product by object id
@products_blb.route("/<string:pid>")
class Product(MethodView):
    def get(self, pid):
        product = ProductListing.objects(_id=pid).first()
        if product:
            return jsonify(product), 200
        return jsonify({"error": "Product not found"}), 404

# When user buys a product, update the product's buyer and sold fields and create new purchased product for the user
# Endpoint for this. The user must be authenticated to access this endpoint
@products_blb.route("/<string:pid>/buy", methods=["PUT"])
class Product(MethodView):
    @jwt_required()
    def put(self, pid):
        try:
            # get user that is accessing the endpoint from the token
            user = get_jwt_identity()
            # get user object from the database
            user_object = User.objects(username=user).first()
            # get product object from the database
            product = ProductListing.objects(_id=pid).first()
            
            if not product:
                return jsonify({"error": "Product not found"}), 404

            if(product.sold):
                return jsonify({"error": "Product already sold"}), 400


            # get product owner field from the product object
            product_owner = product.to_mongo().to_dict()["owner"]

            # get product owner object from the database
            product_owner_obj = User.objects(username=product_owner).first()

            if(product_owner is None):
                return jsonify({"error": "Product owner not found"}), 404
            
            if product:
                try:
                    product.buyer = user_object._id
                    product.sold = True
                    product.save()
                    # create new purchased product object and save to database 
                    purchased_product = PurchasedProductListing(
                        _id = ObjectId(),
                        name = product.name,
                        image = product.image,
                        description = product.description,
                        location = product.location,
                        price = product.price,
                        seller = product_owner_obj._id
                    )
                    purchased_product.save()
                    # add newly created purchased product to buyers purchased products array, using dbref
                    user_object.purchased_products.append(purchased_product.to_dbref())
                    # save user object to database
                    user_object.save()
                except Exception as e:
                    print(e.with_traceback())
                    return jsonify({"error": "Error purchasing product"}), 400
                return jsonify({"message": "Product purchased successfully"}), 200
            return jsonify({"error": "Product not found"}), 404
        except Exception as e:
            print(e.with_traceback())
            return jsonify({"error": "Error purchasing product"}), 400

# Update or delete a product by object id, not implemented yet

# @products_blb.route("/<string:pid>", methods=["PUT", "DELETE"])
# class Product(MethodView):
#     @products_blb.response(200)
#     def put(self, pid):
#         product_index = find_item_index(pid=pid, plist=products)

#         # Update product
#         if product_index is not None:
#             current_date = date.today()
#             # Validate coming data with marshmallow
#             product_update_schema = ProductUpdateSchema()
#             validated_data = product_update_schema.load(request.args)

#             new_data = {
#                 **validated_data,
#                 "updated_on": current_date,
#             }

#             # Update the product
#             products[product_index].update(new_data)
#             return jsonify(products[product_index]), 200

#         return jsonify({"error": "Product not found"}), 404

#     def delete(self, pid):
#         product_index = find_item_index(pid=pid, plist=products)
#         # Delete product from the list
#         if product_index is not None:
#             del products[product_index]
#             return (
#                 jsonify({"message": f"Product {pid} deleted successfully."}),
#                 200,
#             )

#         return jsonify({"error": "Product not found"}), 404
