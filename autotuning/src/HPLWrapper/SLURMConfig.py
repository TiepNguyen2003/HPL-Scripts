from dataclasses import dataclass, field
from pathlib import Path
@dataclass
class SLURMConfig:
    Nodes : int = 1
    Partition : str = "test"
    Alloc_GB : int = 0 # allocated memory in GB, 0 means use entire
    Time : str = "01:00:00" # HH:MM:SS
    Ntasks_perNode : int = 1
    OutputFile : Path = field(default_factory=Path)
    Job_Name : str = "HPL"
    Mail_User : str = "user@example.com"
    Mail_Type : str = "ALL"
    
    @property
    def Alloc_MB(self) -> int:
        return self.Alloc_GB * 1024

    def isValid(self):
        print("Warning, slurm config validation not complete")
        return True