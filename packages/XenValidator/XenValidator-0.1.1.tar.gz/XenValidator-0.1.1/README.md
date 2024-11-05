# XenValidator
XenValidator is a powerful, flexible, and easy-to-use Python library for validating data structures. It simplifies the process of defining complex validation rules, handling cross-field dependencies, and providing informative error messages.

## *Features*
**Comprehensive Validation**: Supports validation for strings, numbers, dates, arrays, urls, and custom data types.

**Custom Error Handling**: Easily customize error messages for various validation rules.

**Flexible Date Formats**: Supports multiple date formats to match various use cases.

## Installation

Install ***XenValidator*** using pip:

```bash
    pip install xenvalidator
``` 

## Example usage:

#### *Import* the package into to your app:

```bash
    from XenValidator import X, Object, ValidationError
```

#### Create and validate the schema.

```bash
    Schema = Object({
        "Name": X["STRING"](),
        "Age":  X["NUMBER"]().min(2),
        "Tags": X["ARRAY"](),
    })

    try:
        Data = {
            "Name": "John Doe",
            "Age": 18,
            "Tags": ["TAG1", "TAG2", "TAG3"], 
        }
        Schema.validate(Data)
        print("Data is valid:", Data)
    except ValidationError as e:
        print("Data is invalid:", e)
```