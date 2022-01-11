import json
import argparse

import pytest

from configarg import Config

@pytest.fixture
def json_path(tmp_path):
    path = tmp_path / "test.json"
    with open(path, "w") as f:
        json.dump({
            "key1": "value1",
            "key2": "value2",
            "nested": {
                "key3": "value3",
            },
        }, f)
    return path

def test_config(json_path):
    parser = argparse.ArgumentParser()
    parser.add_argument("--config")
    parser.add_argument("--option1")
    parser.add_argument("--option2")
    parser.add_argument("--option3")
    config = Config.read_from_option(parser, "config", args=["--config", str(json_path)])
    config.configure(parser, {
        "key1": "option1",
        "key2": "option2",
        "nested.key3": "option3",
    })
    args = parser.parse_args(args=["--option2", "value-from-cli"])
    assert args.option1 == "value1"
    assert args.option2 == "value-from-cli"
    assert args.option3 == "value3"
