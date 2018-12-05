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

from redminelib import Redmine

# Create an argument parser
parser = argparse.ArgumentParser(
        description="export wiki pages in TXT formats")
parser.add_argument("lang", help="the language code (en, fr, es...)",
        nargs='?', choices=["en", "es", "fr"], default="en")
parser.add_argument("-i", "--interactive", action="store_true",
        help="should the program ask a confirmation for each file?")
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
    if args.interactive:
        answer = input("Import '{}' (Y/N)? ".format(
                page.title))
        if answer.lower() != "y":
            continue

    print("Writing", page.title, "in", path)
    text = page.text
    with open(path, "w", encoding="utf-8") as file:
        file.write(text)
        file.close()
