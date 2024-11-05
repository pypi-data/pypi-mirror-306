from .schema import ValidationError
import re
from datetime import datetime

class BaseValidator:
    def __init__(self):
        self.error_message = None
        self.default_value = None
        self.expected_type = None
        self.is_required   = False

    def required(self):
        self.is_required = True
        return self

    def message(self, msg):
        self.error_message = msg
        return self

    def validate(self, value):
        # Handle default value
        if value is None:
            if self.is_required:
                raise ValidationError(self.error_message or "This field is required.")

        # Type inference check (if expected_type is set)
        if self.expected_type and not isinstance(value, self.expected_type):
            raise ValidationError(f"Expected type {self.expected_type.__name__}, got {type(value).__name__}.")

        return value
    

class StringValidator(BaseValidator):
    def __init__(self):
        self.min_length = None
        self.max_length = None
        self.is_email = False
        self.is_required = False
        self.error_message = None

    def email(self):
        self.is_email = True
        return self

    def min(self, length):
        self.min_length = length
        return self

    def max(self, length):
        self.max_length = length
        return self

    def required(self):
        self.is_required = True
        return self

    def message(self, msg):
        self.error_message = msg
        return self

    def validate(self, value):
        if self.is_required and value is None:
            raise ValidationError(self.error_message or "This field is required.")
        if value is None:
            return  # Skip validation if not required

        if not isinstance(value, str):
            raise ValidationError('Must be a string')
        if self.is_email and not self._is_valid_email(value):
            raise ValidationError(self.error_message or 'Invalid email format')
        if self.min_length is not None and len(value) < self.min_length:
            raise ValidationError(self.error_message or f'Is below the minimum length. MIN LENGTH: {self.min_length}.')
        if self.max_length is not None and len(value) > self.max_length:
            raise ValidationError(self.error_message or f'Is above the maximum length. MAX LENGTH: {self.max_length}.')

    def _is_valid_email(self, value):
        return re.match(r'^[\w-]+(\.[\w-]+)*@([\w-]+\.)+[a-zA-Z]{2,7}$', value) is not None

class NumberValidator(BaseValidator):
    def __init__(self):
        self.min_value = None
        self.max_value = None
        self.is_required = False
        self.error_message = None

    def required(self):
        self.is_required = True
        return self

    def min(self, value):
        self.min_value = value
        return self

    def max(self, value):
        self.max_value = value
        return self

    def message(self, msg):
        self.error_message = msg
        return self

    def validate(self, value):
        if self.is_required and value is None:
            raise ValidationError(self.error_message or "This field is required.")
        if value is None:
            return  # Skip validation if not required

        if not isinstance(value, (int, float)):
            raise ValidationError('Must be a number')
        if self.min_value is not None and value < self.min_value:
            raise ValidationError(self.error_message or f'Must be at least {self.min_value}')
        if self.max_value is not None and value > self.max_value:
            raise ValidationError(self.error_message or f'Must be at most {self.max_value}')

class BooleanValidator(BaseValidator):
    def __init__(self):
        self.is_required = False
        self.error_message = None

    def required(self):
        self.is_required = True
        return self

    def message(self, msg):
        self.error_message = msg
        return self

    def validate(self, value):
        if self.is_required and value is None:
            raise ValidationError(self.error_message or "This field is required.")
        if value is None:
            return  # Skip validation if not required

        if not isinstance(value, bool):
            raise ValidationError('Must be a boolean value')

class DateValidator(BaseValidator):
    def __init__(self):
        self.formats = ["%Y-%m-%d", "%m-%d-%Y", "%m-%Y-%d", "%d-%m-%Y"]  # List of accepted date formats
        self.is_required = False
        self.error_message = None

    def required(self):
        self.is_required = True
        return self

    def formats(self, formats):
        self.formats = formats
        return self

    def message(self, msg):
        self.error_message = msg
        return self

    def validate(self, value):
        if self.is_required and value is None:
            raise ValidationError(self.error_message or "This field is required.")
        if value is None:
            return  # Skip validation if not required

        for fmt in self.formats:
            try:
                datetime.strptime(value, fmt)
                return  # Valid date format found, exit the loop
            except ValueError:
                continue  # Try the next format

        # If none of the formats worked, raise a validation error
        raise ValidationError(self.error_message or f'Invalid date format. Accepted formats: {", ".join(self.formats)}')

class ArrayValidator(BaseValidator):
    def __init__(self):
        self.item_validator = None
        self.is_required = False
        self.error_message = None

    def required(self):
        self.is_required = True
        return self

    def items(self, validator):
        self.item_validator = validator
        return self

    def message(self, msg):
        self.error_message = msg
        return self

    def validate(self, value):
        if self.is_required and value is None:
            raise ValidationError(self.error_message or "This field is required.")
        if value is None:
            return  # Skip validation if not required

        if not isinstance(value, list):
            raise ValidationError('Must be an array')
        for item in value:
            if self.item_validator:
                self.item_validator.validate(item)

class CustomValidator(BaseValidator):
    def __init__(self, validator_func):
        self.validator_func = validator_func
        self.is_required = False
        self.error_message = None

    def required(self):
        self.is_required = True
        return self

    def message(self, msg):
        self.error_message = msg
        return self

    def validate(self, value):
        if self.is_required and value is None:
            raise ValidationError(self.error_message or "This field is required.")
        if value is None:
            return  # Skip validation if not required

        if not self.validator_func(value):
            raise ValidationError(self.error_message or 'Custom validation failed')
        
class ObjectValidator(BaseValidator):
    def __init__(self, shape):
        self.shape = shape

    def validate(self, value):
        if not isinstance(value, dict):
            raise ValidationError('Must be an object')

        validated_data = {}
        for key, validator in self.shape.items():
            if key in value:
                validator.validate(value[key])
                validated_data[key] = value[key]
            else:
                raise ValidationError(f'Missing field: {key}')
        return validated_data

class URLValidator(BaseValidator):
    def __init__(self):
        super().__init__()
        self.allowed_protocols = ["http", "https", "ftp", "mailto", "ws", "wss", "file"]  # Default protocols

    def allowedProtocols(self, *protocols):
        """Specify which protocols are allowed for validation."""
        self.allowed_protocols = protocols
        return self

    def validate(self, value):
        super().validate(value)

        if not isinstance(value, str):
            raise ValidationError("URL must be a string")

        # Construct a regex pattern to match allowed protocols
        protocol_pattern = '|'.join(self.allowed_protocols)
        if not re.match(rf'^(?:{protocol_pattern})://[^\s]+', value):
            raise ValidationError(f"Invalid URL format. Allowed protocols: {', '.join(self.allowed_protocols)}")
        