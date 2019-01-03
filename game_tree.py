#coding: UTF-8
import networkx as nx
import random
import numpy as np

class GameTree():
    """
    実験用ゲーム木
    """
    def __init__(self, probability, d, bf, data_size, tree_name='kocsis'):
        self.probability = probability
        self.tree_name = tree_name
        self.d = d
        self.bf = bf
        self.tree = [[] for i in range(data_size)]
        if tree_name == 'kocsis':
            for i in range(data_size):
                #self.tree[i] = self.build_oyo_tree(d=d, bf=bf)
                self.tree[i] = self.build_kocsis_tree(d=d, bf=bf)
        elif tree_name == 'oyo':
            for i in range(data_size):
                self.tree[i] = self.build_oyo_tree(d=d, bf=bf)
        elif tree_name == 'gaussian':
            for i in range(data_size):
                self.tree[i] = self.build_gaussian_tree(d=d, bf=bf)


    def build_oyo_tree(self, d, bf):
        """ 大用さんの論文にある抽象木を作成
        :param d: 深さ
        :param bf: 子ノードの数
        :return: 深さd,子ノードbfの平衡木
        """
        tree = nx.balanced_tree(r=bf, h=d, create_using=nx.DiGraph())
        node_num = nx.number_of_nodes(tree)

        #葉のvalue属性に乱数を設定
        leaf_st = node_num - bf**d  #葉ノードのスタート
        for i in range(bf**(d-1)):
            #[random.randint(0,127) if random.random()<self.probability[i] else  random.randint(128,255) for _ in range(bf)]
            for j in range(bf):
                if random.random() < self.probability[j]:
                    value = random.randint(0,127)
                else:
                    value = random.randint(128,255)

                tree.nodes[leaf_st + (bf * i) + j]["value"] = value

                if value >= 180:
                    tree.nodes[leaf_st + (bf * i) + j]["reward"] = 1
                else:
                    tree.nodes[leaf_st + (bf * i) + j]["reward"] = 0

            self.add_flags(tree, leaf_st)

        #print(tree.nodes(data=True))

        return tree


    def build_kocsis_tree(self, d, bf):
        """ Kocsisの論文にある抽象木を作成
        :param d: 深さ
        :param bf: 子ノードの数
        :return: 深さd,子ノードbfの平衡木
        """
        #print("1")
        tree = nx.balanced_tree(r=bf, h=d, create_using=nx.DiGraph())
        node_num = nx.number_of_nodes(tree)
        #print("2")

        if (d%2) == 0:
            MAX_num = d/2
            MIN_num = d/2
        else:
            MAX_num = d/2 + 1
            MIN_num = d/2

        #葉のvalue属性に乱数を設定
        leaf_st = node_num - bf**d  #葉ノードのスタート
        # for i in range(bf**d):
        #     numbers = np.hstack( (np.random.randint(low=0,high=127+1,size=MAX_num),np.random.randint(low=-127,high=0+1,size=MIN_num)) )
        #     value = sum(numbers)
        #
        #     tree.nodes[leaf_st + i]["value"] = value
        #
        #     if value >= 0:
        #         tree.nodes[leaf_st + i]["reward"] = 1
        #     else:
        #         tree.nodes[leaf_st + i]["reward"] = 0
        children = []
        depth = 0
        parents = [0]
        tree.nodes[0]['value'] = 0

        while depth <= d:
            for p in parents:
                sons = list(tree.successors(p))
                for c in sons:
                    if (depth%2) == 0:
                        tree.nodes[c]['value'] = tree.nodes[p]['value'] + random.randint(-127, 0)
                    else:
                        tree.nodes[c]['value'] = tree.nodes[p]['value'] + random.randint(0, 127)

                    children = children + sons

            parents = children

            depth += 1

        for leaf in children:
            if tree.nodes[leaf]['value'] > 0:
                tree.nodes[leaf]['reward'] = 1
            else:
                tree.nodes[leaf]['reward'] = 0

        self.add_flags(tree, leaf_st)

        #print(tree.nodes(data=True))

        return tree

    def build_gaussian_tree(self, d, bf):
        """ 正規分布に従った報酬設定
        :param d: 深さ
        :param bf: 子ノードの数
        :return: 深さd,子ノードbfの平衡木
        """
        tree = nx.balanced_tree(r=bf, h=d, create_using=nx.DiGraph())
        node_num = nx.number_of_nodes(tree)

        #葉のvalue属性に乱数を設定
        leaf_st = node_num - bf**d  #葉ノードのスタート
        for i in range(bf**d):
            #value = np.random.randn()
            value = np.random.normal(0., 1.)

            tree.nodes[leaf_st + i]["value"] = value

            if value >= 0.:
                tree.nodes[leaf_st + i]["reward"] = 1
            else:
                tree.nodes[leaf_st + i]["reward"] = 0

        self.add_flags(tree, leaf_st)

        #print(tree.nodes(data=True))

        return tree

    def add_flags(self, tree, leaf_st):
        # 展開フラグを全ノードに追加
        nx.set_node_attributes(tree, False, 'expanded')
        # 試行回数を全ノードに追加
        nx.set_node_attributes(tree, 1, 'n')
        # 報酬和を全ノードに追加
        nx.set_node_attributes(tree, 0., 'q')
        # 価値を全ノードに追加
        nx.set_node_attributes(tree, 0., 'ucb')

        # 葉フラグを全ノードに追加(以下で葉にtrueを)
        nx.set_node_attributes(tree, False, 'is_terminal')
        for i in range(self.bf ** self.d):
            tree.nodes[leaf_st + i]['is_terminal'] = True

import utils

def check_game_tree():
    d = 3
    bf = 2
    data_size = 1
    data_sets = GameTree(probability=[0.8, 0.6], d=d, bf=bf, data_size=data_size, tree_name='kocsis')
    utils.print_tree(tree=data_sets.tree[-1], d=d, bf=bf, data_name='value')

if __name__ == "__main__":
    check_game_tree()

