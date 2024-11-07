from livenodes.node import Node
from ln_ports import Ports_any, Ports_empty


class Out_python(Node):
    """Saves all input data into an externally accessible list.

    Saves each process invocation into a list. I.e. if you set the input node's
    `emit_at_once=5`, you'll get list entries of size 5.

    This data can be accessed via `get_state` on this node in your Python
    process. Useful for testing other nodes or extracting results from
    LiveNodes graphs for further external processing.

    Inverse of the `In_python` node.

    Ports In
    --------
    any : Port_Any
        Input data entry to save.

    Methods
    -------
    get_state()
        Returns the saved data. Datatype of list entries depends on input data.
    reset()
        Resets the saved data to an empty list.
    """

    ports_in = Ports_any()
    ports_out = Ports_empty()

    category = "Data Sink"
    description = ""

    example_init = {"name": "Python Output"}

    def __init__(self, name="Python Output", **kwargs):
        super().__init__(name, **kwargs)
        self.reset()

    def process(self, any, **kwargs):
        self.out.append(any)

    def get_state(self):
        return self.out

    def reset(self):
        self.out = []
