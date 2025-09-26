from textnode import TextType, TextNode

class HTMLNode :
	def __init__(self, tag=None, value=None, children=None, props=None) :
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props

	def to_html(self) :
		raise NotImplementedError("Currently not implemented")

	def props_to_html(self) :
		return " ".join([str(i)+f'="{str(self.props[i])}"' for i in self.props])

	def __eq__(self, other) :
		return True if self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props else False

	def __repr__(self) :
		return f"HTMLNode({self.tag},{self.value},{self.children},{self.props})"

class LeafNode(HTMLNode) :
	def __init__(self, tag=None, value=None, props=None) :
		super().__init__(tag=tag, value=value, props=props)

	def to_html(self) :
		if self.value is None :
			raise ValueError("Leaf Node must have a value")

		if not(self.tag) :
			return self.value

		return f"<{self.tag}{' '+super().props_to_html() if self.props else ''}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode) :
	def __init__(self, tag, children, props=None) :
		super().__init__(tag=tag, children=children, props=props)

	def to_html(self) :
		if not(self.tag) :
			raise ValueError("Parent Node must have a tag")

		if not(self.children) :
			raise ValueError("Parent Node must have children")

		return f'<{self.tag}>{"".join([child.to_html() for child in self.children])}</{self.tag}>'

def text_node_to_html_node(node) :
	match node.text_type :
		case TextType.TEXT :
			return LeafNode(value=node.text)
		case TextType.BOLD :
			return LeafNode(tag=node.text_type.value, value=node.text)
		case TextType.ITALIC :
			return LeafNode(tag=node.text_type.value, value=node.text)
		case TextType.CODE :
			return LeafNode(tag=node.text_type.value, value=node.text)
		case TextType.LINK :
			if node.url is None :
				raise ValueError("URL is required for Link TextNode conversion to HTMLNode")
			return LeafNode(tag=node.text_type.value, value=node.text, props={"href":node.url})
		case TextType.IMAGE :
			if node.url is None or node.text is None :
				raise ValueError("Both URL and Text are required for Image TextNode conversion to HTMLNode")
			return LeafNode(tag=node.text_type.value, value="", props={"src":node.url,"alt":node.text})
		case _ :
			raise Exception(f"Unknown TextNode type : {node.text_type}")
