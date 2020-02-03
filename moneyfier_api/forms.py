from marshmallow import Schema, fields


class MonobankStatementsParamsSchema(Schema):
    account = fields.List(fields.String(), many=False, required=False)
    date_from = fields.List(fields.DateTime(), many=False, required=False)
    date_to = fields.List(fields.DateTime(), many=False, required=False)
