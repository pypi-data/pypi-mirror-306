import jsonschema
from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
from jsonschema.validators import Draft202012Validator


class JSONSchemaValidator(BaseValidator):
    def compare(self, value, schema):
        try:
            jsonschema.validate(
                value,
                schema,
                format_checker=Draft202012Validator.FORMAT_CHECKER,
            )
        except jsonschema.exceptions.ValidationError as e:
            raise ValidationError(str(e))
