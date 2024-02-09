from flask import Blueprint, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from app.models.models import PurchasedProductListing
from flask_jwt_extended import jwt_required

purchased_products_blb = Blueprint("purchased_products", __name__, url_prefix="/purchased_products")

# Can be used to get all purchased products or implemented later to return only purchased products by a user accessing the endpoint
@purchased_products_blb.route("/", methods=["GET"])
class PurchasedProducts(MethodView):
    @jwt_required()
    def get(self):
        purchased_products = PurchasedProductListing.get_all()
        return jsonify(purchased_products), 200
