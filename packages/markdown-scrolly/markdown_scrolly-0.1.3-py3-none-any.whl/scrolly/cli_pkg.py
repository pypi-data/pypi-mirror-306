import argparse
try:
    from html_packager import package_file
except:
    from .html_packager import package_file

def main():

    #### fname, signature='', date='today', extensions=[]):
    parser = argparse.ArgumentParser(
        prog = 'html_packager',
        description='Package a html file including css, scripts and images in one file.',
        epilog= '\n'
    )
    parser.add_argument(
        "filename", type=str, 
        help="The filename of the html to be processed"
    )

    args = parser.parse_args()

        
    package_file(args.filename)

if __name__ == "__main__":
    main()