import sys
from pathlib import Path
import re
from typing import List
import pandas as pd
csv_path = Path("/home/tiep_nguyen/IndySCC-HPL-Scripts/analysis/output.csv")
from HPLConfig import HPLConfig, HPL_Run, BCastEnum, PFactEnum, RFactEnum, PMapEnum, SwapEnum

def is_hpl_config(file: Path) -> bool:
    results=[]
    with file.open(mode='r', encoding='utf-8') as f:
        data = f.readlines()
        for i in range(min(len(data), 5)):
            curLine = data[i]
            if "High-Performance Linpack benchmark" in str(curLine):
                return True 
        return False


# designed to match with output from HPL_pdtest.C
hpl_result_regex = re.compile(
    r"W(?P<order>[RC])"         # 'R' or 'C'
    r"(?P<depth>\d)"            # algorithm depth
    r"(?P<ctop>.)"              # char
    r"(?P<crfact>.)"            # char
    r"(?P<nbdiv>\d)"            # int
    r"(?P<cpfact>.)"            # char
    r"(?P<nbmin>\d)"            # int
    r"\s*(?P<N>\d+)"            # int
    r"\s+(?P<NB>\d+)"           # int
    r"\s+(?P<nprow>\d+)"        # int
    r"\s+(?P<npcol>\d+)"        # int
    r"\s+(?P<wtime>[-+]?\d*\.\d+)"  # float
    r"\s+(?P<Gflops>[-+]?\d*\.\d+(?:[eE][-+]?\d+)?)" # scientific float
)

hpl_residual_regex = re.compile(
    r"\|\|Ax-b\|\|_oo/\(eps\*\(\|\|A\|\|_oo\*\|\|x\|\|_oo\+\|\|b\|\|_oo\)\*N\)=\s+"
    r"(?P<residual>[+\-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+\-]?\d+)?)"
    r"\s+\.{6}\s+"
    r"(?P<status>PASSED|FAILED)"
)

'''
TODO, write documentation on this type of result
'''
def process_hpl_output(file : Path) -> pd.DataFrame:
    if is_hpl_config(file) == False:
        raise ValueError("{file} is not an HPLConfig")
    
    results=[]
    with file.open(mode='r', encoding='utf-8') as f:
        data = f.readlines()
        for i in range(len(data)):
            curLine = data[i]
            match = hpl_result_regex.match(curLine)
            #print(curLine)
            if match:
                result = match.groupdict()
                # convert numeric fields
                #print(result)
                results.append(result)
    current_data = None
    try:
        current_data = pd.read_csv(csv_path)
        current_data=pd.concat([current_data, pd.DataFrame(results)], ignore_index=True)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        current_data=pd.DataFrame(results)
    
    current_data["Gflops"] = current_data["Gflops"].astype(float)


    return current_data
#https://github.com/learnbyexample/py_regular_expressions
hpl_config_regex= re.compile(r"(\w+)\s*:\s*(.+)")


