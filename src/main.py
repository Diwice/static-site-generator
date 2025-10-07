import os
import shutil
from copy import *
from sys import argv
from page_generator import *

def main() :
    base_path = "/" if len(argv) < 2 else argv[1].replace('"',"") 

    shutil.rmtree(os.path.abspath("./docs"))
    os.mkdir(os.path.abspath("./docs"))

    copy_static()
    generate_pages_recursive("content", "template.html", "docs", base_path) 

if __name__ == "__main__" :
    main()
