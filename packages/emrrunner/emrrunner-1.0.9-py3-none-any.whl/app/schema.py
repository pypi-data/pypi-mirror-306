from marshmallow import Schema, fields, validate

class EMRJobSchema(Schema):
    """Schema for EMR job request validation."""
    job_name = fields.Str(required=True)
    step = fields.Str(required=True)
    deploy_mode = fields.Str(
        validate=validate.OneOf(['client', 'cluster']), 
        missing='client',  # default value
        dump_default='client'  # default value when serializing
    )