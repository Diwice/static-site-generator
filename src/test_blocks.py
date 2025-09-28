import unittest
from blocks import *

class TestBlocks(unittest.TestCase) :
	def test_basic(self) :
		markdown = "This is a basic\n\ntest"
		blocks = markdown_to_blocks(markdown)
		self.assertEqual(blocks, ["This is a basic","test"])

	def test_markdown_to_blocks(self) :
		md = """This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
		blocks = markdown_to_blocks(md)
		self.assertEqual(blocks, ["This is **bolded** paragraph", "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line", "- This is a list\n- with items"])

	def test_paragraph_type(self) :
		block = "Some plain text"
		block_type = block_to_block_type(block)
		self.assertEqual(block_type, BlockType.paragraph)

	def test_heading_type(self) :
		block = "### Some text"
		block_type = block_to_block_type(block)
		self.assertEqual(block_type, BlockType.heading)

	def test_code_type(self) :
		block = "```Some code text```"
		block_type = block_to_block_type(block)
		self.assertEqual(block_type, BlockType.code)

	def test_quote_type(self) :
		block = ">This block\n>is a quote block"
		block_type = block_to_block_type(block)
		self.assertEqual(block_type, BlockType.quote)

	def test_unordered_list_type(self) :
		block = "- unordered\n- list"
		block_type = block_to_block_type(block)
		self.assertEqual(block_type, BlockType.unordered_list)

	def test_ordered_list_type(self) :
		block = "1. This\n2. is\n3. ordered\n4. list"
		block_type = block_to_block_type(block)
		self.assertEqual(block_type, BlockType.ordered_list)

	def test_fake_ordered_list_type(self) :
		block = "1. some\n45. text"
		block_type = block_to_block_type(block)
		self.assertEqual(block_type, BlockType.paragraph)

	def test_mixed_list_type(self) :
		block = "- mixed\n- list\n3. here"
		block_type = block_to_block_type(block)
		self.assertEqual(block_type, BlockType.paragraph)

	def test_paragraphs(self):
		md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
		)

	def test_codeblock(self):
		md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
		)
