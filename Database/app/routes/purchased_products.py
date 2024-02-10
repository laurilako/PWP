from flask import Blueprint, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from app.models.models import ProductListing
from flask_jwt_extended import jwt_required, get_jwt_identity

purchased_products_blb = Blueprint("purchased_products", __name__, url_prefix="/purchased_products")

# Can be used to get all purchased products or implemented later to return only purchased products by a user accessing the endpoint
@purchased_products_blb.route("/", methods=["GET"])
class PurchasedProducts(MethodView):
    @jwt_required()
    def get(self):
        # get user that is accessing the endpoint from the token
        user = get_jwt_identity()
        # get products that have been purchased by the user
        purchased = ProductListing.objects(buyer=user).all()
        return jsonify(purchased), 200
