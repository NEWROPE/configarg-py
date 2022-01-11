# configarg

This library provides a way to use a config file with [the official argparse library](https://docs.python.org/3/library/argparse.html).


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install configarg.

```bash
pip install configarg
```

## Usage

Assuming you have this JSON file:

```json
{
  "key1": "value1",
  "key2": "value2",
  "nested": {
    "key3": "value3",
  },
}
```

You can use the file to configure default values of your own parser built with `argparse`.

```python
import argparse
import configarg

# Build your parser
parser = argparse.ArgumentParser(description="My CLI tool")
parser.add_argument("--config", help="JSON configuration file")
parser.add_argument("--option1")
parser.add_argument("--option2")
parser.add_argument("--option3")

# Read the JSON file from `--config` option
config = Config.read_from_option(parser, "config")

# Assign values from the config file
if config is not None:
  config.configure(parser, {
      "key1": "option1",
      "key2": "option2",
      "nested.key3": "option3", # Nested fields are allowed
  })

args = parser.parse_args(args=["--option2", "value-from-cli"])
assert args.option1 == "value1"
assert args.option2 == "value-from-cli" # Value from command arguments will supersede a default value
assert args.option3 == "value3"
```

Also, you can use any format of files that can be parsed as a dict object. For example, if you use [PyYAML](https://github.com/yaml/pyyaml):

```python
...

def load(path):
    with open(path) as f:
        return yaml.load(f, Loader=yaml.CLoader)

config = Config.read_from_option(parser, "config", load)

...
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
