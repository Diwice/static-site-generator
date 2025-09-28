import re
from enum import Enum

class BlockType(Enum) :
	paragraph = None
	heading = None
	code = None
	quote = None
	unordered_list = None
	ordered_list = None

def markdown_to_blocks(markdown) :
	res = markdown.split("\n\n")

	return [i.strip() for i in res if i]

def block_to_block_type(block) :
	ord_list_sub = []

	if re.match(r"#{1,6}\s", block) :
		return BlockType.heading
	elif re.match(r"`{3}.+`{3}", block) :
		return BlockType.code
	elif all(i[0] == ">" for i in block.split("\n")) :
		return BlockType.quote
	elif all(i[0:2] == "- " for i in block.split("\n")) :
		return BlockType.unordered_list
	elif all(re.match(r"^\d+\.\s", i) and not(ord_list_sub.append(int(i[0]))) for i in block.split("\n")) :
		if all(ord_list_sub[i] == ord_list_sub[i+1] - 1 for i in range(len(ord_list_sub)-1)) :
			return BlockType.ordered_list

	return BlockType.paragraph
