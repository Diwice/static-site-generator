import unittest
from textnode import *
from splitdelimeter import *

class TestSplitDelimeter(unittest.TestCase) :
	def test_wrong_type_node(self) :
		node = TextNode("This is a `code` node", TextType.CODE)
		new_node = split_nodes_delimeter([node], "`", TextType.CODE)
		self.assertEqual(new_node[0], node)

	def test_wrong_markdown(self) :
		node = TextNode("This is wrong _markdown syntax", TextType.TEXT)
		with self.assertRaises(Exception) as e :
			split_nodes_delimeter([node], "_", TextType.ITALIC)
		self.assertTrue(type(e.exception), Exception) 

	def test_single_delimeter(self) :
		node = TextNode("This is an _italic_ node", TextType.TEXT)
		new_node = split_nodes_delimeter([node], "_", TextType.ITALIC)
		self.assertEqual(len(new_node), 3)
		self.assertEqual(new_node[0].to_html(), "This is an ")
		self.assertEqual(new_node[1].to_html(), "<i>italic</i>")
		self.assertEqual(new_node[2].to_html(), " node")

	def test_multiple_matching_delimeters(self) :
		node = TextNode("This node contains `first code` and `second code` nodes", TextType.TEXT)
		new_node = split_nodes_delimeter([node], "`", TextType.CODE)
		self.assertEqual(len(new_node), 5)
		self.assertEqual(new_node[0].to_html(), "This node contains ")
		self.assertEqual(new_node[1].to_html(), "<code>first code</code>")
		self.assertEqual(new_node[2].to_html(), " and ")
		self.assertEqual(new_node[3].to_html(), "<code>second code</code>")
		self.assertEqual(new_node[4].to_html(), " nodes")
	
	def test_different_delimeters(self) :
		node = TextNode("This node contains `code` and _italic_ nodes", TextType.TEXT)
		new_node = split_nodes_delimeter([node], "_", TextType.ITALIC)
		self.assertEqual(len(new_node), 3)
		self.assertEqual(new_node[0].to_html(), "This node contains `code` and ")
		self.assertEqual(new_node[1].to_html(), "<i>italic</i>")
		self.assertEqual(new_node[2].to_html(), " nodes")

	def test_multiple_nodes(self) :
		nodes = [TextNode("This is the first `code` node", TextType.TEXT), TextNode("And this is a second node of `code`", TextType.TEXT)]
		new_nodes = split_nodes_delimeter(nodes, "`", TextType.CODE)
		self.assertEqual(len(new_nodes), 5)
		self.assertEqual(new_nodes[0].to_html(), "This is the first ")
		self.assertEqual(new_nodes[1].to_html(), "<code>code</code>")
		self.assertEqual(new_nodes[2].to_html(), " node")
		self.assertEqual(new_nodes[3].to_html(), "And this is a second node of ")
		self.assertEqual(new_nodes[4].to_html(), "<code>code</code>")

if __name__ == "__main__" :
	unittest.main()
