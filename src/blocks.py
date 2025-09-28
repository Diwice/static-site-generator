def markdown_to_blocks(markdown) :
	res = markdown.split("\n\n")
	return [i.strip() for i in res if i]
