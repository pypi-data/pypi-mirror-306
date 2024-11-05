from .cml import args
from .core import labour

DEFAULT_COL = "Report Event/Describe the facts of what happened"
DEFAULT_OUT = args.file_name + "_filtered"

if __name__ == '__main__':
    col = DEFAULT_COL if not args.column_name else args.column_name
    nfile = DEFAULT_OUT if not args.output_name else args.output_name

    labour(args.file_name, col, args.cnf, nfile)
    # print(args.file_name, col, args.cnf, nfile)