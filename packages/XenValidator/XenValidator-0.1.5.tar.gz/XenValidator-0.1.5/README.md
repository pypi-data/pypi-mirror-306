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
            "Password": X["Password"]().min(8).max(64).required().message("Password is required and must be 8 characters long."),
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
- **Country**: Required string field for the user's country.
- **Phone**: Optional string field for the phone number.
- **Interests**: Array of strings representing user interests.
- **Balance**: Number field with a minimum value of 0.
- **LastLogin**: Optional date field indicating the last login date.
