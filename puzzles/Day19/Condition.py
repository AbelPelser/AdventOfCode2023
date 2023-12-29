class Condition:
    def __init__(self, eval_str):
        self.eval_str = eval_str

    # noinspection PyUnusedLocal
    def evaluate(self, x, m, a, s):
        return eval(self.eval_str)

    def __hash__(self):
        return hash(self.eval_str)


TRUE_COND = Condition('True')
