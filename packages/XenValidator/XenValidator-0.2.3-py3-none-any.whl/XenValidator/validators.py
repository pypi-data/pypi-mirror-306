from .schema import ValidationError
import re, json
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

class CustomRegexValidator(BaseValidator):
    def __init__(self, pattern):
        super().__init__()
        self.pattern = pattern
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

        if not isinstance(value, str):
            raise ValidationError('Must be a string')
        if not re.match(self.pattern, value):
            raise ValidationError(self.error_message or 'Value does not match the required pattern')
        
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
        
class IPAddressValidator(BaseValidator):
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

        if not isinstance(value, str):
            raise ValidationError('Must be a string')
        if not self._is_valid_ip(value):
            raise ValidationError(self.error_message or 'Invalid IP address format')

    def _is_valid_ip(self, value):
        ip_pattern = (
            r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$'  # IPv4
            r'|^([0-9a-fA-F]{1,4}:){7}([0-9a-fA-F]{1,4}|:)$'  # IPv6 (compressed)
            r'|^::(?:[0-9a-fA-F]{1,4}:){0,6}[0-9a-fA-F]{1,4}$'  # IPv6 (expanded)
            r'|^([0-9a-fA-F]{1,4}:){1,7}:$'  # IPv6 (loopback)
        )
        return re.match(ip_pattern, value) is not None
    
class SizeValidator(BaseValidator):
    def __init__(self):
        self.max_size = None  # in bytes
        self.is_required = False
        self.error_message = None

    def required(self):
        self.is_required = True
        return self

    def max(self, size):
        self.max_size = size
        return self

    def message(self, msg):
        self.error_message = msg
        return self

    def validate(self, value):
        if self.is_required and value is None:
            raise ValidationError(self.error_message or "This field is required.")
        if value is None:
            return  # Skip validation if not required

        if not isinstance(value, int):
            raise ValidationError('File size must be an integer (in bytes)')
        if self.max_size is not None and value > self.max_size:
            raise ValidationError(self.error_message or f'File size must be at most {self.max_size} bytes')

class JSONValidator(BaseValidator):
    def __init__(self):
        super().__init__()
        self.schema = None
        self.is_required = False

    def required(self):
        self.is_required = True
        return self

    def schema(self, schema):
        """Define a schema that the JSON object must match."""
        self.schema = schema
        return self

    def message(self, msg):
        self.error_message = msg
        return self

    def validate(self, value):
        if self.is_required and value is None:
            raise ValidationError(self.error_message or "This field is required.")
        if value is None:
            return  # Skip validation if not required

        try:
            data = json.loads(value)
            if self.schema:
                validated_data = {}
                for key, validator in self.schema.items():
                    if key in data:
                        validator.validate(data[key])
                        validated_data[key] = data[key]
                    else:
                        raise ValidationError(f'Missing field in JSON: {key}')
            return data
        except json.JSONDecodeError:
            raise ValidationError(self.error_message or "Invalid JSON format")

class OptionsValidator(BaseValidator):
    def __init__(self, options):
        super().__init__()
        self.options = options

    def validate(self, value):
        super().validate(value)
        if value not in self.options:
            options_str = " | ".join(self.options)
            raise ValidationError(f"Value must be one of: {options_str}")