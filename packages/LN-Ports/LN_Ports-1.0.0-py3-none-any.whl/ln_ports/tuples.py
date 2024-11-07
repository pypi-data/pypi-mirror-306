from livenodes import Ports_collection
import deprecation
import warnings

from .primitives import *
from .compounds import *
from .compounds_typed import *

# --- Common Constellations ----
class Ports_empty(Ports_collection):
    pass

class Ports_any(Ports_collection):
    any: Port_Any = Port_Any("Any")

class Ports_np(Ports_collection):
    data_np: Port_np_compatible = Port_np_compatible("Data NP")



# --- To be deprecated / replaced by tuple_dims ---
@deprecation.deprecated(deprecated_in="0.12.1", removed_in="1.0", details="Use the dim ports instead")
class Ports_BTS_data_channels(Ports_collection):
    data: Port_BTS_Number = Port_BTS_Number("Data")
    channels: Port_ListUnique_Str = Port_ListUnique_Str("Channel Names")

@deprecation.deprecated(deprecated_in="0.12.1", removed_in="1.0", details="Use the dim ports instead")
class Ports_ts(Ports_collection):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        ts: Port_Timeseries = Port_Timeseries("TimeSeries")

@deprecation.deprecated(deprecated_in="0.12.1", removed_in="1.0", details="Use the dim ports instead")
class Ports_ts_channels(Ports_collection):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        ts: Port_Timeseries = Port_Timeseries("TimeSeries")
        channels: Port_ListUnique_Str = Port_ListUnique_Str("Channel Names")
