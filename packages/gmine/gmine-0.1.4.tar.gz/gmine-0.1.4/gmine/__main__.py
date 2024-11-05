from .cml import args
from .core import labour

DEFAULT_COL = "Report Event/Describe the facts of what happened"

clean_name = args.file_name
clean_name = clean_name.removesuffix(".csv")
DEFAULT_OUT = clean_name + "_filtered" + ".csv"

if __name__ == '__main__':
    col = DEFAULT_COL if not args.column_name else args.column_name
    nfile = DEFAULT_OUT if not args.output_name else args.output_name

    labour(args.file_name, col, args.cnf, nfile)
    # print(args.file_name, col, args.cnf, nfile)