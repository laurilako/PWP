from marshmallow import Schema, fields

# class ProductUpdateSchema(Schema):
#     image = fields.Str(required=False)
#     name = fields.Str(required=False)
#     price = fields.Float(required=False)
#     description = fields.Str(required=False)
#     category = fields.Str(required=False)
#     created_at = fields.DateTime(required=False)
#     updated_on = fields.DateTime(required=False)
#     type = fields.Str(required=False)

class NewProductListingSchema(Schema):
    _id = fields.Str(required=False)
    name = fields.Str(required=True)
    image = fields.Str(required=True)
    description = fields.Str(required=True)
    location = fields.Str(required=True)
    price = fields.Float(required=True)
    tags = fields.List(fields.Str(), required=True)
    owner = fields.Str(required=True)
    buyer = fields.Str(required=False)
    sold = fields.Bool(required=False)
    created_at = fields.DateTime(required=True)
    updated_on = fields.DateTime(required=True)