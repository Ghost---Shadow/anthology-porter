# Anthology Porter

This Python script matches BibTeX entries by title and separates them into matching and non-matching entries. It also includes an optional "tree shaking" feature that processes `.tex` files to filter and refine the BibTeX entries based on the citations found within those files.

## Features

- **Match BibTeX Entries**: Matches entries by title from a raw BibTeX file against an input anthology BibTeX file.
- **Tree Shaking**: Processes LaTeX files to extract citation keys and filter the raw BibTeX entries based on these keys.
- **Output Customization**: Saves matching and non-matching BibTeX entries to specified files.

## Prerequisites

Ensure you have Python installed along with the following packages:
- `pybtex`
- `pylatexenc`
- `tqdm`

You can install these using pip:

```bash
pip install pybtex pylatexenc tqdm
```

## Usage

The script provides several command-line options to customize its operation. Below are the available options:

- `--raw_bib_path`: Path to the raw BibTeX file. Default: `./artifacts/raw.bib`
- `--input_anthology_path`: Path to the input anthology BibTeX file. Default: `./artifacts/input_anthology.bib`
- `--output_anthology_path`: Path to save the matching BibTeX entries. Default: `./artifacts/anthology.bib`
- `--output_custom_path`: Path to save the non-matching BibTeX entries. Default: `./artifacts/custom.bib`
- `--tree_shake_directory`: Root directory containing the `.tex` files for tree shaking. Default: `./latex_files`
- `--output_keys_path`: Path to save the extracted citation keys in JSON format. Default: `./artifacts/citation_keys.json`
- `--shaken_bib_path`: Path to save the filtered BibTeX entries after tree shaking. Default: `./artifacts/shaken_raw.bib`
- `--tree_shake`: A flag to enable the tree shaking process.

### Basic Command

To run the script with default paths:

```bash
python port_anthology.py
```

### Customizing Paths

To specify custom paths for the input and output files:

```bash
python port_anthology.py --raw_bib_path "/path/to/raw.bib" --input_anthology_path "/path/to/anthology.bib" --output_anthology_path "/path/to/matching.bib" --output_custom_path "/path/to/non_matching.bib"
```

### Enabling Tree Shaking

To enable tree shaking and specify the directory containing `.tex` files:

```bash
python port_anthology.py --tree_shake --tree_shake_directory "/path/to/latex_files"
```

## Output

- **Matching Entries**: Saved to the file specified by `--output_anthology_path`.
- **Non-Matching Entries**: Saved to the file specified by `--output_custom_path`.
- **Filtered BibTeX Entries**: If tree shaking is enabled, the filtered entries are saved to the path specified by `--shaken_bib_path`.
- **Citation Keys**: If tree shaking is enabled, the extracted citation keys are saved in JSON format to the path specified by `--output_keys_path`.
