import subprocess
import re
import sys
sys.path.append(str(Path(__file__).parent.parent.resolve())) 

from config import JOB_NAME

# Gets the number of queued processes text output of sacct
def get_num_queued_processes(stdout):
    for line in stdout.split('\n'):
            if "PENDING" in line:
                count += 1
            if "RUNNING" in line:
                count += 1
            if "SUSPENDED" in line:
                raise ValueError("Job is SUSPENDED, the admins will kill us")
    return count


