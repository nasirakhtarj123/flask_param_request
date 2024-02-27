from marshmallow import Schema, fields

class ParentSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    age = fields.Int(required=True)


class ParentsSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    age = fields.Int(required=True)