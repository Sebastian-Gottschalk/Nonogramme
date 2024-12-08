import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

def solver_step(currently_solved, possibilitys):
    # copy the value currently solved to check if the algorithm has converged /
    # if the value of currently_solved changed while doing the solver_step
    old_currently_solved = currently_solved.copy()
    unsolvable = False

    # iterate over each row / column and call the function row_col_step on it
    for row_nr in range(currently_solved.shape[0]):
        currently_solved.iloc[row_nr,:], unsolvable = row_col_step(
            currently_solved.iloc[row_nr,:].values,
            possibilitys[0][row_nr],
            unsolvable
            )
        
        
    for col_nr in range(currently_solved.shape[1]):
        currently_solved.iloc[:,col_nr], unsolvable = row_col_step(
            currently_solved.iloc[:,col_nr].values,
            possibilitys[1][col_nr],
            unsolvable
            )
    return currently_solved, False in (currently_solved.round(3)==old_currently_solved.round(3)).values, unsolvable


def row_col_step(current_value, possibilitys, unsolvable):
    norm_const = 0.0
    result = np.array([0]*len(current_value)).astype(float)
    debug_var = []
    for pos in possibilitys:
        pos = np.array(pos)
        current_prob = get_prob(current_value, pos)
        result += current_prob * pos
        norm_const += current_prob
    if norm_const>0:
        result = result / norm_const
        result[(result != 0) & (result != 1)] = 0.5
        return result, False or unsolvable
    else:
        return result, True

def get_prob(current_value, pos):
    prob = 1
    for i in range(len(current_value)):
        if pos[i] == 1:
            prob *= current_value[i]
        else:
            prob *= 1-current_value[i]
    return prob


def get_possible_combinations(restriction,n,recursion_value = []):
    ''' 
    recursive function to get all possible combinations given the nonogramm restrictions
    restriction and the length of the row / column n, e.g.

    restriction = [1,2]
    n = 5
    Output = [
     [1,0,1,1,0],
     [1,0,0,1,1],
     [0,1,0,1,1]
    ]

    restriction = [2,1]
    n = 5
    Output = [
     [1,1,0,1,0],
     [1,1,0,0,1],
     [0,1,1,0,1]
    ]
    '''
    if len(restriction) > 0:
        possible_values = []
        max_index = n-sum(restriction)-len(restriction)+2
        for i in range(max_index):
            current_recursion_value = recursion_value + [0]*i + [1]*restriction[0]
            j=i
            if len(restriction)>1:
                current_recursion_value += [0]
                j=i+1
            possible_values += get_possible_combinations(
                restriction[1:],
                n-j-restriction[0],
                recursion_value = current_recursion_value
                )
            
    else:
        possible_values = [recursion_value + [0]*n]
    
    return possible_values


def solve_nonogramm(restrictions,display_progress = True):
    
    size = [len(restrictions[0]),len(restrictions[1])]
    currently_solved = pd.DataFrame(0.5, index= range(size[0]), columns= range(size[1]))

    possibilitys = [[],[]]
    for i in range(2):
        for res in restrictions[i]:
            possibilitys[i].append(get_possible_combinations(res,size[i]))

    not_solved = True
    if display_progress:
        plt.ion()
        fig, ax = plt.subplots()
        im = ax.imshow(currently_solved.values, cmap='Greys', vmin= 0, vmax=1)
    counter = 0
    while not_solved:
        print(f'step #{counter}')
        counter+=1
        currently_solved, not_solved, unsolvable = solver_step(
            currently_solved,
            possibilitys
            )
        if display_progress:
            im.set_data(currently_solved.values)
            fig.canvas.draw_idle()
            plt.pause(0.3)
            time.sleep(0.3)
        if unsolvable:
            break
    
    if display_progress:
        plt.ioff()
        plt.show()
        
    
    return currently_solved, unsolvable




restrictions = [
    [
        [3,1,3,1,1],
        [3,1],
        [2,1,2,4],
        [4,10],
        [17],
        [2,5,1,4],
        [3,1,1,3],
        [4,3,1,3],
        [6,1,1,3],
        [5,9],
        [2,6,1],
        [1,2,2,3,1,2],
        [2,4,2,3],
        [15,1],
        [2,13,1],
        [2,6,5,1,1],
        [2,5,1,9],
        [3,3,1,1,9],
        [6,3],
        [6,1,2,1,1],
        [3,1,2,1],
        [10,1,3,3],
        [5,1,1,7],
        [4,4,11],
        [2,3,7,3]
    ],
    [
        [5,1],
        [5,3],
        [3,1,1,4],
        [3,1,4],
        [2,1,2,5],
        [3,2,2,4],
        [3,1,3,4,3,1],
        [13,1,1,2],
        [2,7,7,4],
        [2,2,10,2],
        [7,4,1],
        [1,3,6],
        [1,8,2,1],
        [1,2,1,3,2,5],
        [3,4,3,7],
        [3,4,4,2],
        [4,4,5,2],
        [2,4,5,2],
        [1,3,3,10],
        [3,1,3,4],
        [3,3,2,4],
        [4,1,3,2],
        [5,1,2,4],
        [1,5,2,2,4],
        [4,2,1,4]
    ]
]

solve_nonogramm(restrictions)
