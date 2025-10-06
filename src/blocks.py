import re
from enum import Enum
from textnode import *
from htmlnode import *
from inlineparser import text_to_textnodes

class BlockType(Enum) :
	paragraph = "p"
	heading = "h"
	code = "pre"
	quote = "blockquote"
	unordered_list = "ul"
	ordered_list = "ol"

def markdown_to_blocks(markdown) :
	res = markdown.split("\n\n")

	return [i.strip() for i in res if i]

def block_to_block_type(block) :
	split_block = block.split("\n")

	if block.startswith(tuple(["#"*i for i in range(1,7)])) :
		return BlockType.heading
	if len(split_block) > 1 and split_block[0].startswith("```") and split_block[-1].startswith("```") :
		return BlockType.code
	if len(split_block) and re.match(r"`{3}.+`{3}", block) :
		return BlockType.code
	if block.startswith(">") :
		for split in split_block :
			if not(split.startswith(">")) :
				return BlockType.paragraph
		return BlockType.quote
	if block.startswith("- ") :
		for split in split_block :
			if not(split.startswith("- ")) :
				return BlockType.paragraph
		return BlockType.unordered_list
	if block.startswith("1. ") :
		i = 1
		for split in split_block :
			if not(split.startswith(f"{i}. ")) :
				return BlockType.paragraph
			i += 1
		return BlockType.ordered_list

	return BlockType.paragraph

def markdown_to_html_node(markdown) :
	main_node = HTMLNode(tag="div", children=[])
	blocks = markdown_to_blocks(markdown)

	for block in blocks :
		block_type = block_to_block_type(block)
		if block_type == BlockType.code :
			splitted_block = block.split("\n")

			if splitted_block and splitted_block[0].strip() == "```" :
				splitted_block.pop(0)
			if splitted_block and splitted_block[-1].strip() == "```" :
				splitted_block.pop()

			inner_text = "\n".join(splitted_block)

			if len(splitted_block) :
				inner_text += "\n"

			code_child = text_node_to_html_node(TextNode(inner_text, TextType.TEXT))

			code_node = HTMLNode(tag="code", children=[code_child])
			pre_node = HTMLNode(tag="pre", children=[code_node])

			main_node.children.append(pre_node)

			continue

		if block_type == BlockType.heading :
			splitted_block = block.split("\n")
			hashtags_count = 0

			for i in splitted_block[0].strip() :
				if i == "#" :
					hashtags_count += 1
				else :
					break

			level = min(max(hashtags_count, 1), 6)
			splitted_block[0] = splitted_block[0][level:].lstrip()

			if not(splitted_block[0]) :
				block_type = BlockType.paragraph
			else :
				converted_nodes = text_to_textnodes(splitted_block[0])
				children = [text_node_to_html_node(i) for i in converted_nodes]

				hnode = HTMLNode(tag=f"h{level}", children=children)

				main_node.children.append(hnode)

				continue

		if block_type == BlockType.unordered_list :
			splitted_block = [i.strip() for i in block.split("\n") if i.strip()]

			children = []
			for split in splitted_block :
				if split.startswith("- ") :
					text = split[2:]
				elif split.startswith("* ") :
					text = split[2:]
				else:
					continue

				converted_nodes = text_to_textnodes(text)
				li_children = [text_node_to_html_node(i) for i in converted_nodes]
				children.append(HTMLNode(tag="li", children=li_children))

			if children :
				ul_node = HTMLNode(tag="ul", children=children)
				main_node.children.append(ul_node)

				continue
			else :
				block_type = BlockType.paragraph

		if block_type == BlockType.ordered_list :
			splitted_block = [i.strip() for i in block.split("\n") if i.strip()]

			children = []
			for split in splitted_block :
				match = re.match(r"^\d+\.\s", split)
				if match :
					text = split[match.end():]
				else :
					continue

				converted_nodes = text_to_textnodes(text)
				li_children = [text_node_to_html_node(i) for i in converted_nodes]
				children.append(HTMLNode(tag="li", children=li_children))

			if children :
				ol_node = HTMLNode(tag="ol", children=children)
				main_node.children.append(ol_node)

				continue
			else :
				block_type = BlockType.paragraph

		if block_type == BlockType.quote :
			splitted_block = [i for i in block.split("\n") if i.strip()]

			cleaned = []
			for i in splitted_block :
				sub = i.lstrip()

				if sub.startswith(">") :
					sub = sub[1:]

					if sub.startswith(" ") :
						sub = sub[1:]

				cleaned.append(sub)

			quote_text = " ".join(i.strip() for i in cleaned if i.strip())

			conversed_nodes = text_to_textnodes(quote_text)
			children = [text_node_to_html_node(i) for i in conversed_nodes]

			q_node = HTMLNode(tag="blockquote", children=children)
			main_node.children.append(q_node)

			continue

		text = " ".join(i.strip() for i in block.split("\n") if i.strip())

		conversed_nodes = text_to_textnodes(text)
		children = [text_node_to_html_node(i) for i in conversed_nodes]

		p_node = HTMLNode(tag="p", children=children)
		main_node.children.append(p_node)

	return main_node

def extract_title(markdown) : # honestly idk where should I put this function so I left it here
    blocks = markdown_to_blocks(markdown)

    for block in blocks :
        if block.startswith("# ") :
            return block.lstrip("# ")

    raise Exception("Passed Markdown does not have an h1 header")
