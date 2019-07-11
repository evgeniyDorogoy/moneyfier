from marshmallow import Schema, fields


class MonobankStatementsParamsSchema(Schema):
    account = fields.String(required=False)
    date_from = fields.DateTime(required=False)
    date_to = fields.DateTime(required=False)
