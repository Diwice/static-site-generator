import unittest
from htmlnode import *

class TestHTMLNode(unittest.TestCase) :
	def test_eq(self) :
		node = HTMLNode("p","unodostres",None,{"href":"https://www.google.com"})
		node2 = HTMLNode("p","unodostres",None,{"href":"https://www.google.com"})
		self.assertEqual(node, node2)

	def test_uneq(self) :
		node = HTMLNode("p","unodostres",None,{"href":"https://www.google.com"})
		node2 = HTMLNode("p","unodostres",None,{"href":"https://www.yandex.com"})
		self.assertNotEqual(node, node2)

	def test_props(self) :
		props = HTMLNode("p","unodostres",None,{"href":"https://www.google.com"}).props_to_html()
		props2 = HTMLNode("p","unodostres",None,{"href":"https://www.google.com"}).props_to_html()
		self.assertEqual(props, props2)

	def test_leaf_creation(self) :
		node = LeafNode(value="lol")
		self.assertEqual(node.value, "lol")

	def test_leaf_to_html_p(self) :
		node = LeafNode("p","Hello, world!")
		self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

	def test_leaf_to_html_with_href(self) :
		node = LeafNode("p", "Hello, world!", {"href":"https://google.com"})
		self.assertEqual(node.to_html(), '<p href="https://google.com">Hello, world!</p>')

	def test_leaf_node_plain_text(self) :
		node = LeafNode(None, "Hello, world!")
		self.assertEqual(node.to_html(), "Hello, world!")

	def test_leaf_node_absent_value(self) :
		node = LeafNode("p", None)
		with self.assertRaises(ValueError) as e :
			node.to_html()
		self.assertTrue(type(e.exception), ValueError)

	def test_to_html_with_children(self) :
		child_node = LeafNode("span", "child")
		parent_node = ParentNode("div", [child_node])
		self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

	def test_to_html_with_grandchildren(self) :
		grandchild_node = LeafNode("b", "grandchild")
		child_node = ParentNode("span", [grandchild_node])
		parent_node = ParentNode("div", [child_node])
		self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")

	def test_parent_node_absent_tag(self) :
		parent_node = ParentNode(None, [LeafNode("b", "grandchild")])
		with self.assertRaises(ValueError) as e :
			parent_node.to_html()
		self.assertTrue(type(e.exception), ValueError)

	def test_parent_node_absent_children(self) :
		parent_node = ParentNode("b", [])
		with self.assertRaises(ValueError) as e :
			parent_node.to_html()
		self.assertTrue(type(e.exception), ValueError)

	def test_text(self) :
		node = TextNode("This is a text node", TextType.TEXT)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, None)
		self.assertEqual(html_node.value, "This is a text node")
		self.assertEqual(html_node.to_html(), "This is a text node")

	def test_text_italic(self) :
		node = TextNode("This is an italic node", TextType.ITALIC)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "i")
		self.assertEqual(html_node.value, "This is an italic node")
		self.assertEqual(html_node.to_html(), "<i>This is an italic node</i>")

	def test_text_image(self) :
		node = TextNode("This is an image node", TextType.IMAGE, "https://9p.io/plan9/img/plan9bunnywhite.jpg")
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "img")
		self.assertEqual(html_node.value, "")
		self.assertEqual(html_node.props, {"src":"https://9p.io/plan9/img/plan9bunnywhite.jpg","alt":"This is an image node"})
		self.assertEqual(html_node.to_html(), '<img src="https://9p.io/plan9/img/plan9bunnywhite.jpg" alt="This is an image node"></img>')

	def test_text_unknown_type(self) :
		node = TextNode("This is an unknown node", "unknown")
		with self.assertRaises(Exception) as e :
			text_node_to_html_node(node)
		self.assertTrue(type(e.exception), Exception)

if __name__ == "__main__":
	unittest.main()
