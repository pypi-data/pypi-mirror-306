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
        "IsProMember": X["BOOLEAN"](),
        "Auth": Object({
            "Email": X["STRING"]().email().required(),
            "Password": X["STRING"]().min(8).max(64).required().message("Password is required and must be 8 characters long."),
            "IpAddress": X["IPADDRESS"]().required().message("Invalid IP address."),
            "JoinedOn": X["DATE"](),
        }),
        "SiteName": X["URL"](),
    })

    try:
        Data = {
            "Name": "John Doe",
            "Age": 18,
            "Tags": ["Live streamer", "Web designer", "Front-end developer"],
            "IsProMember": False,
            "Auth": {
                "Email": "mail@example.com",
                "Password": "SecurePassword123&",
                "IpAddress": "127.0.0.1",
                "JoinedOn": "2024-11-05",
            },
            "SiteName": "https://mysite.com",
        }
        Schema.validate(Data)
        print("Data is valid:", Data)
    except ValidationError as e:
        print("Data is invalid:", e)
```

### Explanation

- **Name**: Required field validated as a string.
- **Age**: Number field with a minimum value of 2.
- **Tags**: Array field validated to ensure it is indeed an array.
- **IsProMember**: Boolean field indicating if the user is a pro member.
- **Auth**: Nested object for authentication details.
  - **Email**: Required field validated as a valid email.
  - **Password**: Required string with length between 8 and 64 characters.
  - **IpAddress**: Required field validated as a valid IP address.
  - **JoinedOn**: Optional date field.
- **SiteName**: Optional field validated as a URL.

#### Validate a Regex value

You can use XenValidator's ***Regex*** validation to create TypeSafe Data types such as how many characters should it include and should it be **Case Sensitive** or not. You can use it to validate strong passwords and more.

```bash
    # Define your scheama & create a regex to match pattren with
    Schema = Object({
        # This regex requires at least 1 Uppercase & Lowercase letter and 1 Number & Must be 8 characters long
        "Regex": X["_REGEX"](r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,12}$'),
    })

    # Validate the ragex
    try:
        Data = {
            "Regex": "YourName123",
        }
        Schema.validate(Data)
        print("Valid regex:", Data)
    except ValidationError as e:
        print("Invalid regex:", e)


```

#### Create custom types to validate

```bash
    # Define a custom type to validate

    # This is a type which takes a positive number
    def isPositive(value):
        return isinstance(value, (int, float)) and value > 0

    # Define your schema
    Schema = Object({
        "Amount": X["CUSTOM"](isPositive).required().message("Amount must be positive."),
    })

    # Validate the Data
    try:
        Data = {
            "Amount": 10000  # Valid positive number (A negative number should return an error)
        }
        Schema.validate(Data)
        print("Valid amount:", Data)
    except ValidationError as e:
        print("Invalid amount:", e)


```
