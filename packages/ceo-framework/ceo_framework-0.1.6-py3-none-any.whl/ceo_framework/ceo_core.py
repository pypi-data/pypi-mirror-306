# ceo_core.py
from ceo_framework import Transformation, Condition


class CEO:
    def __init__(self):
        self.conditions = []
        self.transformations = []

    def add_condition(self, condition):
        """Adds a Condition instance to the CEO."""
        if not isinstance(condition, Condition):
            raise TypeError("Condition must be an instance of Condition class.")
        self.conditions.append(condition)

    def add_transformation(self, transformation):
        """Adds a Transformation instance to the CEO."""
        if not isinstance(transformation, Transformation):
            raise TypeError("Transformation must be an instance of Transformation class.")
        self.transformations.append(transformation)

    def process(self, data):
        """Evaluates conditions and applies transformations conditionally."""
        # If all conditions are met, apply all transformations
        if all(condition.evaluate(data) for condition in self.conditions):
            for transformation in self.transformations:
                data = transformation.apply(data)
        return data
