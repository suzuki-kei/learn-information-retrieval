"""
    postings list に関する操作を実装する.

    用語定義
    --------
    posting
        postings list の要素のこと.
        単語が文書に現れたことの記録.

    postings list; inverted list
        単語がどの文書に含まれるかを表すリスト.
        通常はソートされた文書 ID (docID) のリスト.

    postings
        全ての postings list をまとめたもの.
"""

import typing
import unittest


def subtract(
        postings_list1: typing.List[int],
        postings_list2: typing.List[int]
        ) -> typing.List[int]:
    """
        postings list の差分を求める.

        Arguments
        ---------
        postings_list1 : typing.List[int]
            postings list.
        postings_list2 : typing.List[int]
            postings list.

        Returns
        -------
        typing.List[int]
            postings_list1 から postings_list2 を除外した postings list.
    """
    index1 = 0
    index2 = 0
    postings_list = []

    while index1 < len(postings_list1) or index2 < len(postings_list2):
        if index1 >= len(postings_list1):
            break
        if index2 >= len(postings_list2):
            postings_list.extend(postings_list1[index1:])
            break
        if postings_list1[index1] < postings_list2[index2]:
            postings_list.append(postings_list1[index1])
            index1 += 1
            continue
        if postings_list1[index1] > postings_list2[index2]:
            postings_list.append(postings_list2[index2])
            index2 += 1
            continue
        index1 += 1
        index2 += 1
    return postings_list


class SubtractTestCase(unittest.TestCase):

    def test(self):
        self.assertEqual([], subtract([], []))
        self.assertEqual([], subtract([], [1]))
        self.assertEqual([], subtract([], [1, 2]))
        self.assertEqual([], subtract([], [1, 2, 3]))

        self.assertEqual([1], subtract([1], []))
        self.assertEqual([1, 2], subtract([1, 2], []))
        self.assertEqual([1, 2, 3], subtract([1, 2, 3], []))

        self.assertEqual([2, 3], subtract([1, 2, 3], [1]))
        self.assertEqual([3], subtract([1, 2, 3], [1, 2]))
        self.assertEqual([], subtract([1, 2, 3], [1, 2, 3]))


def negate(
        postings_list: typing.List[int],
        document_size: int
        ) -> typing.List[int]:
    """
        postings list の否定を求める.

        Arguments
        ---------
        postings_list : typing.List[int]
            posting list.
        document_size : int
            ドキュメント数.
            ドキュメント ID は [1, document_size] であることを前提とする.

        Returns
        -------
        typing.List[int]
            postings_list が含まない posting を含む postings list.
    """
    return subtract(list(range(1, document_size + 1)), postings_list)


class NegateTestCase(unittest.TestCase):

    def test(self):
        self.assertEqual([], negate([], 0))
        self.assertEqual([1], negate([], 1))
        self.assertEqual([1, 2], negate([], 2))
        self.assertEqual([1, 2, 3], negate([], 3))

        self.assertEqual([2, 4], negate([1, 3, 5], 5))
        self.assertEqual([1, 3, 5], negate([2, 4], 5))


def union(
        postings_list1: typing.List[int],
        postings_list2: typing.List[int]
        ) -> typing.List[int]:
    """
        2 つの postings list の和を求める.

        Arguments
        ---------
        postings_list1 : typing.List[int]
            postings list.
        postings_list2 : typing.List[int]
            postings list.

        Returns
        -------
        typing.List[int]
            postings_list1 と postings_list2 の和.
    """
    index1 = 0
    index2 = 0
    postings_list = []
    while index1 < len(postings_list1) or index2 < len(postings_list2):
        if index1 >= len(postings_list1):
            postings_list.extend(postings_list2[index2:])
            break
        if index2 >= len(postings_list2):
            postings_list.extend(postings_list1[index1:])
            break
        if postings_list1[index1] < postings_list2[index2]:
            postings_list.append(postings_list1[index1])
            index1 += 1
            continue
        if postings_list2[index2] < postings_list1[index1]:
            postings_list.append(postings_list2[index2])
            index2 += 1
            continue
        postings_list.append(postings_list1[index1])
        index1 += 1
        index2 += 1
    return postings_list


class UnionTestCase(unittest.TestCase):

    def test(self):
        self.assertEqual([], union([], []))

        self.assertEqual([1], union([], [1]))
        self.assertEqual([1, 2], union([], [1, 2]))
        self.assertEqual([1, 2, 3], union([], [1, 2, 3]))

        self.assertEqual([1], union([1], []))
        self.assertEqual([1, 2], union([1, 2], []))
        self.assertEqual([1, 2, 3], union([1, 2, 3], []))

        self.assertEqual([1], union([1], []))
        self.assertEqual([1, 2], union([1], [2]))
        self.assertEqual([1, 2, 3], union([1, 3], [2]))
        self.assertEqual([1, 2, 3, 4], union([1, 3], [2, 4]))

        self.assertEqual([1], union([1], [1]))
        self.assertEqual([1, 2], union([1, 2], [1, 2]))
        self.assertEqual([1, 2, 3], union([1, 2, 3], [1, 2, 3]))


def intersect(
        postings1: typing.List[int],
        postings2: typing.List[int]
        ) -> typing.List[int]:
    """
        2 つの Postings List の積集合を求める.
    """
    index1 = 0
    index2 = 0
    postings = []
    while index1 < len(postings1) and index2 < len(postings2):
        if postings1[index1] < postings2[index2]:
            index1 += 1
            continue
        if postings2[index2] < postings1[index1]:
            index2 += 1
            continue
        postings.append(postings1[index1])
        index1 += 1
        index2 += 1
    return postings


class IntersectTestCase(unittest.TestCase):

    def test(self):
        self.assertEqual([], intersect([], []))

        self.assertEqual([], intersect([], [1]))
        self.assertEqual([], intersect([], [1, 2]))
        self.assertEqual([], intersect([], [1, 2, 3]))

        self.assertEqual([], intersect([1], []))
        self.assertEqual([], intersect([1, 2], []))
        self.assertEqual([], intersect([1, 2, 3], []))

        self.assertEqual([], intersect([1], [2]))
        self.assertEqual([], intersect([2], [1]))

        self.assertEqual([1], intersect([1], [1, 2, 3]))
        self.assertEqual([1, 2], intersect([1, 2], [1, 2, 3]))
        self.assertEqual([1, 2, 3], intersect([1, 2, 3], [1, 2, 3]))
        self.assertEqual([1, 2, 3], intersect([1, 2, 3, 4], [1, 2, 3]))

        self.assertEqual([1], intersect([1, 2, 3], [1]))
        self.assertEqual([1, 2], intersect([1, 2, 3], [1, 2]))
        self.assertEqual([1, 2, 3], intersect([1, 2, 3], [1, 2, 3]))
        self.assertEqual([1, 2, 3], intersect([1, 2, 3], [1, 2, 3, 4]))


def main():
    unittest.main()


if __name__ == "__main__":
    main()

