import os
import shutil
from copy import *
from page_generator import *

def main() :
    shutil.rmtree(os.path.abspath("./public"))
    os.mkdir(os.path.abspath("./public"))

    copy_static()
    generate_pages_recursive("content", "template.html", "public") 

if __name__ == "__main__" :
    main()
