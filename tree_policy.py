# coding: UTF-8
import random
import utils
from value_functions import ucb
from value_functions import rs

def tree_policy(tree, algo_name):
    """

    :return:
    """
    node_num = 0
    depth = 0
    while not tree.nodes[node_num]['is_terminal']:
        #全ての子が展開されていたら最も良い子を、そうでなけば未展開な子をランダムで
        children = get_nodes(tree, node_num, False)
        if len(children) == 0:
            #print("non-expanded={}".format(children))
            node_num = best_child(tree, node_num, algo_name)
            #node_num = best_child_negamax(tree=tree, node_num=node_num, depth=depth)
        else:
            return expand(tree, node_num, untried=children)

        depth += 1

    return node_num


def expand(tree, node_num, untried=None):
    """
    まだ試していない行動をして新たなノードを展開(すでに木があるのでexpandedにtrueを)
    :return: 新たに展開した子ノード番号
    """
    if untried == None:
    # 試していない子ノードをリストに
        untried = get_nodes(tree, node_num, tried=False)  # [c for c in children if not tree[c]['expanded']]

    new_node_num = random.choice(untried)
    tree.nodes[new_node_num]['expanded'] = True

    return new_node_num


def best_child_negamax(tree, node_num, depth):
    """
    最も高い価値関数をもつ子ノードの番号を返す(negamax:2人対戦の場合の最善手)
    """
    # 展開された子ノードリスト
    children = get_nodes(tree, node_num, tried=True)
    #print("expanded={}".format(children))
    values = [ucb(n_ij=tree.nodes[c]['n'], n_i=tree.nodes[node_num]['n'], q=tree.nodes[c]['q'])
              for c in children]
    # values = [rs(n_ij=tree.nodes[c]['n'],q=tree.nodes[c]['q'], r=0.5)
    #           for c in children]

    for i in range(len(children)):
        tree.nodes[children[i]]['ucb'] = values[i]

    #展開された子ノードのucbを全て計算してリストに
    if (depth % 2) == 0:
        #深さが偶数ならMAXがプレイ。最大値の添え字(複数なら最大値のうちランダムで)
        best_idx = utils.arg_max_rand(values)
    else:
        minus_values = [values[i] * -1 for i in range(len(values))]
        #print(minus_values)
        # 深さが奇数ならMINがプレイ。最小値の添え字(複数ならランダムで)
        best_idx = utils.arg_max_rand(minus_values)


    return children[best_idx]


def best_child(tree, node_num, algo_name='UCT'):
    """
    最も高い価値関数をもつ子ノードの番号を返す
    """
    # 展開された子ノードリスト
    #children = get_nodes(tree, node_num, tried=True)
    children = list(tree.successors(node_num))

    #展開された子ノードのucbを全て計算してリストに
    if algo_name == 'UCT':
        values = [ucb(n_ij=tree.nodes[c]['n'], n_i=tree.nodes[node_num]['n'], q=tree.nodes[c]['q'])
                    for c in children]
    elif algo_name == 'RS':
        values = [rs(n_ij=tree.nodes[c]['n'], q=tree.nodes[c]['q'], r=0.7)
                             for c in children]
    else:
        print("Algorithm name error.")

    #print("values = {}".format(values))

    for i in range(len(children)):
        tree.nodes[children[i]]['ucb'] = values[i]

    # 最大値の添え字(複数なら最大値のうちランダムで)
    max_idx = utils.arg_max_rand(values)

    return children[max_idx]


def get_nodes(tree, node_num, tried):
    """
    展開された or されていない 子ノードをリストで返す
    :param tree: 木
    :param node_num: 親ノード番号
    :tried: (true)展開されたもの、(false)されていないものを返す
    """
    if tried:
        return [num for num in tree.successors(node_num) if tree.nodes[num]['expanded']]
    else:
        return [num for num in tree.successors(node_num) if not tree.nodes[num]['expanded']]

