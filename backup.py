#coding: UTF-8
from value_functions import ucb

def backup(tree, node_num, reward):
    """
    指定されたノードからルートの子ノードまでの各ノードの情報を報酬を使って更新
    :param tree: 探索木
    :param node_num: 開始ノード
    :reward: 獲得した報酬
    """
    node = node_num
    parents = [c for c in tree.predecessors(node)]
    while len(parents) != 0:
        tree.nodes[node]['n'] += 1
        tree.nodes[node]['q'] += reward

        node = parents[0]
        parents = [c for c in tree.predecessors(parents[0])]

    #ルートのnも更新して、子ノードのucb計算に使う。
    tree.nodes[node]['n'] += 1


def negamax_backup(tree, node_num, reward):
    """
    対局ゲーム用のバックアップ。交互に報酬がマイナスになる。
    指定されたノードからルートの子ノードまでの各ノードの情報を報酬を使って更新
    :param tree: 探索木
    :param node_num: 開始ノード
    :reward: 獲得した報酬
    """
    r = reward
    node = node_num
    parents = [c for c in tree.predecessors(node)]
    while len(parents) != 0:
        tree.nodes[node]['n'] += 1
        tree.nodes[node]['q'] += r

        node = parents[0]

        r = -1 * r

        parents = [c for c in tree.predecessors(parents[0])]

    #ルートのnも更新して、子ノードのucb計算に使う。
    tree.nodes[node]['n'] += 1