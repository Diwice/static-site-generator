import os
import shutil
from copy import *
from page_generator import *

def main() :
    shutil.rmtree(os.path.abspath("./public"))
    os.mkdir(os.path.abspath("./public"))

    copy_static()
    generate_page("content/index.md", "template.html", "public/index.html")    

if __name__ == "__main__" :
    main()
