import os
import re
import json
from pybtex.database import parse_file, BibliographyData
from tqdm import tqdm


def find_citation_keys(tex_content):
    # Regular expression to find all \cite{...}
    pattern = re.compile(r"\\cite\{([^}]+)\}")
    # Find all matches
    matches = pattern.findall(tex_content)
    return matches


def filter_bib_entries(bib_database, keys_to_keep):
    # Filter the entries in the BibTeX database
    filtered_entries = {
        key: bib_database.entries[key]
        for key in keys_to_keep
        if key in bib_database.entries
    }
    return BibliographyData(entries=filtered_entries)


def main():
    # Root directory containing the .tex files
    root_directory = "./latex_files"
    # List to hold all citation keys
    all_citation_keys = []

    # Walk through the directory and its subdirectories
    for dirpath, _, filenames in tqdm(os.walk(root_directory)):
        for filename in filenames:
            if filename.endswith(".tex"):
                # Full path to the file
                filepath = os.path.join(dirpath, filename)
                # Read the content of the file
                with open(filepath, "r") as file:
                    content = file.read()
                    # Extract citation keys from this file
                    citation_keys = find_citation_keys(content)
                    # Add them to the list
                    all_citation_keys.extend(citation_keys)

    # Remove duplicates and sort
    all_citation_keys = sorted(set(all_citation_keys))

    # Parse the BibTeX file using pybtex
    bib_database = parse_file("./raw.bib")

    # Filter the BibTeX entries
    filtered_bib_database = filter_bib_entries(bib_database, all_citation_keys)

    # Write the filtered entries to a new BibTeX file
    with open("./shaken_raw.bib", "w", encoding="utf-8") as output_file:
        filtered_bib_database.to_file(output_file)

    with open("citation_keys.json", "w", encoding="utf-8") as f:
        json.dump(all_citation_keys, f, indent=2)


if __name__ == "__main__":
    main()
