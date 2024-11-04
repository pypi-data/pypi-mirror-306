
class Transformation:
    def apply(self, data):
        raise NotImplementedError

class Normalize(Transformation):
    def __init__(self, scale=1.0):
        self.scale = scale

    def apply(self, data):
        return data * self.scale
