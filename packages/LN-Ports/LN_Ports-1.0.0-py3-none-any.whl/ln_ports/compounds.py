import numpy as np
import deprecation 

from livenodes import Port
from .primitives import Port_Any

# === Compounds ========================================================


# TODO: consider if it really makes sense to mix lists and arrays...
class Port_List(Port):
    example_values = []
    compound_type = Port_Any

    @classmethod
    def all_examples_compound_construction(cls):
        res = []
        for x in cls.compound_type.example_values:
            res.append([x])
            res.append(np.array([x]))
        return list(filter(lambda x: cls.check_value(x)[0], res))

    @classmethod
    def check_value(cls, value):
        if not (type(value) == list or isinstance(value, np.ndarray)):
            return False, f"Should be list; got {type(value)}, val: {value}."
        if len(value) > 0:
            return cls.compound_type.check_value(value[-1])
        return True, None


def has_duplicates(iterable):
    # origianlly used set(), but that prohibits unhashable items, which can still be compared via reference (ie nested lists)
    seen = []
    for x in iterable:
        if x in seen:
            return True
        seen.append(x)
    return False


class Port_ListUnique(Port_List):
    example_values = [["EMG1", "EMG2"], [0, 1], [20, 0.1]]
    compound_type = Port_Any
    label = 'Unique List'

    @classmethod
    def check_value(cls, value):
        if type(value) != list:
            return False, f"Should be list; got {type(value)}, val: {value}."
        elif has_duplicates(value):
            return False, "There should not be any duplicates;"
        elif len(value) > 0:
            return cls.compound_type.check_value(value[-1])
        return True, None


class Port_Dict(Port):
    example_values = [{}, {'name': 'f', 'va': 5}]
    label = 'Meta'

    @classmethod
    def check_value(cls, value):
        if type(value) != dict:
            return False, f"Should be dict; got {type(value)}, val: {value}."
        return True, None


class _Port_np_compatible_base(Port):
    example_values = [1, [-1, 2], -0.5, np.array([[1]]), np.array([[[1, 2], [3, 4]]])]

    @classmethod
    def check_value(cls, value):
        try:
            arr = np.array(value)
            if not np.issubdtype(arr.dtype, np.number):
                return False, "Numpy array is not numerical"
        except Exception as err:
            print(err)
            return False, "Could not convert to numpy array"
        return True, None

class Port_np_compatible(_Port_np_compatible_base, Port_List):
    example_values = []
    compound_type = _Port_np_compatible_base
    label = 'NP Comp.'




@deprecation.deprecated(deprecated_in="0.12.1", removed_in="1.0",
                        details="Use the dim ports instead")
class Port_Timeseries(Port):
    example_values = [np.array([[1]])]
    label = 'TimeSeries'

    @staticmethod
    def check_value(value):
        if not isinstance(value, np.ndarray):
            return False, "Should be numpy array;"
        elif len(value.shape) != 2:
            return False, "Shape should be of length two (Time, Channel);"
        return True, None
