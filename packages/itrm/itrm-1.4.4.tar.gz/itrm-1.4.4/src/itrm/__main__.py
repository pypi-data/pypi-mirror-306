import os
import argparse
import itrm
import numpy as np

def main():
    # Parse the arguments.
    parser = argparse.ArgumentParser(
            description="Interactive terminal utilities")
    parser.add_argument("--func", "-f", type=str,
            choices=["iplot"], default="iplot",
            help="which function to use")
    parser.add_argument("--type", "-t", type=str,
            choices=[None, "txt", "csv", "bin"], default=None,
            help="file type of data file")
    parser.add_argument("--columns", "-c", type=int, default=0,
            help="number of columns in the data file")
    parser.add_argument("file", type=str,
            help="the data file to read")
    args = parser.parse_args()

    # Early exit if the file does not exist.
    if not os.path.exists(args.file):
        raise ValueError("The file does not exist.")

    # Check the extension.
    if args.type is None:
        _, extension = os.path.splitext(args.file)
        if extension.lower() == ".txt":
            args.type = "txt"
        if extension.lower() == ".csv":
            args.type = "csv"
        if extension.lower() == ".bin":
            args.type = "bin"

    # Read the data.
    if args.type == "bin":
        data_raw = np.fromfile(args.file)
        if args.columns == 0:
            N = len(data_raw)
            factors = [i for i in range(1, N//2 + 1) if not N % i]
            min_jumps = np.inf
            min_jumps_cols = 0
            for cols in factors:
                M = data_raw.reshape((-1, cols)).T
                mean_diffs = np.mean(np.abs(np.diff(M, axis=1)), axis=1)
                ranges = np.max(M, axis=1) - np.min(M, axis=1)
                jumps = np.sqrt(np.mean((mean_diffs/ranges)**2))
                if jumps < min_jumps:
                    min_jumps = jumps
                    min_jumps_cols = cols
            args.columns = min_jumps_cols
        data = data_raw.reshape((-1, args.columns)).T
    elif args.type == "csv":
        data = np.loadtxt(args.file, delimiter=",").T
    elif args.type == "txt":
        data = np.loadtxt(args.file, delimiter=None).T
    
    # Process the appropriate function.
    if args.func == "iplot":
        if (data.ndim > 1) and (data.shape[0] > 1):
            itrm.iplot(data[0], data[1:])
        else:
            itrm.iplot(data.flatten())

if __name__ == "__main__":
    main()
