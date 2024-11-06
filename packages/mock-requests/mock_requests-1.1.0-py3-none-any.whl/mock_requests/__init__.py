import json
import urllib.parse
import requests
import os
#import pkg_resources
from .mock_requests import get, getName, MockResponse

"""
Rebuild distribution files:
python setup.py sdist bdist_wheel

Re-upload to PyPI:
twine upload dist/*

To install locally:
pip install dist/mock_requests-1.0.0-py3-none-any.whl --force-reinstall
"""

