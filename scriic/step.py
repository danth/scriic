from .errors import UnsetDisplayIndexException


class Step:
    """
    A tree node which represents an instruction.

    :param text_elements: Text, values and UnknownValues to concatenate
        together when this step is displayed

    :var children: List of child steps
    :var display_index: Set this to a number or string when this step is
        displayed. It is used in future steps to tell the user to refer back
        to this step.
    """

    def __init__(self, *text_elements):
        self.text_elements = text_elements
        self.children = list()

        # This is set to the step number when it is displayed
        self.display_index = None

    def __repr__(self):
        if self.display_index is None:
            raise UnsetDisplayIndexException(
                'Display index not set, cannot reference step')

        return f'step {self.display_index}'

    def text(self):
        """
        Return the concatenated text of this step.

        May require some previous steps to have been displayed if they are
        referenced from this step.
        """
        text = str()
        for element in self.text_elements:
            text += str(element)
        return text

    def add_child(self, *args, **kwargs):
        """
        Create a new Step and add it as a child of this one.

        :returns: Created step
        """
        child = Step(*args, **kwargs)
        self.children.append(child)
        return child

    def leaf_nodes(self):
        """Yield the leaves which are descendants of this step."""
        if len(self.children) > 0:
            for child in self.children:
                # Recursively call leaf_nodes on each child
                for leaf in child.leaf_nodes():
                    yield leaf
        else:
            # We are a leaf node
            yield self