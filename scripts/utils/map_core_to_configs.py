import pandas as pd
import sys, os, math

if __name__=='__main__':
    log_folder = sys.argv[1]
    core = int(sys.argv[2])

    map_file = os.path.join(log_folder, 'map_core_to_configs.csv')
    core2configs = pd.read_csv(map_file)
    configs = core2configs.loc[core]
    print(f'{configs["start"]}-{configs["end"]}')
