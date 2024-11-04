
class Condition:
    def evaluate(self, data):
        raise NotImplementedError

class ValueAboveThreshold(Condition):
    def __init__(self, threshold):
        self.threshold = threshold

    def evaluate(self, data):
        return data > self.threshold

class CompositeCondition(Condition):
    def __init__(self, *conditions, operator='AND'):
        self.conditions = conditions
        self.operator = operator

    def evaluate(self, data):
        if self.operator == 'AND':
            return all(cond.evaluate(data) for cond in self.conditions)
        elif self.operator == 'OR':
            return any(cond.evaluate(data) for cond in self.conditions)
        elif self.operator == 'NOT':
            return not self.conditions[0].evaluate(data)
        else:
            raise ValueError('Unsupported operator')
