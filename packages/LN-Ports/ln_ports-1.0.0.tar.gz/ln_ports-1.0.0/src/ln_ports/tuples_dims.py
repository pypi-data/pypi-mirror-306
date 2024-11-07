from livenodes import Ports_collection

from .primitives import *
from .compounds import *
from .compounds_dims import *
from .compounds_typed import Port_ListUnique_Str


# --- 1D Tuples ----
class Ports_1D_Number(Ports_collection):
    d1: Port_1D_Number = Port_1D_Number("List")

class Ports_1D_Number_Channels(Ports_1D_Number):
    channels: Port_ListUnique_Str = Port_ListUnique_Str("Channel Names")


# --- 2D Tuples ----
class Ports_2D_Number(Ports_collection):
    d2: Port_2D_Number = Port_2D_Number("Time Series")

class Ports_2D_Number_Channels(Ports_2D_Number):
    channels: Port_ListUnique_Str = Port_ListUnique_Str("Channel Names")


# --- 3D Tuples ----
class Ports_3D_Number(Ports_collection):
    d3: Port_3D_Number = Port_3D_Number("Batched TS")

class Ports_3D_Number_Channels(Ports_3D_Number):
    channels: Port_ListUnique_Str = Port_ListUnique_Str("Channel Names")
