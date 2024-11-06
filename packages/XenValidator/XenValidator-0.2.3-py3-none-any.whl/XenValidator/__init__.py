from .schema import Schema, ValidationError
from .validators import StringValidator, NumberValidator, BooleanValidator, ArrayValidator, OptionsValidator, CustomRegexValidator, JSONValidator, CustomValidator, DateValidator, URLValidator, IPAddressValidator, SizeValidator

def Object(shape):
    """ 
    Creates a Schema instance based on the provided shape, enabling object-based schema validation.

    Parameters:
    -----------
    shape : dict
        A dictionary representing the structure of the schema, where keys are field names and values 
        are validator instances initialized with specific rules.

    Returns:
    --------
    Schema
        A schema instance configured with the specified structure, enabling validation according to the defined rules.

    Usage:
    ------
    Define your schema using the `Object` function and `X` validator types:
    
        ```python
        Your_Schema = Object({
            "Name": X['STRING']().message("Name is required!"),
            "Age":  X['NUMBER']().min(3),                         
            "DOB":  X["DATE"]().required(),                       
        })
        ```

    Example:
    --------
    Here's an example of how to use `Your_Schema` for validation:

        ```python
        data = {
            "Name": "John Doe",
            "Age": 25,
            "DOB": "1995-05-15",
        }
        
        try:
            Your_Schema.validate(data)
        except ValidationError as e:
            print("Validation Error:", e)
        ```

    Fields:
    -------
    - `STRING`: Validates the value as a string, optionally with custom messages, length, etc.
    - `NUMBER`: Validates the value as a number, supporting rules like min and max values.
    - `BOOL` / `BOOLEAN`: Validates the value as a boolean.
    - `ARRAY`: Validates the value as an array, with support for nested schema validation.
    - `CUSTOM`: A placeholder for any custom validation logic.
    - `DATE`: Validates the value as a date with required fields and optional range constraints.
    - `URL`: Validates the value as an URL (http://, https://, ftp://).
    - `IP` / `IPADDRESS`: Validates the value as an IP address (192.168.0.1).
    - `RANGE`: Validates the value's size within a specified range.
    - `_REGEX`: Allows you to define a custom regex validation rule.
    - `JSON`: Validates the value as a JSON string.
    - `OPTIONS` / `PICK`: Validates the value against a predefined list of options.
    """
    return Schema(shape)

X = {
    'STRING':       StringValidator,
    'NUMBER':       NumberValidator,
    'BOOL':         BooleanValidator,
    'BOOLEAN':      BooleanValidator,
    'ARRAY':        ArrayValidator,
    'CUSTOM':       CustomValidator,
    "DATE":         DateValidator,
    "URL":          URLValidator,
    "IP":           IPAddressValidator,
    "IPADDRESS":    IPAddressValidator,
    "RANGE":        SizeValidator,
    "_REGEX":       CustomRegexValidator,
    "JSON":         JSONValidator,
    "OPTIONS":      OptionsValidator,
    "PICK":         OptionsValidator,
}
