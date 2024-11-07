from livenodes.producer import Producer
from ln_ports import Ports_any, Ports_empty


class In_python(Producer):
    """Inputs any python data into the LiveNodes graph.

    Data should be a list of items to be sent into the graph. Each process
    invocation sends one of these items.

    Mostly for debug purposes and fast iterations. In the long run I would
    expect a custom node to always be more efficient

    Inverse of the `Out_python` node.

    Attributes
    ----------
    data : List
        List of data items to send.

    Ports Out
    ---------
    any : Port_Any
        Data list item.
    """

    ports_in = Ports_empty()
    ports_out = Ports_any()

    category = "Data Source"
    description = ""

    example_init = {"name": "Python Input"}

    def __init__(self, name="Python Input", data=[], **kwargs):
        super().__init__(name, **kwargs)
        self.data = data

    def _run(self):
        for val in self.data:
            yield self.ret(any=val)
