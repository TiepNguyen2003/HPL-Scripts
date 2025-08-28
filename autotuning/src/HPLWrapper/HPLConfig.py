import sys
from pathlib import Path


from dataclasses import dataclass, field
from typing import List

@dataclass
class HPLConfig:
    Output_Name: str = "output.log"
    Device_Out: str = "6" # 6 for stdout, 7 for stin, file for file
    N_Array: List[int] = field(default_factory=list)  # line 5-6
    NB_Array: List[int] = field(default_factory=list) # line 7-8
    PMAP_Process_Mapping: int = 0  # (0 = row, 1 = column-major) # line 9
    P_Array: List[int] = field(default_factory=list) # line 11
    Q_Array: List[int] = field(default_factory=list) # line 12
    Threshold: float = 16.0 # line 13
    PFact_Array: List[int] = field(default_factory=lambda: [0, 1, 2]) # line 14-15
    NBMin_Array: List[int] = field(default_factory=list) # line 16-17
    NDIV_Array: List[int] = field(default_factory=list) # line 18-19
    RFact_Array: List[int] = field(default_factory=lambda: [0, 1, 2])  # (0=left, 1=Crout, 2=Right) line 20-21
    BCAST_Array: List[int] = field(default_factory=lambda: [0])  # (0=1rg,1=1rM,2=2rg,3=2rM,4=Lng,5=LnM) line 22-23
    Depth_Array: List[int] = field(default_factory=lambda: [0]) # line 24-25
    Swap_Type: int = 0  # 0=bin-exch,1=long,2=mix # line 26
    Swap_Threshold: int = 60 # line 27
    L1_Form: int = 0  # 0=transposed,1=no-transpose line 28
    U_Form: int = 0  # 0=transposed,1=no-transpose line 29
    Equilibration_Enabled: bool = True  # (False = no, True = yes) line 30
    MemoryAlignment: int = 8 # line 31

    def isValid(self) -> bool:

        if (len(self.P_Array) != len(self.Q_Array)):
            return False
        return True
