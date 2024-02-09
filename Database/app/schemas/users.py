from marshmallow import Schema, fields

class RegisterUser(Schema):
    email = fields.Email(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    confirm_password = fields.Str(required=True)