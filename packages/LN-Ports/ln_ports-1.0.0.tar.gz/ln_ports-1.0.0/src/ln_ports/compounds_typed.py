import numpy as np

from .primitives import Port_Int, Port_Number, Port_Str, Port_Any
from .compounds import Port_List, Port_ListUnique

# === Typed Compounds =========================================================


# --- Lists -------------------------------------------------------------------
class Port_List_Int(Port_List):
    example_values = []
    compound_type = Port_Int


class Port_List_Number(Port_List):
    example_values = []
    compound_type = Port_Number


class Port_List_Str(Port_List):
    example_values = []
    compound_type = Port_Str


class Port_List_Any(Port_List):
    example_values = []
    compound_type = Port_Any


class Port_ListUnique_Str(Port_ListUnique):
    example_values = []
    compound_type = Port_Str


# --- Legacy Matrices ---------------------------------------------------------
class Port_Matrix_Int(Port_List):
    example_values = []
    compound_type = Port_List_Int


class Port_Matrix_Number(Port_List):
    example_values = []
    compound_type = Port_List_Number


class Port_Matrix_Str(Port_List):
    example_values = []
    compound_type = Port_List_Str


class Port_Matrix_Any(Port_List):
    example_values = []
    compound_type = Port_List_Any


# --- Legacy TimeSeries -------------------------------------------------------
class Port_TS_Int(Port_List):
    example_values = []
    compound_type = Port_Matrix_Int


class Port_TS_Number(Port_List):
    example_values = []
    compound_type = Port_Matrix_Number


class Port_TS_Str(Port_List):
    example_values = []
    compound_type = Port_Matrix_Str


class Port_TS_Any(Port_List):
    example_values = []
    compound_type = Port_Matrix_Any


# --- Legacy Batched TimeSeries -----------------------------------------------
class Port_BTS_Int(Port_List):
    example_values = []
    compound_type = Port_TS_Int


class Port_BTS_Number(Port_List):
    example_values = []
    compound_type = Port_TS_Number


class Port_BTS_Str(Port_List):
    example_values = []
    compound_type = Port_TS_Str


class Port_BTS_Any(Port_List):
    example_values = []
    compound_type = Port_TS_Any
