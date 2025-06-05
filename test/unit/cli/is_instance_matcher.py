class IsInstance:
    def __init__(self, cls):
        self.cls = cls

    def __eq__(self, other):
        is_eq = isinstance(other, self.cls)
        return is_eq

    def __repr__(self):
        return f"IsInstance({self.cls.__name__})"
