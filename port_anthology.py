import re
import argparse
from pybtex.database import parse_file
from pybtex.database import BibliographyData
from tqdm import tqdm


def clean_title(title):
    # Remove all special characters except alphanumeric and spaces
    return re.sub(r"[^a-zA-Z0-9\s]", "", title)


def read_bib_file(file_path):
    try:
        return parse_file(file_path)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None


def write_bib_file(bib_data, file_path):
    try:
        with open(file_path, "w", encoding="utf-8") as bib_file:
            bib_data.to_file(bib_file)
    except Exception as e:
        print(f"Error writing {file_path}: {e}")


def main(raw_bib_path, input_anthology_path, output_anthology_path, output_custom_path):
    print("Parsing", raw_bib_path)
    raw_bib = read_bib_file(raw_bib_path)
    print("Parsing done")

    print("Parsing", input_anthology_path)
    input_anthology = read_bib_file(input_anthology_path)
    print("Parsing done")

    if raw_bib is None or input_anthology is None:
        return

    # Dictionary to store titles from input anthology
    anthology_titles = {
        clean_title(entry.fields.get("title", "")).lower(): key
        for key, entry in tqdm(
            input_anthology.entries.items(), desc="Processing input anthology"
        )
    }

    matching_entries = {}
    non_matching_entries = {}

    # Processing raw.bib entries with tqdm
    for key, entry in tqdm(raw_bib.entries.items(), desc="Comparing entries"):
        title = clean_title(entry.fields.get("title", "")).lower()
        if title in anthology_titles:
            # Use the entry from input anthology but with the key from raw.bib
            matching_entries[key] = input_anthology.entries[anthology_titles[title]]
        else:
            non_matching_entries[key] = entry

    # Convert dictionaries to BibliographyData objects
    matching_bib_data = BibliographyData(entries=matching_entries)
    non_matching_bib_data = BibliographyData(entries=non_matching_entries)

    # Write results to files with tqdm for progress indication
    print("Writing matching entries to", output_anthology_path)
    write_bib_file(matching_bib_data, output_anthology_path)
    print("Writing non-matching entries to", output_custom_path)
    write_bib_file(non_matching_bib_data, output_custom_path)

    print("Operation completed")


# Command-line argument parsing
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Match BibTeX entries by title and separate them."
    )

    # Define optional arguments with default values
    parser.add_argument(
        "--raw_bib_path",
        default="./artifacts/shaken_raw.bib",
        help="Path to the raw BibTeX file.",
    )
    parser.add_argument(
        "--input_anthology_path",
        default="./artifacts/input_anthology.bib",
        help="Path to the input anthology BibTeX file.",
    )
    parser.add_argument(
        "--output_anthology_path",
        default="./artifacts/anthology.bib",
        help="Path to save the matching BibTeX entries.",
    )
    parser.add_argument(
        "--output_custom_path",
        default="./artifacts/custom.bib",
        help="Path to save the non-matching BibTeX entries.",
    )

    args = parser.parse_args()

    main(
        args.raw_bib_path,
        args.input_anthology_path,
        args.output_anthology_path,
        args.output_custom_path,
    )
