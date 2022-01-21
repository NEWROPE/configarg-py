import json
import argparse

import pytest

from configarg import Config


@pytest.fixture
def json_path(tmp_path):
    path = tmp_path / "test.json"
    with open(path, "w") as f:
        json.dump({"test": "ok"}, f)
    return path


def test_getitem():
    config = Config({"parent": {"child": "value"}})
    assert config["parent.child"] == "value"


def test_configure():
    config = Config({"parent": {"child": "value"}})
    parser = argparse.ArgumentParser()
    config.configure(parser, {"parent.child": "destination"})
    args = parser.parse_args([])
    assert args.destination == "value"


def test_read(json_path):
    config = Config.read(json_path)
    assert config["test"] == "ok"


def test_read_with_custom_load_func():
    def load(path):
        return {"path": path}  # Can be YAML parser etc.

    config = Config.read("config-file-path", load)
    assert config["path"] == "config-file-path"


def test_read_from_option(json_path):
    parser = argparse.ArgumentParser()
    parser.add_argument("--config")
    config = Config.read_from_option(
        parser, "config", args=["--config", str(json_path)]
    )
    assert config["test"] == "ok"


def test_read_from_option_without_config(json_path):
    parser = argparse.ArgumentParser()
    parser.add_argument("--config")
    config = Config.read_from_option(parser, "config", args=[])
    assert config is None


def test_read_from_option_with_help(json_path):
    parser = argparse.ArgumentParser()
    parser.add_argument("--config")
    config = Config.read_from_option(
        parser, "config", args=["--help", "--config", str(json_path)]
    )
    assert config["test"] == "ok"
