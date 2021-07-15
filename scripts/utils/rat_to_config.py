import pandas as pd
import sys, os

if __name__=='__main__':
    config_file = sys.argv[1]
    rat = int(sys.argv[2])
    rats = pd.read_csv(config_file, sep="\t")
    print(rats['config'][rat][1:])

