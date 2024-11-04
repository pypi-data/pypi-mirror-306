
class CEO:
    def __init__(self):
        self.conditions = []
        self.transformations = []

    def add_condition(self, condition):
        self.conditions.append(condition)

    def add_transformation(self, transformation):
        self.transformations.append(transformation)

    def process(self, data):
        for condition in self.conditions:
            if condition.evaluate(data):
                for transformation in self.transformations:
                    data = transformation.apply(data)
        return data
