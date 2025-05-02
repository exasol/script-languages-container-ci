
class IsInstance:
    def __init__(self, cls):
        self.cls = cls

    def __eq__(self, other):
        return isinstance(other, self.cls)

    def __repr__(self):
        return f"IsInstance({self.cls.__name__})"