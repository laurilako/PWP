from flask import Flask
from flask_bcrypt import Bcrypt
from flask_mongoengine import MongoEngine
import json
import datetime
from flask_jwt_extended import JWTManager
from app.routes.user_routes import user_bp
from app.routes.products import products_blb
from app.routes.purchased_products import purchased_products_blb
from app.models.models import User, ProductListing, PurchasedProductListing

app = Flask(__name__)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

app.config["JWT_SECRET_KEY"] = "super-secret"

app.config["MONGODB_SETTINGS"] = {
    "db": "test_sellixdb",
    "host": "mongodb://localhost:27017/test_sellixdb",
}

db = MongoEngine()

db.init_app(app)

app.register_blueprint(user_bp)
app.register_blueprint(products_blb)
app.register_blueprint(purchased_products_blb)


# populate the database with test data from JSON files
def populate_db():
    print("Populating the database with test data...")

    with open("app/data/sellixdb.user.json", "r") as f:
        users = json.load(f)
        for user in users:
            new_user = User(
                **user,
                created_at = datetime.datetime.now(),
                modified_at = datetime.datetime.now()
            )
            new_user.save()

    with open("app/data/sellixdb.product_listing.json", "r") as f:
        products = json.load(f)
        for product in products:
            new_product = ProductListing(
                **product,
                created_at = datetime.datetime.now(),
                updated_on = datetime.datetime.now()
            )
            new_product.save()

    with open("app/data/sellixdb.purchased_product_listing.json", "r") as f:
        purchased_products = json.load(f)
        for purchased_product in purchased_products:
            new_purchased_product = PurchasedProductListing(
                **purchased_product
            )
            new_purchased_product.save()

    print("Database populated with test data.")

populate_db()

if __name__ == "__main__":
    app.run(port=8000, debug=True)
