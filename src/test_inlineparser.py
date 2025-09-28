import unittest
from textnode import *
from inlineparser import *

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

	def test_empty_link_markdown(self) :
		node = TextNode("This node does not contain image nor link", TextType.TEXT)
		parsed_node = extract_markdown_links(node)
		self.assertEqual(parsed_node, None)

	def test_empty_image_markdown(self) :
		node = TextNode("This node does not contain images", TextType.TEXT)
		parsed_node = extract_markdown_images(node)
		self.assertEqual(parsed_node, None)

	def test_extract_link_markdown(self) :
		node = TextNode("This is a link [to google](https://google.com/)", TextType.TEXT)
		parsed_node = extract_markdown_links(node)
		self.assertEqual(parsed_node, [("to google", "https://google.com/")])

	def test_extract_image_markdown(self) :
		node = TextNode("This is an image ![haha funny rabbit](https://9p.io/plan9/img/plan9bunnywhite.jpg)", TextType.TEXT)
		parsed_node = extract_markdown_images(node)
		self.assertEqual(parsed_node, [("haha funny rabbit", "https://9p.io/plan9/img/plan9bunnywhite.jpg")])

	def test_multiple_link_extract(self) :
		node = TextNode("This is a link to youtube [to youtube](https://youtube.com/) and this is a link to google [to google](https://google.com/)", TextType.TEXT)
		parsed_node = extract_markdown_links(node)
		self.assertEqual(parsed_node, [("to youtube", "https://youtube.com/"), ("to google", "https://google.com/")])

	def test_mixed_image_extract(self) :
		node = TextNode("This is Glenda ![Glenda](https://9p.io/plan9/img/plan9bunnywhite.jpg) and this is a link to plan9 [Plan9](https://9p.io/plan9/)", TextType.TEXT)
		parsed_node = extract_markdown_images(node)
		self.assertEqual(parsed_node, [("Glenda", "https://9p.io/plan9/img/plan9bunnywhite.jpg")])

	def test_link_nodes_creation(self) :
		node = TextNode("This node contains a [google](https://google.com/) link", TextType.TEXT)
		new_nodes = split_nodes_link([node])
		self.assertListEqual(new_nodes, [TextNode("This node contains a ", TextType.TEXT), TextNode("google", TextType.LINK, "https://google.com/"), TextNode(" link", TextType.TEXT)])

	def test_image_nodes_creation(self) :
		node = TextNode("This node contains an ![Glenda](https://9p.io/plan9/img/plan9bunnywhite.jpg) image", TextType.TEXT)
		new_nodes = split_nodes_image([node])
		self.assertListEqual(new_nodes, [TextNode("This node contains an ", TextType.TEXT), TextNode("Glenda", TextType.IMAGE, "https://9p.io/plan9/img/plan9bunnywhite.jpg"), TextNode(" image", TextType.TEXT)])

	def test_multiple_image_nodes(self) :
		nodes = [TextNode("This node contains first image ![Glenda](https://9p.io/plan9/img/plan9bunnywhite.jpg)", TextType.TEXT), TextNode("This node contains second image ![Glenda](https://9p.io/plan9/img/plan9bunnywhite.jpg)", TextType.TEXT)]
		new_nodes = split_nodes_image(nodes)
		self.assertListEqual(new_nodes, [TextNode("This node contains first image ", TextType.TEXT), TextNode("Glenda", TextType.IMAGE, "https://9p.io/plan9/img/plan9bunnywhite.jpg"), TextNode("This node contains second image ", TextType.TEXT), TextNode("Glenda", TextType.IMAGE, "https://9p.io/plan9/img/plan9bunnywhite.jpg")])

	def test_split_images(self):
		node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)
		new_nodes = split_nodes_image([node])
		self.assertListEqual([TextNode("This is text with an ", TextType.TEXT), TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"), TextNode(" and another ", TextType.TEXT), TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")],new_nodes)

	def test_multiple_links_single_node(self) :
		node = TextNode("This node contains multiple links : [google](https://google.com/) and [youtube](https://youtube.com/)", TextType.TEXT)
		new_nodes = split_nodes_link([node])
		self.assertListEqual(new_nodes, [TextNode("This node contains multiple links : ", TextType.TEXT), TextNode("google", TextType.LINK, "https://google.com/"), TextNode(" and ", TextType.TEXT), TextNode("youtube", TextType.LINK, "https://youtube.com/")])

	def test_single_link_multiple_nodes(self) :
		nodes = [TextNode("This node contains a link [google](https://google.com/)", TextType.TEXT), TextNode("This node does not contain a link", TextType.TEXT)]
		new_nodes = split_nodes_link(nodes)
		self.assertListEqual(new_nodes, [TextNode("This node contains a link ", TextType.TEXT), TextNode("google", TextType.LINK, "https://google.com/"), TextNode("This node does not contain a link", TextType.TEXT)])

	def test_image_absent_node(self) :
		node = TextNode("This node does not contain a link", TextType.TEXT)
		new_node = split_nodes_link([node])
		self.assertListEqual(new_node, [node])

if __name__ == "__main__" :
	unittest.main()
