import json
import urllib.parse
import requests
import os
#import pkg_resources

class MockResponse:
    def __init__(self, filepath, status_code):
        #self.filename = filename
        self.filepath = filepath
        self.status_code = status_code

    def json(self):
        if self.filepath:
            with open(self.filepath) as file:
                return json.load(file)
        print("Invalid URL")

    def text(self):
        if self.filepath:
            with open(self.filepath) as file:
                return json.dumps(file)
        print("Invalid URL")

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

def createCache(url):
    name = getName(url)
    if not os.path.isfile(name):
        data = requests.get(url)
        if data.status_code != 200:
            # raise ValueError(f"{url} has an invalid response.")
            print(f"{url} has an invalid response.")
            return False
        data = data.json()
        with open(name, "w") as outfile:
            json.dump(data, outfile)
        with open(getName(url + "/"), "w") as outfile:
            json.dump(data, outfile)
    return True


def get(url):
    try:
        filename = getName(url)
        filepath = os.path.join(os.path.dirname(__file__), "data", filename)
        #filepath = pkg_resources.resource_filename('mock_requests', "data/" + filename)
        with open(filepath) as file:
                return MockResponse(filepath, 200 if len(file.read()) > 0 else 404)
    except:
        filename = getName(url)
        if "https://taylor-swift-api.sarbo.workers.dev/lyrics" in url or "https://taylor-swift-api.sarbo.workers.dev/albums" in url or "https://taylor-swift-api.sarbo.workers.dev/songs" in url:
            request = requests.get(url)
            data = request.json()
            with open(filename, "w") as outfile:
                json.dump(data, outfile)
                return MockResponse(filename, request.status_code)
        else:
            return MockResponse("", 404)






