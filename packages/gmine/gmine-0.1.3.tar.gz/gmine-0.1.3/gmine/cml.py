import argparse

# Initiate
parser = argparse.ArgumentParser(
    fromfile_prefix_chars='@',
    prog="gmine",
    description="Text mining with custom cnf",
)

# Positional
parser.add_argument(
    "file_name", type=str,
    help="Path of the input file",
)
parser.add_argument(
    "cnf", type=str,
    help="The filter condition expressed in conjunctive normal form",
)

# Flags
parser.add_argument(
    "-c", "--column-name", type=str,
    help="Target column name. If not specified, 'Report Event/Describe the facts of what happened' will be used."
)
parser.add_argument(
    "-o", "--output-name", type=str,
    help="Output file name. If not specified, 'original file name' + '_f' will be used.",
)

parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")

# Parse
args = parser.parse_args()