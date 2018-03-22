
class SvnLump:

    def __init__(self):
        self.headers = { }
        self.header_order = [ ]
        self.properties = { }
        self.content = None

    def set_header(self, key, value):
        if not self.headers.has_key(key):
            self.header_order.append(key)
        self.headers[key] = value
        return self

    def get_header(self, key):
        return self.headers[key]

    def has_header(self, key):
        return self.headers.has_key(key)

    def delete_header(self, key):
        del self.headers[key]
        self.header_order.remove(key)
        return self

    def get_header_keys(self):
        return self.header_order

    @property
    def path(self):
        return self.headers.get("Node-path", None)

    @property
    def kind(self):
        return self.headers.get("Node-kind", None)

    @property
    def action(self):
        return self.headers.get("Node-action", None)

    @property
    def revision(self):
        return self.headers.get("Revision-number", None)
