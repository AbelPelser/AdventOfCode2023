class Edge:
    def __init__(self, a: 'Node', b: 'Node'):
        self.a = a
        self.b = b
        self.length = 1

    def get_neighbour(self, node: 'Node'):
        assert node in (self.a, self.b)
        return self.a if self.b == node else self.b

    def __hash__(self):
        return hash((self.a, self.b))

    def __repr__(self):
        return f'Edge a={self.a.location} b={self.b.location} length={self.length}'
