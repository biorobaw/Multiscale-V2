import pandas as pd
import default_cell_generator as generator
import git, os, numpy as np


lab_maze = {'mx':-1.1, 'Mx': 1.1, 'my': -1.5, 'My': 1.5} # min and Max x and y coordinates of lab maze


def create_uniform_layer(r, nx, dims=lab_maze):
    mx = dims['mx']
    Mx = dims['Mx']
    my = dims['my']
    My = dims['My']
    ratio = round((My-my)/(Mx-mx), 4)
    ny = int(np.ceil(nx*ratio))
    return generator.distribute_uniformly(mx, Mx, nx, my, My, ny, r)

def create_uniform_layer_at(x, y, r, nx, dx):
    # add cells of size 0.16 around target 
    half_width = dx*(nx-1)/2.0
    dims = {
        'mx' : x - half_width,     # min x
        'Mx' : x + half_width,     # max x
        'my' : y - half_width,     # min y
        'My' : y + half_width     # max y
    }
    return create_uniform_layer(r, nx, dims)

def create_and_save_uniform(folder, r, nx, dims=lab_maze):
    file = f'u{round(r*100):02d}_{nx:02d}.csv'
    pcs = create_uniform_layer(r, nx, dims)
    save_layer(pcs, folder, file)

def save_layer(pcs, folder, file):
    full_path = os.path.join(folder, file)
    makedirs(full_path)
    print(f'Generating file: {file}  at  {full_path}')
    pcs.to_csv(full_path, index=False)


def git_root():
    git_repo = git.Repo('.', search_parent_directories=True)
    return git_repo.git.rev_parse("--show-toplevel")
      

def mazes_root_dir():
    return os.path.join(git_root(), 'experiments/pc_layers')

def makedirs(file):
    os.makedirs(os.path.dirname(file), exist_ok=True)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

if __name__ == '__main__':

    ####### CONSTANTS ##################################################################
    mazes_dir = mazes_root_dir()

    ####### UNIFOR LAYERS ##############################################################

    # minimum number of cells (columns) to cover the maze
    uniform_min_nx = {
        0.04: 40,
        0.08: 21,
        0.12: 14,
        0.16: 11,
        0.20: 9,
        0.24: 7,
        0.28: 6,
        0.32: 6,
        0.36: 6,
        0.40: 5,
        0.44: 5,
        0.48: 4,
        0.52: 4,
        0.56: 4,
    }
    sizes = [5*i for i in range(1,9)] # possible number of columns, from 5 to 40 in steps of 5
    uniform_layers = pd.DataFrame(
            columns=['r', 'nx'],
            data = [ [r, n] for r in uniform_min_nx.keys() for n in sizes if n >= uniform_min_nx[r]]
        )

    print(f'{bcolors.OKBLUE}## GENERATING UNIFORM LAYERS ##{bcolors.ENDC}')
    print()
    uniform_mazes_dir = os.path.join(mazes_dir,'uniform','')
    for r, nx in uniform_min_nx.items():
        create_and_save_uniform(uniform_mazes_dir, r, nx)
    for index, row in uniform_layers.iterrows():
        create_and_save_uniform(uniform_mazes_dir, row['r'], int(row['nx']))

    ######### LOCALLY UNIFORM LAYERS #######################################################


    print()
    print(f'{bcolors.OKBLUE}## GENERATING LOCALLY UNIFORM LAYERS ##{bcolors.ENDC}')
    print()

    GOAL_CELLS = create_uniform_layer_at(0.1, 1.2, 0.16, 3, 0.21)
    GAP_CELLS  = create_uniform_layer_at(0.575, 0, 0.16, 4, 0.21)

    lu_folder = os.path.join(mazes_dir,'locally_uniform','')

    for r, nx in uniform_min_nx.items():
        if r <= 0.16:
            continue
        uniform = create_uniform_layer(r, nx)

        lu0 = pd.concat([uniform, GOAL_CELLS], ignore_index=True)
        filename = f'lu0_{round(r*100):02d}_16.csv'
        save_layer(lu0, lu_folder, filename)


        lu1 = pd.concat([uniform, GOAL_CELLS, GAP_CELLS], ignore_index=True)
        filename = f'lu1_{round(r*100):02d}_16.csv'
        save_layer(lu1, lu_folder, filename)

    ######### NON UNIFORM LAYERS #######################################################
    
    # Generated manually, thus section empty

    ######### UNIFORM MULTILAYER #######################################################

    dfs = {
        round(r*100) : pd.read_csv(os.path.join(uniform_mazes_dir, f'u{round(r*100):02d}_{nx:02d}.csv'))
        for r, nx in uniform_min_nx.items()
    }

    combinations = [
        [4 , 16 , 52]
    ]

    multi_layer_folder = os.path.join(mazes_dir,'multi_layer','')
    for c in combinations:
        pcs = pd.concat([dfs[r] for r in c], ignore_index= True)
        filename = 'ml_' + '_'.join([str(r) for r in c]) + '.csv'
        save_layer(pcs, multi_layer_folder, filename)
        
