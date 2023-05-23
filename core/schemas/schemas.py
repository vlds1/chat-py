from marshmallow import Schema, fields


class UserSchema(Schema):
    email = fields.Email()
    password = fields.Str()

    class Meta:
        strict = True


class JWTSchema(Schema):
    refresh_token = fields.Str()

    class Meta:
        strict = True
