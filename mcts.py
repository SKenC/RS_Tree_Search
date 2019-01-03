# coding: UTF-8
from tree_policy import tree_policy, best_child_negamax, best_child
from default_policy import default_policy
from backup import backup, negamax_backup

import utils

def mcts(tree, n, ans_path, algo_name='UCT'):
    """
    モンテカルロ木探索
    Args:
        tree: 探索する木
        n: ロールアウト回数
        ans_path: 答えのパスを表すリスト
    :return:
        best_leaf_num: 最も良いと思われる葉番号
    """
    accuracy_list = [0. for i in range(n)]
    chosen = -1
    for i in range(n):
        #新たにノードを展開 or 最もいい価値関数を進んだノード
        chosen = tree_policy(tree=tree, algo_name=algo_name)
        #選ばれたノードからランダムに葉まで行って報酬獲得
        reward = default_policy(tree=tree, node_num=chosen)
        #報酬をchosenからルートノードまで伝播
        #backup(tree=tree, node_num=chosen, reward=reward)
        negamax_backup(tree=tree, node_num=chosen, reward=reward)

        #現時点での正解率を計算
        accuracy_list[i] = utils.accuracy(result=get_best_path(tree, algo_name), target=ans_path)

    #print("MCTS-END")

    return get_best_path(tree=tree, algo_name=algo_name), accuracy_list #get_best_path(tree)


def get_best_path(tree, algo_name, d=1000):
    """
    学習後に価値関数最大を選んで最も良いと思われる葉を返す
    :param tree:
    :return:
    """
    node = 0
    depth = 0
    path = [0 for _ in range(d)]
    while not tree.nodes[node]['is_terminal']:
        #node = best_child_negamax(tree=tree, node_num=node, depth=depth)
        node = best_child(tree=tree, node_num=node, algo_name=algo_name)
        path[depth] = node
        depth += 1

    return path[:depth]

def get_path(tree, node_num, d=1000):
    """
    node_numまでのルートからのパスを返す
    :param node_num:
    :return:
    """
    parent = list(tree.predecessors(node_num))
    path = [0 for _ in range(d)]
    path[0] = node_num
    path_num = 1
    while len(parent) != 0:
        path[path_num] = parent[0]
        path_num += 1
        parent = list(tree.predecessors(parent[0]))

    return list(reversed(path[:path_num-1]))



