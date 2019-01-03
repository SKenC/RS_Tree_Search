# coding: UTF-8
import random

def default_policy(tree, node_num):
    """
    指定されたノードからランダムに行動して報酬を返す
    :param tree: 探索木
    :param node_num: 開始ノード
    :return: 最終的に得た報酬
    """
    node = node_num
    while not tree.nodes[node]['is_terminal']:
        children = [c for c in tree.successors(node)]
        node = random.choice(children)

    return tree.nodes[node]['reward']