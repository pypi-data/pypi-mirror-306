class ValidationError(Exception):
    pass

class Schema:
    def __init__(self, shape):
        self.shape = shape

    def validate(self, data):
        errors = {}

        for key, validator in self.shape.items():
            try:
                value = data.get(key)
                validator.validate(value)
            except ValidationError as e:
                errors[key] = str(e)

        if errors:
            raise ValidationError(errors)
        return data
