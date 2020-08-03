from os.path import isfile as exists
from os.path import join as join_path
from os import listdir
from sys import argv
import re


if __name__ == '__main__':

    configs_folder = join_path(argv[1], 'configs', '')
    search_file = configs_folder + 'c{}/' + argv[2].replace('#ID', '{}')
    num_rats = int(argv[3])

    config_list = [f for f in listdir(configs_folder) if re.match('c\\d+$', f)]
    print('configs: ', len(config_list))

    
    missing_ids = [ str(c*num_rats + r) for c in config_list 
                                        for r in range(num_rats)
                                        if not exists(search_file.format(c,r))]

    totalMissing = len(missing_ids)
    print('num missing:', totalMissing)
    if totalMissing > 0:
        print('missingIds: ', ','.join(missing_ids))
