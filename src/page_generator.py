import os
from blocks import markdown_to_html_node, extract_title

def generate_page(from_path, template_path, dest_path, base_path):
    print(f"Generating page from '{from_path}' to '{dest_path}' using '{template_path}'")

    from_path, template_path, dest_path = make_abs(from_path, template_path, dest_path)

    with open(from_path, "r") as f_file:
        md = f_file.read()

    with open(template_path, "r") as t_file:
        template = t_file.read()

    node = markdown_to_html_node(md).to_html()
    title = extract_title(md)

    res = template.replace("{{ Content }}", node).replace("{{ Title }}", title).replace('href="/', f'href="{base_path}').replace('src="/',f'src="{base_path}')

    os.makedirs("/".join(dest_path.split("/")[:-1]), exist_ok=True)

    with open(dest_path, "w") as new_file:
        new_file.write(res)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):
    dir_path_content, dest_dir_path = make_abs(dir_path_content, dest_dir_path)
    sub_items = [os.path.join(dir_path_content, i) for i in os.listdir(dir_path_content)]

    for item in sub_items :
        if not(os.path.isfile(item)) :
            generate_pages_recursive(item, template_path, dest_dir_path+item.replace(dir_path_content, "", 1), base_path)
            continue

        if item.split("/")[-1].split(".")[-1] == "md" :
            generate_page(item, template_path, os.path.join(dest_dir_path, item.split("/")[-1].split(".")[0]+".html"), base_path)

def make_abs(*args) :
    res_list = [os.path.abspath("./"+i) if not(os.path.isabs(i)) else i for i in [*args]]
    return res_list
