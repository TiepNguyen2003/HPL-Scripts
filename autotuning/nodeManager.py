import time
from pssh.clients import SSHClient
from pathlib import Path
import re
import logging

logname = 'node_manager.log'

logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')


CHECK_INTERVAL = 5*60  # seconds

def check_slurm_jobs(client : SSHClient):
    cmd = 'squeue --user=tnguyen668 --name=hpl_autotuning_train --format="%.18i %.8j %.8u %.2t %.10M %.6D %R"'
    output = client.run_command(cmd)

    i = 0
    jobs = []
    for line in output.stdout:
        i += 1
        logging.info(line)

        if (i < 3): # skip header lines
            continue
        parts = line.split()
        keys = ['JOBID', 'NAME', 'USER', 'STATE', 'TIME', 'NODES', 'NODELIST(REASON)']
        job_info = dict(zip(keys, parts))
        jobs.append(job_info)

    return jobs

# Submits a batch job to slurm and returns the job id
def submit_batch_job(client : SSHClient, rank : int) -> int:
    cmd = f'sbatch --export=HPL_RANK={rank + 1} /home/tnguyen668/software/HPL-Scripts/autotuning/train_batch.sh'
    output = client.run_command(cmd)
    jobid=0
    for line in output.stdout:
        match = re.search(r"Submitted batch job (\d+)", line)
        if match:
            jobid = match.group(1)
            logging.info(f"Submitted batch job {jobid}")
            return int(jobid)
    raise ValueError("Failed to submit job")
MAX_PROCESSES= 4
knownProcessList = [0] * MAX_PROCESSES


if __name__ == "__main__":
    # Read process list

    LOCAL_USER = 'tnguyen668'

    LOCAL_PASSWORD = input('Enter password for user ' + LOCAL_USER + ': ')

    host = 'login.rc.ucmerced.edu'
    client = SSHClient(host, user=LOCAL_USER, password=LOCAL_PASSWORD)


    while True:
        logging.info("Checking SLURM jobs..." )
        jobs = check_slurm_jobs(client)
        
        job_ids = []
        for job in jobs:
            job_id = int(job['JOBID'])
            job_ids.append(job_id)

        if (len(job_ids) <= MAX_PROCESSES): # sanity check to ensure not overloading
            for i in range(MAX_PROCESSES):
                if knownProcessList[i] != 0 and knownProcessList[i] not in job_ids:
                    logging.info(f"Process {knownProcessList[i]} finished, slot {i} is now free")
                    knownProcessList[i] = 0

            for i in range(MAX_PROCESSES):
                if knownProcessList[i] == 0:
                    for job_id in job_ids:
                        if job_id not in knownProcessList:
                            logging.info(f"Process {job_id} exists, adding to free slot {i}")
                            knownProcessList[i] = job_id
                            break

            for i in range(MAX_PROCESSES):
                if knownProcessList[i] == 0:
                    job_id = submit_batch_job(client, i)
                    knownProcessList[i] = job_id
        
        time.sleep(CHECK_INTERVAL)

