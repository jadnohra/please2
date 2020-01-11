class TreeNode:

    class LabelLayer:
        def __init__(self, name = ''):
            self._labels = set()
            self._attrs = {}
            self._name = name
            self._value = None

        def __str__(self):
            return self.name()

        def set_name(self, name):
            self._name = name

        def name(self):
            return self._name

        def set_value(self, value):
            self._value = value

        def value(self):
            return self._value

        def labels(self):
            return self._labels

        def set_label(self, label):
            self._labels.add(label)

        def unset_label(self, label):
            self._labels.remove(label)

        def has_label(self, label):
            return label in self._labels

        def merge_attr_set(self, key, val):
            merge_set = self._attrs.get(key, set())
            merge_set.add(val)
            self._attrs[key] = merge_set

        def set_attr(self, key, val):
            self._attrs[key] = val

        def has_attr(self, key):
            return key in self._attrs

        def get_attr(self, key, dflt=None):
            return self._attrs.get(key, dflt)

    def __init__(self, name=None):
        self._children = []
        self._name = name
        self._label_layers = {}

    def is_internal(self):
        return not is_leaf()

    def is_leaf(self):
        return len(self._children) == 0

    def children(self):
        return self._children

    def set_children(self, children):
        self._children = list(children)

    def get_label_layer(self, name):
        return self._label_layers.get(name, None)

    def label_layer(self, name):
        if name not in self._label_layers:
            self._label_layers[name] = self.LabelLayer()
        return self._label_layers[name]

    def label_layers(self):
        return self._label_layers

    def has_label_layer(self, name):
        return name in self._label_layers

    def label_value(self, name):
        if name in self._label_layers:
            return self._label_layers[name].value()
        return None

    def add_child(self, child):
        self._children.append(child)
        return child

    def add_children(self, children):
        for child in children:
            self.add_child(child)

    def sort_children(self):
        self._children = sorted(self._children, key= lambda x: x.name())

    def set_name(self, name):
        self._name = name

    def name(self):
        return self._name

    def __str__(self):
        return self.name()
