#!/usr/local/bin/python
import sys
import getopt
import datetime
import os
import shutil
from TagDictionary import TagDictionary

def print_help():
    print("Usage: zk <command>\n")
    print("-n, --new    - create new note")
    print("-i, --index  - indexes current notes and creates index pages")
    print("-g, --github - prepares repository to be published to GitHub")
    print("-h, --help   - displays this help page")

def create_new_note():
    while True:
        date_time = datetime.datetime.now()
        date = date_time.strftime("%Y%m%d-%H%M%S")
        file_name = input("Enter file name: ")

        if file_name == "end":
            sys.exit()

        file_name = date + "-" + file_name.replace(" ", "-") +".md"
        print(file_name)

        print("Begin typing note:")
        note = input(">> ")
        
        tags = input("\nAdd tags (seperate tags by ','): ")

        file = open(file_name, "w+")
        file.write("[//]: %s\n" % file_name)
        file.write("# %s\n" % file_name)
        file.write("TAGS=%s\n" % tags)
        file.write("### Begin Note>>>\n")
        file.write("%s\n" % note)
        file.close()

def create_tags():
    if os.path.exists(".tags"):
        shutil.rmtree(".tags")
    
    for file in os.listdir(os.getcwd()):
        tag_line = ""
        tag_list =[]
        if os.path.isfile(file) and file.endswith(".md"):
            if not file.startswith("index.md"):
                with open(file) as f:
                    for line in f:
                        if line.startswith("TAGS="):
                            tag_line = line
                            break
                if tag_line != "":
                    tag_line = tag_line.lstrip("TAGS=")
                    tag_line = tag_line.rstrip("\n")
                    tag_list = tag_line.split(',')
                    tag_list = [tag.strip() for tag in tag_list]
            # for tag in tag_list:
                # TagDictionary.addFile(tag, file)
    print(os.path.basename(os.getcwd()))

def create_index_file():
    current_dir = os.path.basename(os.getcwd())
    file = open("index.md", "w+")
    file.write("# %s\n" % current_dir)
    file.close()

def index_files():
    create_index_file()
    index = open("index.md", "a")

    for file in os.listdir(os.getcwd()):
        if os.path.isfile(file) and file.endswith(".md"):
            if not file.startswith("index.md"):
                index.write("[%s](%s) \n" % (file, file))
        elif os.path.isdir(file):
            if not file.startswith(".") and not file.startswith("__pycache__"):
                os.chdir(file)
                index_files()
                os.chdir("..")
            else:
                print("Skipping %s", file)
    
    index.write("## Subdirectories\n")
    for file in os.listdir(os.getcwd()):
        if not file.startswith(".") and not file.startswith("__pycache__") and os.path.isdir(file):
            index.write("[%s](%s/index.md) \n" % (file, file))
    index.close()

    create_tags()

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hign",["help","index","github","new"])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-n", "--new"):
            create_new_note()
            sys.exit()
        elif opt in ("-i", "--index"):
            index_files()
            sys.exit()
        elif opt in ("-g", "--github"):
            print("GITHUB")
            sys.exit()
        elif opt in ("-h", "--help"):
            print_help()
            sys.exit()

if __name__ == "__main__":
    main(sys.argv[1:])