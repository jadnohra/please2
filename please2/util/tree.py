class TreeNode:

    class LabelLayer:
        def __init__(self, name = ''):
            self._labels = set()
            self._attrs = {}
            self._name = name

        def __str__(self):
            return self.name()

        def set_name(self, name):
            self._name = name

        def name(self):
            return self._name

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

    def __init__(self):
        self._children = set()
        self._name = None
        self._label_layers = []

    def is_internal(self):
        return not is_leaf()

    def is_leaf(self):
        return len(self._children) == 0

    def children(self):
        return self._children

    def set_children(self, children):
        self._children = set(children)

    def add_label_layer(self, name):
        self._label_layers.append(self.LabelLayer(name))
        return self.label_layer()

    def label_layers(self):
        return self._label_layers

    def label_layer_at(self, i):
        return self._label_layers[i]

    def has_label_layer(self):
        return len(self._label_layers) > 0

    def label_layer(self):
        return self._label_layers[-1] if len(self._label_layers) else None

    def is_label_layer(self, name):
        layer = self.label_layer()
        if layer is not None:
            return layer.name() == name
        return False

    def has_label(self, label):
        layer = self.label_layer()
        if layer is not None:
            return layer.has_label(label)
        return False

    def labels(self):
        layer = self.label_layer()
        if layer is not None:
            return layer.labels()
        return set()

    def add_child(self, child):
        self._children.add(child)

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
