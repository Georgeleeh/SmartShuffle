class node:
    def __init__(self, name=None, self_to_other=None, other_to_self=None):
        if name = None:
            name = ''
        self.name = name

        if self_to_other = None:
            self_to_other = []
        self.self_to_other = self_to_other

        if other_to_self = None:
            other_to_self = []
        self.other_to_self = other_to_self