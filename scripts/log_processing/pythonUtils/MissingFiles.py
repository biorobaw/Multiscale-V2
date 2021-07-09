from os.path import isfile as exists
from os.path import join as join_path
from os import listdir
from sys import argv
import re
import pandas as pd

if __name__ == '__main__':

    log_folder = argv[1]
    configs_folder = join_path(log_folder, 'configs', '')
    search_file = configs_folder + '{}/' + argv[2].replace('#ID', '{}')    
    all_configs = pd.read_csv(join_path(log_folder,'configs.csv'),sep='\t')

    missing_ids = [ str(index) for index, row in all_configs.iterrows()
                                if not exists(search_file.format(row['config'], row['run_id']))]

    total_missing = len(missing_ids)
    print()
    print(f'TOTAL MISSING: {total_missing} / {len(all_configs)}')
    print()
    if total_missing > 0:
        print('missingIds: ', ','.join(missing_ids))

    print()
