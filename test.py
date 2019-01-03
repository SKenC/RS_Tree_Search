# coding: UTF-8
import numpy as np
import utils
from game_tree import GameTree
from mcts import mcts
import mini_max


def main():

    d = 5
    bf = 2
    data_size = 1
    rollout_num = 50

    data_set = GameTree(probability=[0.8, 0.6], d=d, bf=bf, data_size=data_size, tree_name='kocsis')

    results = [[] for i in range(data_size)]
    accuracy = [[] for i in range(data_size)]
    for i in range(data_size):
        ans_path = mini_max.get_minimax_path(tree=data_set.tree[i], d=d, bf=bf, draw=True)
        results[i], accuracy[i] = mcts(tree=data_set.tree[i], n=rollout_num, ans_path=ans_path, algo_name='UCT')

        print("{}%done, ans={},results={}".format((float(i)/data_size)*100,ans_path, results[i]))

    utils.print_tree(tree=data_set.tree[-1], d=d, bf=bf, data_name='ucb')

    #print("ans={},minimax_ans={}".format(ans, minimax_ans))

    #correct_rate = accuracy(ans, minimax_ans)
    #print(accuracy)

    means = np.zeros(rollout_num)
    accuracy = np.array(accuracy)
    for i in range(rollout_num):
        means[i] = np.mean(accuracy[:, i])

    print("result = {}".format(results[-1]))
    print("means = {}".format(means))

if __name__ == "__main__":
    main()