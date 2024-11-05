from .schema import Schema, ValidationError
from .validators import StringValidator, NumberValidator, BooleanValidator, ArrayValidator, CustomValidator, DateValidator

def Object(shape):
    return Schema(shape)

X = {
    'STRING':       StringValidator,
    'NUMBER':       NumberValidator,
    'BOOL':         BooleanValidator,
    'BOOLEAN':      BooleanValidator,
    'ARRAY':        ArrayValidator,
    'CUSTOM':       CustomValidator,
    "DATE":         DateValidator,
}
