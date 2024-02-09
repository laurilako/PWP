from datetime import datetime
import mongoengine as me
from flask_bcrypt import generate_password_hash, check_password_hash

class ProductListing(me.Document):
    _id = me.ObjectIdField()
    name = me.StringField(required=True, unique=False)
    image = me.StringField(required=False)
    description = me.StringField(required=True)
    location = me.StringField(required=True)
    price = me.DecimalField(required=True)
    tags = me.ListField(field=me.StringField(), required=True)
    owner = me.ReferenceField('User', required=True)
    buyer = me.ReferenceField('User', required=False)
    created_at = me.DateTimeField(required=True)
    updated_on = me.DateTimeField(required=True)
    sold = me.BooleanField(required=True, default=False)

    def get_all():
        return ProductListing.objects()

class PurchasedProductListing(me.Document):
    _id = me.ObjectIdField()
    name = me.StringField(required=False, unique=False)
    image = me.StringField(required=False)
    description = me.StringField(required=False)
    location = me.StringField(required=False)
    price = me.DecimalField(required=True)
    seller = me.ReferenceField('User', required=True)

    def get_all():
        return PurchasedProductListing.objects()
    
class User(me.Document):
    _id = me.ObjectIdField()
    username = me.StringField(required=True, unique=True)
    email = me.EmailField(required=True, unique=True)
    password = me.StringField(required=True)
    phone_number = me.StringField(required=False)
    created_at = me.DateTimeField(required=True, default=datetime.now())
    modified_at = me.DateTimeField(required=True, default=datetime.now())
    created_products = me.ListField(field=me.ReferenceField(ProductListing))
    purchased_products = me.ListField(field=me.ReferenceField(PurchasedProductListing))
    # implement later - this is for the user's favourite products
    favourites = me.ListField(field=me.StringField())

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf-8')

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
User.register_delete_rule(ProductListing, 'owner', me.CASCADE)
User.register_delete_rule(PurchasedProductListing, 'seller', me.CASCADE)
