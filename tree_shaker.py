import os
import json
import argparse
from pybtex.database import parse_file, BibliographyData
from pylatexenc.latexwalker import LatexWalker, LatexMacroNode, LatexCharsNode
from tqdm import tqdm


def strip_array(arr):
    return list(map(lambda x: x.strip(), arr))


def find_citation_keys(tex_content):
    walker = LatexWalker(tex_content)
    nodes, _, _ = walker.get_latex_nodes()

    citation_keys = []
    for node in nodes:
        if isinstance(node, LatexMacroNode) and node.macroname == "cite":
            if (
                node.nodeargd
                and node.nodeargd.argnlist
                and len(node.nodeargd.argnlist) > 0
            ):
                for arg in node.nodeargd.argnlist:
                    if arg and arg.nodelist:
                        for subnode in arg.nodelist:
                            if isinstance(subnode, LatexCharsNode):
                                keys = subnode.chars.split(",")
                                keys = strip_array(keys)
                                citation_keys.extend(keys)
                            elif (
                                isinstance(subnode, LatexMacroNode) and subnode.nodeargd
                            ):
                                # Handling deeper macros, just in case
                                deeper_keys = "".join(
                                    n.chars
                                    for n in subnode.nodeargd.argnlist
                                    if isinstance(n, LatexCharsNode)
                                )
                                deeper_keys = strip_array(deeper_keys.split(","))
                                citation_keys.extend(deeper_keys)
    return citation_keys


def filter_bib_entries(bib_database, keys_to_keep):
    # Filter the entries in the BibTeX database
    filtered_entries = {
        key: bib_database.entries[key]
        for key in keys_to_keep
        if key in bib_database.entries
    }
    return BibliographyData(entries=filtered_entries)


def tree_shake(root_directory, input_bib_path, output_bib_path, output_keys_path):
    # List to hold all citation keys
    all_citation_keys = []

    # Walk through the directory and its subdirectories
    full_tree = list(os.walk(root_directory))
    for dirpath, _, filenames in tqdm(full_tree, desc="Processing LaTeX files"):
        for filename in filenames:
            if filename.endswith(".tex"):
                # Full path to the file
                filepath = os.path.join(dirpath, filename)
                # Read the content of the file
                with open(filepath, "r", encoding="utf-8") as file:
                    content = file.read()
                    # Extract citation keys from this file
                    citation_keys = find_citation_keys(content)
                    # Add them to the list
                    all_citation_keys.extend(citation_keys)

    # Remove duplicates and sort
    all_citation_keys = sorted(set(all_citation_keys))

    # Parse the BibTeX file using pybtex
    bib_database = parse_file(input_bib_path)

    # Filter the BibTeX entries
    filtered_bib_database = filter_bib_entries(bib_database, all_citation_keys)

    # Write the filtered entries to a new BibTeX file
    with open(output_bib_path, "w", encoding="utf-8") as output_file:
        filtered_bib_database.to_file(output_file)

    # Write the list of citation keys to a JSON file
    with open(output_keys_path, "w", encoding="utf-8") as f:
        json.dump(all_citation_keys, f, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process LaTeX files to extract and filter BibTeX entries."
    )
    parser.add_argument(
        "--root_directory",
        default="./latex_files",
        help="Root directory containing the .tex files.",
    )
    parser.add_argument(
        "--input_bib_path",
        default="./artifacts/raw.bib",
        help="Path to the input BibTeX file.",
    )
    parser.add_argument(
        "--output_bib_path",
        default="./artifacts/shaken_raw.bib",
        help="Path to save the filtered BibTeX entries.",
    )
    parser.add_argument(
        "--output_keys_path",
        default="./artifacts/citation_keys.json",
        help="Path to save the extracted citation keys in JSON format.",
    )

    args = parser.parse_args()

    tree_shake(
        args.root_directory,
        args.input_bib_path,
        args.output_bib_path,
        args.output_keys_path,
    )
