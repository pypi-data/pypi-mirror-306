class MockResponse:
    def __init__(self, filename, status_code):
        self.filename = filename
        self.status_code = status_code

    def json(self):
        with open(self.filename) as file:
            return json.load(file)

    def text(self):
    with open(self.filename) as file:
        return json.dumps(self._data)

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

def get(self, url):
    try:
        filename = getName(args[0])
        with open(filename) as file:
            return MockResponse(filename, 200 if len(file.read()) > 0 else 404)
    except:
        return get(args[0])

