import pandas as pd
import sys, os, math

if __name__=='__main__':
    log_folder = sys.argv[1]
    rats_per_core = int(sys.argv[2])
    min_config = int(sys.argv[3])
    max_config = int(sys.argv[4])

    config_file = os.path.join(log_folder, 'configs.csv')
    save_file = os.path.join(log_folder, 'map_core_to_configs.csv')


    rats = pd.read_csv(config_file, sep="\t")
    total_cores = math.ceil(float(len(rats))/rats_per_core)


    rats['config'] = rats['config'].map( lambda s : int(s[1:]))
    rats = rats[['config','run_id']].groupby('config').count()

    start = 0
    core_ranges = []
    current_count = 0
    min_core = 0
    max_core = 0
    for index, row in rats.iterrows():
        current_count += row['run_id']
        if current_count >= rats_per_core :
            core_ranges += [[ start, index]]
            if start <= min_config and min_config <= index:
                min_core = len(core_ranges)-1
            if start <= max_config and max_config <= index:
                max_core = len(core_ranges)-1
            current_count = 0
            start = index + 1

    if start < len(rats):
        core_ranges += [[start, len(rats)]]
        if start <= min_config and min_config <= index:
            min_core = len(core_ranges)-1
        if start <= max_config and max_config <= index:
            max_core = len(core_ranges)-1

    pd.DataFrame(columns=['start', 'end'], data=core_ranges).to_csv(save_file, index=False)
    print(f'{min_core}-{max_core}')

