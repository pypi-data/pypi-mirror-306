"""
TODO: Expand. For now only one test to satisfy CI/CD pipeline.
"""

import numpy as np
import logging

logging.basicConfig(level=logging.DEBUG)

from ln_ports import Port_2D_Number, Port_np_compatible, Port_3D_Number, Port_1D_Str

def _h(port, val):
    result, msg = port.check_value(val)
    assert result, msg

class TestProcessing:
    def test_port_2D_Number_valid(self):
        _h(Port_2D_Number(), np.arange(100).reshape((20, 5)))

    def test_Port_np_compatible(self):
        _h(Port_np_compatible(), np.arange(100))
        _h(Port_np_compatible(), np.arange(100).reshape((20, 5)))
        _h(Port_np_compatible(), np.arange(100).reshape((1, 20, 5)))
        _h(Port_np_compatible(), [])
        _h(Port_np_compatible(), [10])
        _h(Port_np_compatible(), [[1], [2]])

        assert Port_np_compatible.can_input_to(Port_2D_Number)
        assert Port_np_compatible.can_input_to(Port_3D_Number)
        assert not Port_np_compatible.can_input_to(Port_1D_Str)
