from pathlib import Path
import re
import pandas as pd
csv_path = Path("/home/tiep_nguyen/IndySCC-HPL-Scripts/analysis/output.csv")


# designed to match with output from HPL_pdtest.C
pattern = re.compile(
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


'''
TODO, write documentation on this type of result
'''
def process_hpl_output(file : Path) -> pd.DataFrame:
    results=[]
    with file.open(mode='r', encoding='utf-8') as f:
        
        data = f.readlines()
        for i in range(len(data)):
            curLine = data[i]
            match = pattern.match(curLine)
            #print(curLine)
            if match:
                result = match.groupdict()
                # convert numeric fields
                print(result)
                results.append(result)
    current_data = None
    try:
        current_data = pd.read_csv(csv_path)
        current_data=pd.concat([current_data, pd.DataFrame(results)], ignore_index=True)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        current_data=pd.DataFrame(results)
    
    current_data["Gflops"] = current_data["Gflops"].astype(float)


    return current_data
    