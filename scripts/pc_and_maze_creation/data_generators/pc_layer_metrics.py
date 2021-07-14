import pandas as pd
import git, sys, os, numpy as np
from shapely.geometry import Point, LineString
from multiprocessing import Pool
import glob, time

join = os.path.join
save_name = 'layer_metrics.csv'
git_folder = git.Repo('.', search_parent_directories=True).git.rev_parse("--show-toplevel")
layers_folder = join(git_folder, 'experiments/pc_layers/')


def create_layer_metrics(folder = layers_folder):
    print('Creating layer metrics in folder ', join(folder, "**/*"))

    def is_pc_layer_file(path):
        return path.endswith(".csv") and save_name not in path

    files = [(folder, os.path.relpath(p, start = folder)) for p in glob.glob(join(folder, "**/*")) if is_pc_layer_file(p) ]

    print('TOTAL files: ', len(files))
    with Pool(12) as p:
        results = p.starmap(calculate_all_metrics, files)
        metrics = pd.DataFrame(results)
        metrics.to_csv(join(folder,save_name), index=False)
    print('DONE creating layer metrics')


def calculate_all_metrics(base_folder, file_path):
    start_time = time.time()
    full_path = join(base_folder, file_path)
    print('starting: ', time.strftime("%H:%M:%S", time.localtime()) , file_path)

    pcs = pd.read_csv(full_path)

    metrics = {}
    metrics['layer'                   ]  = file_path
    metrics['number of cells'         ]  = number_of_cells(pcs)
    metrics['total area'              ]  = total_area(pcs)
    metrics['mean area'               ]  = metrics['total area'] / metrics['number of cells']
    metrics['mean radius'             ]  = average_radius(pcs)
    metrics['mean distance'           ]  = average_distance_between_centers(pcs)
    metrics['normalized mean distance']  = metrics['mean distance'] / metrics['mean radius']

    print(f'finished {file_path} in {time.time() - start_time}')

    return metrics

def number_of_cells(pcs):
    return len(pcs)

def average_radius(pcs):
    return pcs['r'].mean()

def total_area(pcs):
    return np.pi * (pcs['r'] * pcs['r']).sum()

def total_area_clipped(pcs):
    # TODO
    pass

def average_distance_between_centers(pcs):
    num_pcs = len(pcs)
    def distance(i, j):
        return np.linalg.norm(pcs.loc[i, ['x','y']] - pcs.loc[j, ['x','y']])
    return np.mean([ distance(i,j) for i in range(num_pcs) for j in range(i+1, num_pcs)])

def average_area(total_a, num_cells):
    return total_a / num_cells

def normalized_average_distance_between_centers(average_distance, average_radius):
    return average_distance / average_radius


if __name__ == '__main__':
    folder = sys.argv[1] if len(sys.argv) > 1 else layers_folder
    create_layer_metrics(folder)

