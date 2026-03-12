import importlib


def test_import():
    assert importlib.import_module("ship_il_sdk") is not None
