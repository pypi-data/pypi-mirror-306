import numpy as np

from .primitives import Port_Int, Port_Number, Port_Str, Port_Any
from .compounds import Port_List, Port_ListUnique

# === Typed Compounds =========================================================


# --- 1D (Lists) -------------------------------------------------------------------
class Port_1D_Int(Port_List):
    example_values = []
    compound_type = Port_Int

class Port_1D_Number(Port_List):
    example_values = []
    compound_type = Port_Number

class Port_1D_Str(Port_List):
    example_values = []
    compound_type = Port_Str

class Port_1D_Any(Port_List):
    example_values = []
    compound_type = Port_Any

class Port_1D_Unique_Str(Port_ListUnique):
    example_values = []
    compound_type = Port_Str


# --- 2D (TS / Matrices) ---------------------------------------------------------
class Port_2D_Int(Port_List):
    example_values = []
    compound_type = Port_1D_Int

class Port_2D_Number(Port_List):
    example_values = []
    compound_type = Port_1D_Number

class Port_2D_Str(Port_List):
    example_values = []
    compound_type = Port_1D_Str

class Port_2D_Any(Port_List):
    example_values = []
    compound_type = Port_1D_Any


# --- 3D (Batched TS / Multi-Channel Matrix) -------------------------------------------------------
class Port_3D_Int(Port_List):
    example_values = []
    compound_type = Port_2D_Int

class Port_3D_Number(Port_List):
    example_values = []
    compound_type = Port_2D_Number

class Port_3D_Str(Port_List):
    example_values = []
    compound_type = Port_2D_Str

class Port_3D_Any(Port_List):
    example_values = []
    compound_type = Port_2D_Any
