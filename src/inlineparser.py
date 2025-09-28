import re
from textnode import *
from htmlnode import LeafNode

def split_nodes_delimeter(old_nodes, delimeter, text_type) :
	new_nodes = []

	for node in old_nodes :
		if node.text_type is not TextType.TEXT :
			new_nodes.append(node)
			continue

		if not(node.text.count(delimeter)) :
			new_nodes.append(node)
			continue

		if node.text.count(delimeter) < 2 or node.text.count(delimeter) % 2 != 0 :
			raise Exception(f"Invalid Markdown Syntax : missing or not closed delimeter / text - '{node.text}' / delimeter - '{delimeter}'")

		split_text = node.text.split(delimeter)
		new_nodes.extend([TextNode(i, text_type) if split_text.index(i) % 2 != 0 else TextNode(i, TextType.TEXT) for i in split_text if i])

	return new_nodes

def extract_markdown_images(node) :
        res_matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", node.text)
        return res_matches if res_matches else None

def extract_markdown_links(node) :
	res_matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", node.text)
	return res_matches if res_matches else None

def split_nodes_image(old_nodes):
	new_nodes = []
	pattern = re.compile(r'!\[([^\[\]]*)\]\(([^\(\)]*)\)')

	for node in old_nodes:
		if node.text_type != TextType.TEXT:
			new_nodes.append(node)
			continue

		text = node.text
		i = 0

		matched = False
		for m in pattern.finditer(text):
			matched = True

			if m.start() > i:
				new_nodes.append(TextNode(text[i:m.start()], TextType.TEXT))
			new_nodes.append(TextNode(m.group(1), TextType.IMAGE, m.group(2)))

			i = m.end()

		if matched:
			if i < len(text):
				new_nodes.append(TextNode(text[i:], TextType.TEXT))
		else:
			new_nodes.append(node)

	return new_nodes

def split_nodes_link(old_nodes):
	new_nodes = []
	pattern = re.compile(r'(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)')

	for node in old_nodes:
		if node.text_type != TextType.TEXT:
			new_nodes.append(node)
			continue

		text = node.text
		i = 0

		matched = False
		for m in pattern.finditer(text):
			matched = True

			if m.start() > i:
				new_nodes.append(TextNode(text[i:m.start()], TextType.TEXT))
			new_nodes.append(TextNode(m.group(1), TextType.LINK, m.group(2)))

			i = m.end()

		if matched:
			if i < len(text):
				new_nodes.append(TextNode(text[i:], TextType.TEXT))
		else:
			new_nodes.append(node)

	return new_nodes

def text_to_textnodes(text) :
	processed_nodes = [TextNode(text, TextType.TEXT)]

	processed_nodes = split_nodes_image(processed_nodes)
	processed_nodes = split_nodes_link(processed_nodes)

	processed_nodes = split_nodes_delimeter(processed_nodes, "**", TextType.BOLD)
	processed_nodes = split_nodes_delimeter(processed_nodes, "_", TextType.ITALIC)
	processed_nodes = split_nodes_delimeter(processed_nodes, "`", TextType.CODE)

	return processed_nodes
