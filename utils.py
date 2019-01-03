# coding: UTF-8
import sys
import random
import numpy as np
from value_functions import ucb
import tree_policy

def accuracy(result, target, level=0):
    """
    正解率として、二つのリストの一致割合を返す
    :return:
    """

    if len(result) < len(target):
        eq_list = [1. if x == y else 0. for x, y in zip(result, target)] + [0. for _ in range(len(target)-len(result))]
    else:
        eq_list = [1. if x == y else 0. for x, y in zip(result, target)]

    #print("eq_list={},result={},target={}".format(eq_list, result, target))
    #return np.mean(eq_list)
    return eq_list[level]

def arg_max_rand(values):
    """
    :values: 調べるリスト
    :return: 最大値の添え字
    """
    max = -float('inf')  # minimum value.
    max_indices = []
    #get maximum values and those indices.
    for i in range(len(values)):
        if values[i] > max:
            max = values[i]
            max_indices = [i]
        elif values[i] == max:
            max_indices.append(i)


    max_num = len(max_indices)

    #print(max_indices, max, values)

    if max_num == 1:
        #return maximum index
        return max_indices[0]
    else:
        #retrun random index of maximum values
        return max_indices[random.randint(0,max_num-1)]

def print_tree(tree, d, bf, data_name='value'):

    children = [list(tree.successors(0))]
    for _ in range((bf**d)/2):
        print ' ',

    print(tree.nodes[0][data_name])

    for i in range(d):
        for j in range(len(children)):
            vals = [tree.nodes[c][data_name] for c in children[j]]
            for v in vals:
                for k in range((bf**d)/(2**(i+2))):
                    print ' ',
                if data_name == 'ucb' or data_name == 'value':
                    print('{0:.2f}'.format(v)),
                else:
                    print("%3d"%v),
        print ''
        children = [list(tree.successors(c)) for c in np.reshape(children,[-1])]