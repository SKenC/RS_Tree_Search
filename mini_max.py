#coding: UTF-8
import networkx as nx
import test
import random
import utils
import numpy as np

def minimax_algo(tree, d, bf, draw=False):
    """
    探索木の最適な道をミニマックス法で求めてリストで返す
    :tree: DiGraph instance.
    :draw: ミニマックス木を表示するか否か
    :return: ans_nodes ノードから選択すべきノード番号リスト。size = d-1
    """
    #データ表示用
    if draw:
        leaf_st = nx.number_of_nodes(tree) - bf**d
        print("values={}".format([tree.nodes[leaf_st + i]['value'] for i in range(bf**d)]))

    #minimax_tree = nx.balanced_tree(r=bf, h=d, create_using=nx.DiGraph())
    #node_num = nx.number_of_nodes(tree)

    #葉ノードスタート
    leaf_st = nx.number_of_nodes(tree) - bf**d

    # for i in range(bf**d):
    #     minimax_tree.nodes[leaf_st + i]['value'] = tree.nodes[leaf_st + i]['value']
    minimax_tree = [[] for _ in range(d)] + [[tree.nodes[leaf_st + i]['value'] for i in range(bf**d)]]
    values = [tree.nodes[leaf_st + i]['value'] for i in range(bf ** d)]
    #parents = np.reshape([[p for p in minimax_tree.predecessors(node_num - bf**d + c)] for c in range(bf**d)], [-1])
    for i in range(d):

        # #最初の一手は、MAXの行動とする。MAX-->MIN-->MAX-->...
        if ((d-i)%2) == 0:
            #同じ親の中で最も小さい評価値をリストに (MINのプレイ)
            opt_values = [min(values[(k*bf) : (k*bf)+bf]) for k in range(bf**(d-i-1))]
        else:
            #同じ親の中で最も大きい評価値をリストに (MAXのプレイ)
            opt_values = [max(values[(k*bf) : (k*bf)+bf]) for k in range(bf**(d-i-1))]


        minimax_tree[d-i-1] = opt_values
        # for j in range(len(opt_values)):
        #     tree.nodes[parents[j]]['value'] = opt_values[j]

        #親の評価値として代入
        values = opt_values

        #parents = np.reshape([[p for p in minimax_tree.predecessors(parents[j])] for j in range(len(parents))], [-1])

        #データ表示用
        if draw:
            print("values={}".format(values))

    #print(minimax_tree)

    return minimax_tree[0][0]

#networkxを使ってminimaxtreeを作る
def minimax_algo_nx(tree, bf, d):
    minimax_tree = nx.balanced_tree(r=bf, h=d, create_using=nx.DiGraph())
    # 葉ノードスタート
    leaf_st = nx.number_of_nodes(tree) - bf ** d
    leaf_nums = [list(tree.nodes)[leaf_st + i] for i in range(bf**d)]
    for i in range(bf**d):
        minimax_tree.nodes[leaf_st + i]['value'] = tree.nodes[leaf_nums[i]]['value']

    #parents_st = leaf_st - bf**(d-1)
    #print(minimax_tree.nodes())
    #d-1層のノード
    #parents = list(minimax_tree.nodes())[parents_st : parents_st + bf**(d-1)]
    parents = [list(minimax_tree.predecessors(leaf_nums[bf*i]))[0] for i in range(bf**(d-1))]
    #minimax_treeを作る
    rev = 1.
    for depth in range(d, 0, -1): #d層から1層まで
        #print(depth, parents)
        #print(depth)
        for i in range(len(parents)):
            #子ノードの評価値をリストに
            children = list(minimax_tree.successors(parents[i]))
            c_vals = [minimax_tree.nodes[c]['value'] for c in children]
            #parentの層が偶数ならMAXによる選択,奇数ならMINによる選択
            # if (depth-1)%2 == 0:
            #     minimax_tree.nodes[parents[i]]['value'] = max(c_vals)
            # else:
            #     minimax_tree.nodes[parents[i]]['value'] = min(c_vals)
            rev_val = map(lambda x: x * rev, c_vals)
            max_idx = np.argmax(rev_val)
            minimax_tree.nodes[parents[i]]['value'] = c_vals[max_idx]

        rev *= -1.

        parents = [list(minimax_tree.predecessors(parents[bf * j]))[0] for j in range(len(parents)/bf)]
        #print("parents={},p_st={},d={}".format(parents,parents_st,depth))
        #parents_st -= depth-1
        #parents = list(minimax_tree.nodes())[parents_st: parents_st + len(parents)/bf] #今見ている層の親の親の個数はbf^(depth-2)

    return minimax_tree

#minimax treeで得られる最善のpathをリストで
def get_minimax_path(tree, bf, d, draw=False):
    minimax_tree = minimax_algo_nx(tree, bf, d)

    if draw:
        utils.print_tree(tree=minimax_tree, d=d, bf=bf)

    children = list(minimax_tree.successors(0))
    root_val = minimax_tree.nodes[0]['value']

    path = [0 for i in range(d)]
    for i in range(d):
        b_idx = np.argmax([minimax_tree.nodes[children[c]]['value'] for c in range(len(children))])
        #b_idx = [minimax_tree.nodes[children[c]]['value']for c in range(len(children))].index(root_val)
        path[i] = children[b_idx]

        children = list(minimax_tree.successors(children[b_idx]))

    return path


#このファイルのテスト用
def check_method():

    d = 5
    bf = 2
    gt = test.GameTree(probability=[random.random() for _ in range(bf**(d-1))], d=d, bf=bf, threshold=128)

    #print(gt.tree.nodes(data=True))

    print( minimax_algo_nx(tree=gt.tree, d=d, bf=bf).nodes(data=True))
    print( get_minimax_path(tree=gt.tree, d=d, bf=bf) )



if __name__ == "__main__":
    check_method()


