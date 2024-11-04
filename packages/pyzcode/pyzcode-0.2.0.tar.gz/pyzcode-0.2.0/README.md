# pyzcode

## Overview

`pyzcode` is a Python package designed to handle and manipulate zip codes in the United States. This package provides a comprehensive set of tools to validate, parse, and format zip codes, making it easier for developers to work with postal codes in their applications.

## Features

- **Parsing**: Extract relevant information from zip codes, such as state and city.
- **Lookup**: Retrieve detailed information about a zip code, including geographic and demographic data.

## Installation

You can install `pyzcode` using pip:

```sh
pip install pyzcode
```

## Usage

Once installed, you can start using `pyzcode` to handle zip codes in your Python projects. The package is designed to be intuitive and easy to integrate into existing codebases.

ZipCode class:

```python
from pyzcode import ZipCode

# Create a ZipCode object
zipcode = ZipCode('90210')

# Get the city and state
city = zipcode.city
state = zipcode.state

print(f'The city is {city} and the state is {state}')
```

ZipCodeQuery class:

```python
from pyzcode import ZipCodeQuery

# Create a ZipCodeQuery object
query = ZipCodeQuery()

# Lookup a zip code
zipcode = query.get_zipcode('90210')

print(zipcode)
```

### Get Zipcodes by city, state, and type

There are many combinations of get_zipcodes functions where the user can search by city, state, and zip code type.

```python
from pyzcode import ZipCodeQuery

# Create a ZipCodeQuery object
query = ZipCodeQuery()

# Get zip codes by city and state
zipcodes = query.get_zipcodes_by_city_state('Beverly Hills', 'CA')

print(zipcodes)

# Get zip codes by city, state, and type
zipcodes = query.get_zipcodes_by_city_state_type('Beverly Hills', 'CA', 'Standard')

print(zipcodes)
```

## License

`pyzcode` is licensed under the MIT License. See the LICENSE file for more details.

## Contributing

We welcome contributions to `pyzcode`. If you have suggestions for improvements or have found a bug, please open an issue or submit a pull request on our GitHub repository.

## Contact

For any questions or inquiries, please contact the maintainers at [email@example.com].
