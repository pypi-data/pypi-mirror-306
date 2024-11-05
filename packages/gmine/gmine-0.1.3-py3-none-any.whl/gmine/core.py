import pandas as pd

from .regex import satisfy

def labour(fpath: str, col: str, cnf: str, nfname: str):
    df = pd.read_csv(fpath, low_memory=False)
    mask = df[col].apply(lambda x: satisfy(x, cnf))
    df = df[mask]
    df.to_csv(nfname, index=False)






