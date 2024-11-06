# shiertier_os

English | [中文](https://github.com/shiertier-utils/shiertier_os/blob/main/README_zh.md)

## Introduction

`shiertier_os` is a Python utility library designed to simplify the management of environment variables. It provides functions to get, set, and convert environment variables, making it easier to work with environment configurations in your applications.

## Installation

You can install `shiertier_os` via `pip`:

```bash
pip install git+https://github.com/shiertier/shiertier_os.git
```

Please note that this project is still under development.

## Usage

### Getting Environment Variables

You can use the `get_env` function to retrieve environment variables. This function allows you to specify a default value if the environment variable is not set. If the value contains a comma, it will be converted to a list.

```python
from shiertier_os import get_env

# Get an environment variable
value = get_env('MY_VAR', default_value='default')
print(value)

# Get an environment variable as a list
value_list = get_env('MY_LIST_VAR', default_value='item1,item2,item3')
print(value_list)
```

### Setting Environment Variables

You can use the `set_env` function to set environment variables. If the value is a list, it will be converted to a string before being set.

```python
from shiertier_os import set_env

# Set an environment variable
set_env('MY_VAR', 'new_value')

# Set an environment variable from a list
set_env('MY_LIST_VAR', ['item1', 'item2', 'item3'])
```

### Getting Configuration Variables

You can use the `get_var` function to retrieve a configuration variable. This function first checks if the environment variable is set. If not, it returns the provided configuration value.

```python
from shiertier_os import get_var

# Get a configuration variable
config_value = get_var('MY_VAR', 'default_config_value')
print(config_value)
```

### Converting Between String and List

The library also provides utility functions to convert between strings and lists:

- `convert_str_to_list(s)`: Converts a comma-separated string to a list.
- `convert_list_to_str(l)`: Converts a list to a comma-separated string.

```python
from shiertier_os import convert_str_to_list, convert_list_to_str

# Convert a string to a list
my_list = convert_str_to_list('item1,item2,item3')
print(my_list)

# Convert a list to a string
my_string = convert_list_to_str(['item1', 'item2', 'item3'])
print(my_string)
```

## License

This project is released under the MIT License. See the [LICENSE](LICENSE) file for details.