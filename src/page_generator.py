import os
from blocks import markdown_to_html_node, extract_title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from '{from_path}' to '{dest_path}' using '{template_path}'")

    from_path = os.path.abspath("./"+from_path) if not(os.path.isabs(from_path)) else from_path
    template_path = os.path.abspath("./"+template_path) if not(os.path.isabs(template_path)) else template_path
    dest_path = os.path.abspath("./"+dest_path) if not(os.path.isabs(dest_path)) else dest_path

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

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    dir_path_content = os.path.abspath("./"+dir_path_content) if not(os.path.isabs(dir_path_content)) else dir_path_content
    dest_dir_path = os.path.abspath("./"+dest_dir_path) if not(os.path.isabs(dest_dir_path)) else dest_dir_path
    sub_items = [os.path.join(dir_path_content, i) for i in os.listdir(dir_path_content)]
    for item in sub_items :
        if not(os.path.isfile(item)) :
            generate_pages_recursive(item, template_path, dest_dir_path+item.replace(dir_path_content, "", 1))
            continue

        if item.split("/")[-1].split(".")[-1] == "md" :
            generate_page(item, template_path, os.path.join(dest_dir_path, item.split("/")[-1].split(".")[0]+".html"))