def get_hpl_config(file : Path) -> HPLConfig:

    if is_hpl_config(file) == False:
        raise ValueError("{file} is not an HPLConfig")
    
    # reading
    with file.open(mode='r', encoding='utf-8') as f:
        fullcontent = f.readlines()
        configContent=fullcontent[17:36] # based off of test_samples hpl_output
        print("Reading results")
        results = {}
        for i in range(len(configContent)):
            curLine = configContent[i]
            #print(curLine)
            match = re.match(hpl_config_regex, curLine)
            if match:
                key, value = match.groups()
                #print("key =", key)
                #print("value =", value)
                results[key]=value
    print(results)
    # preprocessing
    results['N'] = int(results['N'])
    results['NB'] = int(results['NB'])

    if results['PMAP'] == 'Row-major process mapping':
        results['PMAP'] = 0
    elif results['PMAP'] == 'Column-major process mapping':
        results['PMAP'] = 1
    else:
        raise ValueError("Unknown PMAP value: " + results['PMAP'])
    results['P'] = int(results['P'])
    results['Q'] = int(results['Q'])
    results['NDIV'] = int(results['NDIV'])

    results['DEPTH'] = int(results['DEPTH'])

    if "Binary" in str(results['SWAP']):
        results['SWAP'] = SwapEnum.BinExch
    if "Long" in str(results['SWAP']):
        results['SWAP'] = SwapEnum.Long
    if "Mix" in str(results['SWAP']):
        results['SWAP'] = SwapEnum.Mix

    if "no" not in str(results['L1']):
        results['L1'] = 0
    else:
        results['L1'] = 1

    if "no" not in str(results['U']):
        results['U'] = 0
    else:
        results['U'] = 1

    if "yes" in str(results['EQUIL']):
        results['EQUIL'] = True
    else:
        results['EQUIL'] = False

    alignNumbers = re.findall(r"\d+", results['ALIGN'])
    if (len(alignNumbers) > 1):
        raise ValueError("Multiple numbers found in ALIGN: " + results['ALIGN'])

    Pfact_Array = []

    if ("Left" in str(results['PFACT'])):
        Pfact_Array.append(0)
    if ("Crout" in str(results['PFACT'])):
        Pfact_Array.append(1)
    if ("Right" in str(results['PFACT'])):
        Pfact_Array.append(2)
    
    Rfact_Array = []

    if ("Left" in str(results['RFACT'])):
        Rfact_Array.append(0)
    if ("Crout" in str(results['RFACT'])):
        Rfact_Array.append(1)
    if ("Right" in str(results['RFACT'])):
        Rfact_Array.append(2)
    
    Bcast_Array = []

    if (bool(re.search(r"1ring\s", str(results['BCAST'])))):
        Bcast_Array.append(0)
    if (bool(re.search(r"1ringM\s", str(results['BCAST'])))):
        Bcast_Array.append(1)
    if (bool(re.search(r"2ring\s", str(results['BCAST'])))):
        Bcast_Array.append(2)
    if (bool(re.search(r"2ringM\s", str(results['BCAST'])))):
        Bcast_Array.append(3)
    if (bool(re.search(r"Blong\s", str(results['BCAST'])))):
        Bcast_Array.append(4)
    if (bool(re.search(r"BlongM\s", str(results['BCAST'])))):
        Bcast_Array.append(5)

    # object to return
    config = HPLConfig(
        N_Array=[results['N']],
        NB_Array=[results['NB']],
        PMAP_Process_Mapping=results['PMAP'],
        P_Array=[results['P']],
        Q_Array=[results['Q']],
        PFact_Array=Pfact_Array,
        NBMin_Array=[1, 2], #TODO
        NDIV_Array=[results['NDIV']],
        RFact_Array=Rfact_Array,
        BCAST_Array=Bcast_Array,
        Depth_Array=[results['DEPTH']],
        Swap_Type=results['SWAP'],
        L1_Form=results['L1'],
        U_Form=results['U'],
        Equilibration_Enabled=results['EQUIL'],
        MemoryAlignment=int(alignNumbers[0])
    )
    return config

def get_hpl_runs(file : Path) -> List[HPL_Run]:

    if is_hpl_config(file) == False:
        raise ValueError("{file} is not an HPLConfig")
    config = get_hpl_config(file)

    results=[]
    residuals=[]
    with file.open(mode='r', encoding='utf-8') as f:
        data = f.readlines()
        for i in range(len(data)):
            curLine = data[i]
            match = hpl_result_regex.match(curLine)
            #print(curLine)
            if match:
                result = match.groupdict()
                 # convert numeric fields
                #print(result)
                results.append(result)
            
            match = hpl_residual_regex.match(curLine)
            if match:
                residual = match.groupdict()
                residuals.append(residual)
    
    if (len(residuals) != len(results)):
        raise ValueError("Number of residuals does not match number of results")

    runs = []
    for i in range(len(results)):
        result = results[i]
        residual = residuals[i]
        print(result)

        result['Gflops'] = float(result['Gflops'])

        if "L" in str(result['cpfact']):
            result['cpfact'] = PFactEnum.Left
        elif "R" in str(result['cpfact']):
            result['cpfact'] = PFactEnum.Right
        elif "C" in str(result['cpfact']):
            result['cpfact'] = PFactEnum.Crout

        if "L" in str(result['crfact']):
            result['crfact'] = RFactEnum.Left
        elif "R" in str(result['crfact']):
            result['crfact'] = RFactEnum.Right
        elif "C" in str(result['crfact']):
            result['crfact'] = RFactEnum.Crout

        run = HPL_Run(
            source_file = str(file),
            N=result['N'],
            NB=result['NB'],
            PMAP_Process_Mapping=config.PMAP_Process_Mapping,
            P=result['nprow'],
            Q=result['npcol'],
            Threshold= config.Threshold,
            Equilibration_Enabled=config.Equilibration_Enabled,
            BCast=int(result['ctop']), # ctop  
            PFact=result['cpfact'], # cpfact
            RFact=result['crfact'], # crfact
            Nbdiv=result['nbdiv'], 
            Depth=result['depth'],
            wTime=result['wtime'],
            Gflops=result['Gflops'],
            Align=config.MemoryAlignment,
            L1=config.L1_Form,
            U=config.U_Form,
            SwapType=config.Swap_Type
        )
        runs.append(run)
    return runs
    



    