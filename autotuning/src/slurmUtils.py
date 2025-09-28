import subprocess
import re
sys.path.append(str(Path(__file__).parent.parent.resolve())) 

from config import JOB_NAME


def get_num_queued_processes():
    try:
        result = subprocess.run(['sacct', str(f"--name={JOB_NAME}"), "--state=PENDING,RUNNING,SUSPENDED"], stdout=subprocess.PIPE)
        print(result.stdout)
        output = result.stdout.strip()
        count = 0
        for line in output.split('\n'):
            if "PENDING" in line:
                count += 1
            if "RUNNING" in line:
                count += 1
            if "SUSPENDED" in line:
                raise ValueError("Job is SUSPENDED, the admins will kill us")
        return count

    except Exception as e:
        print(f"Error occurred while fetching running processes: {e}")
        return 0