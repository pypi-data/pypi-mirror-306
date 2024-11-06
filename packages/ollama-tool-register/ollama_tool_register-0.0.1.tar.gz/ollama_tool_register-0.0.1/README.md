# ollama-tool-register

[![PyPI - Version](https://img.shields.io/pypi/v/ollama-tool-register.svg)](https://pypi.org/project/ollama-tool-register)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ollama-tool-register.svg)](https://pypi.org/project/ollama-tool-register)

A simple library to register your python functions as tools to be used by supported Ollama LLM models.

### Status

This is a hobby project for now, consider all the interfaces to be alpha quality and subject to backwards breaking change until version 1.0.

Pull Requests welcome - use `ruff check` && `ruff format` tools and add/run tests with `pytest`.

### Todos

- more functionality, as I discover needs in my own use
- more tests, more developer setup docs if others show interest

-----

## Table of Contents

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install ollama-tool-register
```

## Example

```python
@ollama.annotated_tool
def some_tool_function(
    expr_1: t.Annotated[str, "first simple str value"],
    expr_2: t.Annotated[str, "second simple str value"],
    req_int_arg: t.Annotated[int, "a required integer"],
    req_float_arg: t.Annotated[float, "any real number"],
    req_list_arg_1: t.Annotated[list, "any builtin list"],
    req_list_arg_2: t.Annotated[t.List[t.Any], "any typed List"],
    req_enum_1: t.Annotated[ExampleEnum, "required foo bar or baz"],
    opt_arg_1: t.Annotated[t.Optional[str], "an optional string"] = None,
    opt_enum_1: t.Annotated[t.Optional[ExampleEnum], "optional foo bar or baz"] = None,
    opt_enum_2: ExampleEnum = ExampleEnum.FOO,
    opt_builtin_str_1: str = "foobar",
    opt_builtin_int_1: int = 1e6,
    opt_builtin_float_1: float = 1.0,
    opt_builtin_list_1: list = None,
):
    """a test case for Annotating a tool function's parameters.
    the docstring of the function is the Function.description."""
    return None
```

The above `some_tool_function.tool_schema` would provide this, usable as an item in Ollama Python's `tools=` list


```json
{
  "type": "function",
  "function": {
    "name": "example_1",
    "description": "a test case for Annotating a tool function's parameters.\n    the docstring of the function is the Function.description.",
    "parameters": {
      "type": "object",
      "required": [
        "expr_2",
        "expr_1",
        "req_int_arg",
        "req_list_arg_2",
        "req_enum_1",
        "req_float_arg",
        "req_list_arg_1"
      ],
      "properties": {
        "expr_1": {
          "type": "string",
          "description": "first simple str value",
          "is_optional": false,
          "enum": null
        },
        "expr_2": {
          "type": "string",
          "description": "second simple str value",
          "is_optional": false,
          "enum": null
        },
        "req_int_arg": {
          "type": "integer",
          "description": "a required integer",
          "is_optional": false,
          "enum": null
        },
        "req_float_arg": {
          "type": "number",
          "description": "any real number",
          "is_optional": false,
          "enum": null
        },
        "req_list_arg_1": {
          "type": "array",
          "description": "any builtin list",
          "is_optional": false,
          "enum": null
        },
        "req_list_arg_2": {
          "type": "array",
          "description": "any typed List",
          "is_optional": false,
          "enum": null
        },
        "req_enum_1": {
          "type": "string",
          "description": "required foo bar or baz",
          "is_optional": false,
          "enum": [
            "foo",
            "bar",
            "baz"
          ]
        },
        "opt_arg_1": {
          "type": "string",
          "description": "an optional string",
          "is_optional": true,
          "enum": null
        },
        "opt_enum_1": {
          "type": "string",
          "description": "optional foo bar or baz",
          "is_optional": true,
          "enum": [
            "foo",
            "bar",
            "baz"
          ]
        },
        "opt_enum_2": {
          "type": "string",
          "description": "opt enum 2",
          "is_optional": true,
          "enum": [
            "foo",
            "bar",
            "baz"
          ]
        },
        "opt_builtin_str_1": {
          "type": "string",
          "description": "opt builtin str 1",
          "is_optional": true,
          "enum": null
        },
        "opt_builtin_int_1": {
          "type": "integer",
          "description": "opt builtin int 1",
          "is_optional": true,
          "enum": null
        },
        "opt_builtin_float_1": {
          "type": "number",
          "description": "opt builtin float 1",
          "is_optional": true,
          "enum": null
        },
        "opt_builtin_list_1": {
          "type": "array",
          "description": "opt builtin list 1",
          "is_optional": true,
          "enum": null
        }
      }
    }
  }
}
```

## License

`ollama-tool-register` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
