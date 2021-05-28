"""
Trie data structure
"""

import unittest


class TrieNode:
    """
    Trie Node
    """
    def __init__(self):
        self.children = {}


class Trie:
    """
    Trie Data structure. Initialised with empty root node.
    """
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        """
        Insert a string (word) into the Trie.
        :param word: string
        """
        current_node = self.root

        for char in word:
            if current_node.children.get(char):
                current_node = current_node.children[char]
            else:
                new_node = TrieNode()
                current_node.children[char] = new_node
                current_node = new_node

        current_node.children['*'] = None

    def contains(self, word):
        """
        Check if the trie contains the exact word as supplied. Must be full word, not partial or prefix.
        :param word: word to search for
        :return: True if word is in the Trie, otherwise false
        """
        return '*' in self.get_next_node(word).children

    def get_next_node(self, prefix):
        """
        Search for the next node of a given prefix.
        e.g. Trie contains 'Hello' and 'HelloWorld' get_next_node('Hello') will return the
        next node after 'o', containing 2 children '*' to indicate end of 'Hello' and 'W' for start of 'World'

        Example usage. Method can be used for autocomplete to find all possible words in the Trie
        for a given prefix (from that point onwards).
        :param prefix: The string (word) to find in the Trie.
        :return: the node containing the start of the word, if found or None.
        """
        current_node = self.root

        for char in prefix:
            if current_node.children.get(char):
                current_node = current_node.children[char]
            else:
                return None

        return current_node

    def collect_all_words(self, node=None, prefix="", words=[]):
        """
        Recursive method to find all remaining portions of the words with matching prefix.
        e.g. Trie contains 'Hello' for prefix 'He', then 'llo; is returned.
        Nothing is returned for a complete match of prefix and word.
        :param node: THe start node, uses root node if None
        :param prefix: prefix
        :param words: empty list to hold results
        :return: words (list of all words matched)
        """
        current_node = node or self.root

        for key, child_node in current_node.children.items():
            if key == '*':
                words.append(prefix)
            else:
                self.collect_all_words(child_node, prefix + key, words)

        return words


class TestTrie(unittest.TestCase):
    def test_trie_should_contain_word(self):
        trie = Trie()
        trie.insert("Hello")
        result = trie.contains("Hello")

        self.assertTrue(result)

    def test_trie_should_not_contain_word(self):
        trie = Trie()

        result = trie.contains("Hello")
        self.assertFalse(result)

        trie.insert("HelloWorld")
        self.assertFalse(result)

    def test_should_not_find_word_in_empty_trie(self):
        trie = Trie()
        result = trie.get_next_node("WordNotInTrie")

        self.assertEqual(None, result)

    def test_should_find_end_node_for_given_word(self):
        trie = Trie()
        trie.insert("Hello")

        result = trie.get_next_node("Hello")
        # Indicates end of the word, i.e located the whole word
        self.assertEqual(1, len(result.children))
        self.assertEqual(None, result.children['*'])

    def test_should_find_next_node_for_given_prefix(self):
        trie = Trie()
        trie.insert("Hello")
        trie.insert("HelloWorld")

        result = trie.get_next_node("Hello")
        # Indicates end of the word, i.e located the whole word
        self.assertEqual(2, len(result.children))
        self.assertEqual(None, result.children['*'])

        # Next node is start of the 'World' part of 'HelloWorld'
        self.assertIsNotNone(result.children['W'])

    def test_return_remaining_portion_of_word_with_matching_prefix(self):
        trie = Trie()
        trie.insert("World")

        result = trie.get_next_node("Wor")
        # Indicates end of the word, i.e located the whole word
        self.assertEqual(1, len(result.children))
        self.assertIsNotNone(result.children['l'])

        # Next node
        result = result.children['l']
        self.assertEqual(1, len(result.children))
        self.assertIsNotNone(result.children['d'])

        # Terminating node
        result = result.children['d']
        self.assertEqual(1, len(result.children))
        self.assertIsNone(result.children['*'])

    def test_return_all_remaining_portions_of_words_with_matching_prefix(self):
        trie = Trie()
        trie.insert("World")
        trie.insert("World!")

        result = trie.get_next_node("Worl")
        # Indicates end of the word, i.e located the whole word
        self.assertEqual(1, len(result.children))
        self.assertIsNotNone(result.children['d'])

        # Terminating node of 1st word + next node for second matching word
        result = result.children['d']
        self.assertEqual(2, len(result.children))
        self.assertIsNotNone(result.children['!'])
        self.assertIsNone(result.children['*'])

        # Terminating node of second word + next node for second matching word
        result = result.children['!']
        self.assertEqual(1, len(result.children))
        self.assertIsNone(result.children['*'])


if __name__ == '__main__':
    unittest.main()
