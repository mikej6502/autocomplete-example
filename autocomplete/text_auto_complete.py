"""
Class to provide basic auto complete functionality. Initialise with a list of words, then search
for a prefix. Any words starting with the prefix are returned.
"""
from trie import Trie
import unittest


class TextAutoComplete:
    """
    Text Auto Complete. Supply an a list of words to initialise
    """
    def __init__(self, words):
        self._trie = Trie()
        for word in words:
            self._trie.insert(word)

    def autocomplete(self, prefix):
        """
        Provide a prefix, minimum one character. All matching words are returned that begin with
        the prefix.
        NB: Only the portion of the word is returned, excluding the prefix e.g.
         - Initialised with 'Hello' and 'HelloWorld'
         - Call autocomplete with prefix 'He'
         - 'llo' and 'lloworld' are returned, as partial words, as the full word matches the prefix.
         - Simple concatinate the prefix to with each string returned to get the full word.
        :param prefix:
        :return: list of matching words (from next character after prefix), if found, else empty list
        """
        current_node = self._trie.get_next_node(prefix)
        if not current_node:
            return None

        all_words = []
        return self._trie.collect_all_words(current_node, '', all_words)


class TextAutoCompleteText(unittest.TestCase):
    def test_should_find_two_words(self):
        autocomplete = TextAutoComplete(['Hat', 'Hatton', 'public', 'private'])
        result = autocomplete.autocomplete('Ha')

        print(result)
        self.assertEqual(2, len(result))

    def test_multiple_searches(self):
        autocomplete = TextAutoComplete(['Hat', 'Hatton', 'public', 'private'])

        result = autocomplete.autocomplete('p')
        self.assertEqual('ublic', result[0])
        self.assertEqual('rivate', result[1])

        self.assertEqual(2, len(result))

        result = autocomplete.autocomplete('pu')
        self.assertEqual('blic', result[0])
        self.assertEqual(1, len(result))

        result = autocomplete.autocomplete('pr')
        self.assertEqual('ivate', result[0])
        self.assertEqual(1, len(result))
