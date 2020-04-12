import os
import sys
import re


def get_list_of_configs(base_folder):
    return [f for f in os.listdir(base_folder) if re.match('c\\d+$', f)]


if __name__ == '__main__':

    experiment_folder = os.path.join(sys.argv[1], '')
    filename = sys.argv[2]
    num_rats = int(sys.argv[3])

    config_list = get_list_of_configs(experiment_folder)
    num_configs = len(config_list)
    print('configs: ', num_configs)
    missing_ids = []
    totalMissing = 0
    for configId in range(num_configs):
        for rat_id in range(num_rats):
            search_file = experiment_folder + 'c' + str(configId) + '/' + filename.replace('#ID', str(rat_id))
            if not os.path.isfile(search_file):
                missing_ids += [str(configId * num_rats + rat_id)]
                totalMissing += 1
    print('num missing:', totalMissing)
    if totalMissing > 0:
        print('missingIds: ', ','.join(missing_ids))
    pass
