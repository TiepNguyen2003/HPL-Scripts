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
    r"(?P<nbdiv>\d+)"            # int
    r"(?P<cpfact>.)"            # char
    r"(?P<nbmin>\d+)"            # int
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
    
    hpl_runs : List[HPL_Run] = get_hpl_runs(file)
    df = pd.DataFrame([run.__dict__ for run in hpl_runs])

    
    return df
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
    results['N'] = list(map(int,results['N'].split()))
    results['NB'] = list(map(int,results['NB'].split()))

    if results['PMAP'] == 'Row-major process mapping':
        results['PMAP'] = PMapEnum.Row
    elif results['PMAP'] == 'Column-major process mapping':
        results['PMAP'] = PMapEnum.Column
    else:
        raise ValueError("Unknown PMAP value: " + results['PMAP'])
    results['P'] = list(map(int,results['P'].split()))
    results['Q'] = list(map(int,results['Q'].split()))
    results['NDIV'] = list(map(int,results['NDIV'].split()))
    results['NBMIN'] = list(map(int,results['NBMIN'].split()))


    results['DEPTH'] = list(map(int,results['DEPTH'].split()))

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
        N_Array=results['N'],
        NB_Array=results['NB'],
        PMAP_Process_Mapping=results['PMAP'],
        P_Array=results['P'],
        Q_Array=results['Q'],
        PFact_Array=Pfact_Array,
        NBMin_Array=results['NBMIN'], #TODO
        NDIV_Array=results['NDIV'],
        RFact_Array=Rfact_Array,
        BCAST_Array=Bcast_Array,
        Depth_Array=results['DEPTH'],
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

    curResult = None
    curResidual = None
    runs = []
    with file.open(mode='r', encoding='utf-8') as f:
        data = f.readlines()
        for i in range(len(data)):
            curLine = data[i]
            match = hpl_result_regex.match(curLine)
            #print(curLine)
            if match:
                if curResult is not None:
                    raise ValueError(f"Read result at line {i+1} while previous result exists")
                curResult = match.groupdict()
                continue
            
            match = hpl_residual_regex.match(curLine)
            if match:
                curResidual = match.groupdict()
                if curResult is None:
                    raise ValueError(f"Read residual at line {i+1} without previous match")
                curResult['Gflops'] = float(curResult['Gflops'])

                if "L" in str(curResult['cpfact']):
                    curResult['cpfact'] = PFactEnum.Left
                elif "R" in str(curResult['cpfact']):
                    curResult['cpfact'] = PFactEnum.Right
                elif "C" in str(curResult['cpfact']):
                    curResult['cpfact'] = PFactEnum.Crout

                if "L" in str(curResult['crfact']):
                    curResult['crfact'] = RFactEnum.Left
                elif "R" in str(curResult['crfact']):
                    curResult['crfact'] = RFactEnum.Right
                elif "C" in str(curResult['crfact']):
                    curResult['crfact'] = RFactEnum.Crout

                curResidual['residual'] = float(curResidual['residual'])
                curResidual['status'] = True if "PASSED" in str(curResidual) else False
                run = HPL_Run(
                    source_file = str(file),
                    N=curResult['N'],
                    NB=curResult['NB'],
                    PMAP_Process_Mapping=config.PMAP_Process_Mapping,
                    P=curResult['nprow'],
                    Q=curResult['npcol'],
                    Threshold= config.Threshold,
                    Equilibration_Enabled=config.Equilibration_Enabled,
                    BCast=int(curResult['ctop']), # ctop  
                    PFact=curResult['cpfact'], # cpfact
                    RFact=curResult['crfact'], # crfact
                    Nbdiv=curResult['nbdiv'], 
                    Nbmin=curResult['nbmin'],
                    Depth=curResult['depth'],
                    wTime=curResult['wtime'],
                    Gflops=curResult['Gflops'],
                    Align=config.MemoryAlignment,
                    L1=config.L1_Form,
                    U=config.U_Form,
                    SwapType=config.Swap_Type,
                    residual=curResidual['residual'],
                    passed=curResidual['status']

                )
                #print(f"Run {i} " + str(run))
                runs.append(run)

                curResidual = None
                curResult = None
    return runs
    

def process_hpl_csv(path : Path) -> pd.DataFrame:
    df = pd.read_csv(path)

    # Check dataframe
    # TODO, implement dataframe check
    #

    df['PMAP_Process_Mapping']= df['PMAP_Process_Mapping'].map(lambda c: PMapEnum[c.split(".")[1]])
    df['BCast'] = df['BCast'].map(lambda c: BCastEnum[c.split(".")[1]])
    df['PFact'] = df['PFact'].map(lambda c: PFactEnum[c.split(".")[1]])
    df['RFact'] = df['RFact'].map(lambda c: RFactEnum[c.split(".")[1]])
    df['SwapType'] = df['SwapType'].map(lambda c: SwapEnum[c.split(".")[1]])

    return df


    