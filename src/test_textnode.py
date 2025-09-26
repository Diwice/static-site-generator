import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase) :
	def test_eq(self) :
		node = TextNode("This is a text node", TextType.TEXT)
		node2 = TextNode("This is a text node", TextType.TEXT)
		self.assertEqual(node, node2)

	def test_uneq(self) :
		node = TextNode("This is a text node", TextType.TEXT)
		node2 = TextNode("This is an italic text node", TextType.ITALIC)
		self.assertNotEqual(node, node2)

	def test_url_difference(self) :
		node = TextNode("This is a text node", TextType.TEXT, "https://vittusaatana.com/")
		node2 = TextNode("This is a text node", TextType.TEXT, "https://boot.dev/")
		self.assertNotEqual(node.url, node2.url)

if __name__ == "__main__" :
	unittest.main()
