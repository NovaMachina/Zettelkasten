#!/usr/local/bin/python
import sys
import getopt

def print_help():
    print("Usage: zk <command>\n")
    print("-n, --new    - create new note")
    print("-i, --index  - indexes current notes and creates index pages")
    print("-g, --github - prepares repository to be published to GitHub")
    print("-h, --help   - displays this help page")

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hign",["help","index","github","new"])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-n", "--new"):
            print("NEW")
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