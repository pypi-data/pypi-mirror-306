# python-lynxlynx

## About

Shared Python library used by my scripts.

## Installation

```shell
python -m build
```
## Development docs

### Upload to PyPI

First create the config file `~/.pypirc`:
```ini
[pypi]
	username = __token__
	password = pypi-ABCDEFGHTOKEN
```

Then upload the package:
```shell
# Testing PyPI
python -m twine upload --repository testpypi dist/*
# Prod PyPI
python -m twine upload dist/*
```
## License

AGPL-3.0-only, contact me if you need other licensing.
