class TreeNode:

    def __init__(self):
        self._children = set()
        self._labels = set()
        self._attrs = {}
        self._name = None

    def is_internal(self):
        return not is_leaf()

    def is_leaf(self):
        return len(self._children) == 0

    def children(self):
        return self._children

    def set_children(self, children):
        self._children = set(children)

    def labels(self):
        return self._labels

    def add_child(self, child):
        self._children.add(child)

    def set_name(self, name):
        self._name = name

    def name(self):
        return self._name

    def __str__(self):
        return self.name()

    def set_label(self, label):
        self._labels.add(label)

    def has_label(self, label):
        return label in self._labels

    def set_attr(self, key, val):
        self._attrs[key] = val

    def has_attr(self, key):
        return key in self._attrs

    def get_attr(self, key, dflt=None):
        return self._attrs.get(key, dflt)
