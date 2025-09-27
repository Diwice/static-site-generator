import re
from textnode import *
from htmlnode import LeafNode

def split_nodes_delimeter(old_nodes, delimeter, text_type) :
	new_nodes = []

	for node in old_nodes :
		if node.text_type is not TextType.TEXT :
			new_nodes.append(node)
			continue

		if node.text.count(delimeter) < 2 or node.text.count(delimeter) % 2 != 0 :
			raise Exception(f"Invalid Markdown Syntax : missing or not closed delimeter / text - '{node.text}' / delimeter - '{delimeter}'")

		split_text = node.text.split(delimeter)
		new_nodes.extend([LeafNode(tag=text_type.value, value=i) if split_text.index(i) % 2 != 0 else LeafNode(value=i) for i in split_text if i])

	return new_nodes

def extract_markdown_links(node) :
	res_matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", node.text)
	return res_matches if res_matches else None

def extract_markdown_images(node) :
	res_matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", node.text)
	return res_matches if res_matches else None

