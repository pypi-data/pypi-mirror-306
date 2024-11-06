import json
import urllib.parse
import requests
import os
#import pkg_resources

class MockResponse:
    def __init__(self, filename, filepath, status_code):
        self.filename = filename
        self.filepath = filepath
        self.status_code = status_code

    def json(self):
        with open(self.filepath) as file:
            return json.load(file)

    def text(self):
        with open(self.filepath) as file:
            return json.dumps(file)

    def __str__(self):
        return '<Response [' + str(self.status_code) + ']>'

    # parse request url and make new name for opening cached data

def getName(string):
    url = urllib.parse.urlparse(string)
    queries = dict(item.split('=') for item in url.query.split('&')) if url.query else dict()
    name = url.netloc + url.path
    for k,v in sorted(queries.items()):
        if 'key' not in k.lower():
            name += '/' + k + '=' + v
    name = ''.join(c if c.isalnum() else '_' for c in name) + '.json'
    return name


def get(url):
    try:
        filename = getName(url)
        filepath = os.path.join(os.path.dirname(__file__), "data", filename)
        #filepath = pkg_resources.resource_filename('mock_requests', "data/" + filename)
        with open(filepath) as file:
                return MockResponse(filename, filepath, 200)

    except:
        print(f"Error: File for URL '{url}' not found.")
        return MockResponse(filename, filepath, 404)

