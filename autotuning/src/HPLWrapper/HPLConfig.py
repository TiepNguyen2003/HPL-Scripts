from enum import Enum
import string
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent.resolve())) 

from dataclasses import dataclass, field, fields
from typing import List
from skopt.space import Space, Real, Integer, Categorical
from config import MAXIMUM_HPL_N, NUM_PROCESS

#region Enums
class PMapEnum(Enum):
    Row = 0
    Column = 1

class BCastEnum(Enum):
    OneRing = 0
    OneRingM = 1
    TwoRing = 2
    TwoRingM = 3
    Blong = 4
    BlongM = 5
class PFactEnum(Enum):
    Left = 0
    Crout = 1
    Right = 2
class RFactEnum(Enum):
    Left = 0
    Crout = 1
    Right = 2

class SwapEnum(Enum):
    BinExch = 0
    Long = 1
    Mix = 2
#endregion
@dataclass
class HPLConfig:
    N_Array: List[int]  # line 5-6
    NB_Array: List[int] # line 7-8
    P_Array: List[int]  # line 11
    Q_Array: List[int] # line 12
    NBMin_Array: List[int] # line 16-17
    NDIV_Array: List[int]  # line 18-19
    Output_Name: str = "output.log"
    Device_Out: str = "6" # 6 for stdout, 7 for stin, file for file
    PMAP_Process_Mapping: PMapEnum = PMapEnum.Row  # (0 = row, 1 = column-major) # line 9
    Threshold: float = 16.0 # line 13
    PFact_Array: set[PFactEnum] = field(default_factory=lambda: {PFactEnum.Left, PFactEnum.Crout, PFactEnum.Right}) # line 14-15
    RFact_Array: set[RFactEnum] = field(default_factory=lambda: {RFactEnum.Left, RFactEnum.Crout, RFactEnum.Right})  # (0=left, 1=Crout, 2=Right) line 20-21
    BCAST_Array: set[BCastEnum] = field(default_factory=lambda: {BCastEnum.OneRing})  # (0=1rg,1=1rM,2=2rg,3=2rM,4=Lng,5=LnM) line 22-23
    Depth_Array: set[int] = field(default_factory=lambda: {0}) # line 24-25
    Swap_Type: SwapEnum = SwapEnum.BinExch  # 0=bin-exch,1=long,2=mix # line 26
    Swap_Threshold: int = 64 # line 27
    L1_Form: int = 0  # 0=transposed,1=no-transpose line 28
    U_Form: int = 0  # 0=transposed,1=no-transpose line 29
    Equilibration_Enabled: bool = True  # (False = no, True = yes) line 30
    MemoryAlignment: int = 8 # line 31

    '''Defines if HPL Config is valid (although not necessarily on this machine)'''
    def isValid(self) -> bool:
        # validate types
        for val in self.PFact_Array:
            if isinstance(val,PFactEnum) is False:
                raise ValueError("PFact not enum")

        for val in self.RFact_Array:
            if isinstance(val,RFactEnum) is False:
                raise ValueError("Rfact not enum")
        
        for val in self.BCAST_Array:
            if isinstance(val,BCastEnum) is False:
                raise ValueError("Bcast not enum")
        
        if isinstance(self.PMAP_Process_Mapping, PMapEnum) is False:
            raise ValueError("PMAP not enum")
        
        if self.L1_Form < 0 or self.L1_Form > 1:
            raise ValueError("L1_Form not 0 or 1")
        
        if self.U_Form < 0 or self.U_Form > 1:
            raise ValueError("U_Form not 0 or 1")
        
        # conditional logic
        if (len(self.P_Array) != len(self.Q_Array)):
            return False
        
        return True

    def __eq__(self, other):
       if not isinstance(other, HPLConfig):
           return NotImplemented
       return self.__dict__ == other.__dict__
    def __post_init__(self):
        # auto-convert int to Enum
        self.PFact_Array = {PFactEnum(x) if isinstance(x, int) else x for x in self.PFact_Array}
        self.RFact_Array = {RFactEnum(x) if isinstance(x, int) else x for x in self.RFact_Array}
        self.BCAST_Array = {BCastEnum(x) if isinstance(x, int) else x for x in self.BCAST_Array}

        self.Swap_Type = SwapEnum(self.Swap_Type) if isinstance(self.Swap_Type, int) else self.Swap_Type
        if isinstance(self.PMAP_Process_Mapping, int):
            self.PMAP_Process_Mapping = PMapEnum(self.PMAP_Process_Mapping)

        # validate types

        for val in self.PFact_Array:
            if isinstance(val,PFactEnum) is False:
                raise ValueError("PFact not enum")

        for val in self.RFact_Array:
            if isinstance(val,RFactEnum) is False:
                raise ValueError("Rfact not enum")
        
        for val in self.BCAST_Array:
            if isinstance(val,BCastEnum) is False:
                raise ValueError("Bcast not enum")
        
        if isinstance(self.PMAP_Process_Mapping, PMapEnum) is False:
            raise ValueError("PMAP not enum")

        print(self.NDIV_Array)
        for val in self.NDIV_Array:
            
            if val < 2:
                raise ValueError("NDIV less than 2")
        
        

'''Class describes  an HPL run'''
@dataclass
class HPL_Run:
    source_file : string # name of the hpl.dat file
    N: int
    NB: int
    PMAP_Process_Mapping: PMapEnum
    P: int # nprow
    Q: int # ncol
    Threshold: float 
    Equilibration_Enabled: bool 
    BCast: BCastEnum # ctop  
    PFact: PFactEnum # cpfact
    RFact: RFactEnum # crfact
    Nbmin: int
    Nbdiv: int

    Depth: int
    wTime: float
    Align: float
    SwapType: SwapEnum
    L1: int
    U: int
    Gflops: float

    def __post_init__(self):
        # auto-convert int to Enum
        if isinstance(self.BCast, int):
            self.BCast = BCastEnum(self.BCast)
        if isinstance(self.PFact, int):
            self.PFact = PFactEnum(self.PFact)
        if isinstance(self.RFact, int):
            self.RFact = RFactEnum(self.RFact)
        if isinstance(self.PMAP_Process_Mapping, int):
            self.PMAP_Process_Mapping = PMapEnum(self.PMAP_Process_Mapping)
        if isinstance(self.SwapType, int):
            self.SwapType = SwapEnum(self.SwapType)
        

        self.N = int(self.N)
        self.NB = int(self.NB)
        self.P = int(self.P)
        self.Q = int(self.Q)
        self.Equilibration_Enabled = bool(self.Equilibration_Enabled)
        self.Threshold = float(self.Threshold)
        self.Nbdiv = int(self.Nbdiv)
        self.Nbmin = int(self.Nbmin)
        self.Depth = int(self.Depth)
        self.wTime = float(self.wTime)
        self.Align = float(self.Align)
        self.L1 = int(self.L1)
        self.U = int(self.U)
        self.Gflops = float(self.Gflops)
        
