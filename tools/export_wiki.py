"""This script exports the wiki pages from Redmine in TXT format.

All wiki pages on Redmine (https://cocomud.plan.io) are saved in the
'doc' directory.

Requirements:
    This script needs 'python-redmine', which you can obtain with
        pip install python-redmine

"""

import argparse
import os
import sys
import urllib2

from redmine import Redmine

# Create an argument parser
parser = argparse.ArgumentParser(
        description="export wiki pages in TXT formats")
parser.add_argument("lang", help="the language code (en, fr, es...)",
        nargs='?', choices=["en", "fr"], default="en")
args = parser.parse_args()

# Configure the system
lang = args.lang
path = os.path.join("..", "doc")

# Connects to the REST API
redmine = Redmine("https://cocomud.plan.io")

# Gets the wiki pages of the documentation
# Note: if the exported documentation is in English (the default),
# then pages are retreived from the 'cocomud-client' project.  Otherwise,
# they are retrieved from the project with the language code (for
# example, 'fr' for French).
if lang == "en":
    project_id = "cocomud-client"
else:
    project_id = lang

# If the exported format is txt, the directory differs

pages = redmine.wiki_page.filter(project_id=project_id)
for page in pages:
    # Write the exported file
    path = os.path.join("..", "doc", page.title + ".txt")
    print "Writing", page.title, "in", path, "version", version
    text = page.text.decode("utf-8").encode("latin-1").replace("\r", "")
    file = open(path, "w")
    file.write(text)
    file.close()
