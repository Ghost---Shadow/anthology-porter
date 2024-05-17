from pybtex.database import parse_file
from pybtex.database import BibliographyData
from tqdm import tqdm


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


def main(raw_bib_path, input_anthology_path):
    print("Parsing", raw_bib_path)
    raw_bib = read_bib_file(raw_bib_path)
    print("Parsing", input_anthology_path)
    input_anthology = read_bib_file(input_anthology_path)

    if raw_bib is None or input_anthology is None:
        return

    # Dictionary to store titles from input anthology
    anthology_titles = {
        entry.fields.get("title", "").lower(): key
        for key, entry in tqdm(input_anthology.entries.items())
    }

    matching_entries = {}
    non_matching_entries = {}

    for key, entry in tqdm(raw_bib.entries.items()):
        title = entry.fields.get("title", "").lower()
        if title in anthology_titles:
            matching_entries[key] = entry
        else:
            non_matching_entries[key] = entry

    # Convert dictionaries to BibliographyData objects
    matching_bib_data = BibliographyData(entries=matching_entries)
    non_matching_bib_data = BibliographyData(entries=non_matching_entries)

    # Write results to files
    write_bib_file(matching_bib_data, "anthology.bib")
    write_bib_file(non_matching_bib_data, "custom.bib")

    print("Matching entries written to anthology.bib")
    print("Non-matching entries written to custom.bib")


# Example usage
if __name__ == "__main__":
    main("raw.bib", "input_anthology.bib")
