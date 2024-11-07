import numbers
from livenodes.components.port import Port, ALL_VALUES
import numpy as np


# === Special Case Any ========================================================
class Port_Any(Port):
    example_values = ALL_VALUES
    label = 'Any'

    @classmethod
    def check_value(cls, value):
        return True, None


# === Primitives ==============================================================


class Port_Int(Port):
    example_values = [0, 1, np.array([1])[0]]
    label = 'Int'

    @classmethod
    def check_value(cls, value):
        if not isinstance(value, int):
            try:
                if np.issubdtype(value, np.integer):
                    return True, None
                else:
                    return False, f"Should be int; got {type(value)}, val: {value}."
            except:
                return False, f"Should be int; got {type(value)}, val: {value}."
        return True, None


class Port_Number(Port):
    example_values = [0, 0.5, 20, np.array([1])[0]]
    label = 'Number'

    @classmethod
    def check_value(cls, value):
        if not isinstance(value, numbers.Number):
            return False, f"Should be number; got {type(value)}, val: {value}."
        return True, None


class Port_Str(Port):
    example_values = ["Some example value", "another_one", np.array(['test'])[0]]
    label = "Text"

    @classmethod
    def check_value(cls, value):
        if not isinstance(value, str):
            return False, f"Should be string; got {type(value)}, val: {value}."
        return True, None


class Port_Bool(Port):
    example_values = [True, False, np.array([True])[0]]
    label = 'Bool'

    @classmethod
    def check_value(cls, value):
        if not (isinstance(value, bool) or isinstance(value, np.bool_)):
            return False, f"Should be boolean ;got {type(value)}, val: {value}."
        return True, None
