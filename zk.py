#!/usr/local/bin/python
import sys
import getopt
import datetime

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
            print("INDEX")
            sys.exit()
            # inputfile = arg
        elif opt in ("-g", "--github"):
            print("GITHUB")
            sys.exit()
            # outputfile = arg
        elif opt in ("-h", "--help"):
            print_help()
            sys.exit()

if __name__ == "__main__":
    main(sys.argv[1:])