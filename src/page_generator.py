import os
from blocks import markdown_to_html_node, extract_title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from '{from_path}' to '{dest_path}' using '{template_path}'")

    from_path, template_path, dest_path = os.path.abspath("./"+from_path), os.path.abspath("./"+template_path), os.path.abspath("./"+dest_path)

    with open(from_path, "r") as f_file:
        md = f_file.read()

    with open(template_path, "r") as t_file:
        template = t_file.read()

    node = markdown_to_html_node(md).to_html()
    title = extract_title(md)

    res = template.replace("{{ Content }}", node).replace("{{ Title }}", title)

    os.makedirs("/".join(dest_path.split("/")[:-1]), exist_ok=True)

    with open(dest_path, "w") as new_file:
        new_file.write(res)
