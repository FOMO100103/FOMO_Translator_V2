import unittest
from translator.core import split_text

class SplitTextTests(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(split_text("", 20), [])

    def test_short_text(self):
        self.assertEqual(split_text("Hello.", 20), ["Hello."])

    def test_long_text_preserves_content(self):
        source = "First sentence. Second sentence. Third sentence."
        chunks = split_text(source, 18)
        self.assertEqual("".join(chunks).replace(" ", ""), source.replace(" ", ""))
        self.assertTrue(all(len(chunk) <= 18 for chunk in chunks))

if __name__ == "__main__":
    unittest.main()
