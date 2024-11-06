class ValidationError(Exception):
    pass

class Schema:
    def __init__(self, shape):
        self.shape = shape

    def validate(self, data):
        """
            Validate the provided data against the schema.\n
            Raises ValidationError if the data does not match the schema.\n
            Returns the validated data if no errors occur.\n
            Usage:\n
                Your_Schema.validate(Data)
        """
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
