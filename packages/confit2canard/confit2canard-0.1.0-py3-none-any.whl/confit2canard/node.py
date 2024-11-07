class Node:
    def __init__(self, data: dict):
        self._keys = []
        for key, value in data.items():
            setattr(self, key, value)
            self._keys.append(key)

    def __getattribute__(self, attr: str):
        value = super().__getattribute__(attr)
        if isinstance(value, dict):
            value = Node(value)
        return value

    def __getitem__(self, item):
        return getattr(self, item, None)

    def __iter__(self):
        for key in self._keys:
            yield key
