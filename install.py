"""Installtion script for WordSeer.
"""
import argparse
import shutil
import os
import pdb
import subprocess
import urllib2
import zipfile
import gzip
import glob

# Config
# Location of CoreNLP
CORENLP = "http://nlp.stanford.edu/software/stanford-corenlp-full-2013-06-20.zip"
# Location of libxml for macs
LIBXML_MAC = "http://www.explain.com.au/download/combo-2007-10-07.dmg.gz"
# Path to requirements file
REQUIREMENTS = "requirements.txt"
# Directory to save corenlp to
CORENLP_LOCAL_DIR = "./"
# Directory name for the corenlp tree
CORENLP_LOCAL_NAME = "stanford-corenlp"

CORENLP_LOCAL_PATH = os.path.join(CORENLP_LOCAL_DIR, CORENLP_LOCAL_NAME)
CORENLP_ZIP_DIRECTORY = os.path.splitext(os.path.basename(CORENLP))[0]

def download_file(src, dest):
    """Download a file using urllib2.
    """
    source_file = urllib2.urlopen(src)
    with open(dest, "w") as local_file:
        local_file.write(source_file.read())

def install_prerequisites():
    """Install requirements that we can't install in a virtual environment.
    """
    system = subprocess.check_output(["uname", "-a"])

    if "Linux" in system:
        print "Attempting to install prerequisites for linux."
        if "ARCH" in system:
            subprocess.call(["sudo pacman -S libxslt libxml2 jre7-openjdk"])
        elif "Ubuntu" in system:
            subprocess.call(["sudo apt-get install libxml2 libxslt1.1 openjdk-7-jre"])
    elif "Darwin" in system:
        print "Installing prerequisites for mac."
        download_file(LIBXML_MAC, "libxml.dmg.gz")
        with gzip.GzipFile("libxml.dmg.gz") as local_zip,\
            open("libxml.dmg", "w") as local_dmg:
                local_dmg.write(local_zip.read())
        os.remove("libxml.dmg.gz")
        mounting = subprocess.check_output(["hdiutil", "mount", "libxml.dmg"])
        mountpoint = mounting.split("\n")[-2].split()[2]
        frameworks = glob.glob(mountpoint + "/*.framework")
        for framework in frameworks:
            subprocess.call(["sudo", "cp", "-r", framework, "/Library/Frameworks"])
            #shutil.move(framework, "/Library/Frameworks")
        executables = [os.path.join(mountpoint, "xmllint"),
                os.path.join(mountpoint, "xsltproc"),
                os.path.join(mountpoint, "xmlcatalog")]
        for executable in executables:
            subprocess.call(["sudo", "cp", executable, "/usr/bin"])
            #shutil.move(executable, "/usr/bin")
        subprocess.call(["hdiutil", "unmount", mountpoint])
    else:
        print ("Could not identify operating system, prerequisite installation "
        "failed.")

def install_interactively():
    """Install while prompting the user.
    """
    print ("You can either perform a full install or a partial install, just "
        "enough to run the interactive wordseer tool.")
    while True:
        install_libxml = raw_input("Perform full install? (y/n)").lower()
        if install_libxml in ["y", "n"]:
            break

    if install_libxml == "y":
        print "Performing full install."
        install_prerequisites()

    else:
        print "Performing partial install."

    print ("The python packages can be installed inside a virtual environment, "
        "which is a cleaner way to install the dependencies.")
    while True:
        use_virtualenv = raw_input("Use virtualenv? (y/n)").lower()
        if use_virtualenv in ["y", "n"]:
            break

    if use_virtualenv == "y":
        print "Using virtualenv."



def main():
    """Perform the installation process.
    """
    parser = argparse.ArgumentParser(
        description="Install wordseer's requirements.")
    parser.add_argument("--sudo", action="store_true",
        help="Use sudo to install some dependencies")
    parser.add_argument("-i", "--interactive", action="store_true",
        help="Run interactively. This supersedes all other options.")
    parser.add_argument("-v", "--virtualenv", action="store_true",
        help="Run interactively.")
    args = parser.parse_args()

    if args.interactive:
        install_interactively()

    if args.sudo:
        install_prerequisites()

    # Install things
    print "Installing python dependencies"
    subprocess.call(["pip install -r " + REQUIREMENTS],
        shell=True)

    subprocess.call(["python -m nltk.downloader punkt"], shell=True)

    print "Setting up database..."
    subprocess.call(["python database.py reset"], shell=True)

    print "Installing stanford-corenlp"
    source_file = urllib2.urlopen(CORENLP)

    with open("corenlp.zip", "w") as local_file:
        local_file.write(source_file.read())

    with zipfile.ZipFile("corenlp.zip", "r") as local_zip:
        local_zip.extractall()

    shutil.move(CORENLP_ZIP_DIRECTORY, CORENLP_LOCAL_PATH)

    print "Cleaning up..."
    os.remove("corenlp.zip")


if __name__ == "__main__":
    main()

