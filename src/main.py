import argparse
import os
from pathlib import Path

from load import load_gfa
from store import graph_to_file, format_choices


def parse_args():
    desc = "Program for converting GFA data to more portable graph formats"
    parser = argparse.ArgumentParser(prog="GFAConverter", description=desc)

    help = "Output file path"
    parser.add_argument("--out", "-o", type=Path, help=help)

    help = "Supported output formats"
    parser.add_argument("--format", "-f", type=str, choices=format_choices(), help=help)
    help = "Input GFA file"
    parser.add_argument("gfafile", type=Path, help=help)

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    try:
        g = load_gfa(args.gfafile)
        parent_dir = args.out.parent
        if not parent_dir:
            os.makedirs(parent_dir, exist_ok=True)
        graph_to_file(g, Path(args.out), args.format)
    except FileNotFoundError:
        print(f"Whoops! No such file {args.gfafile}!")
    except Exception as ex:
        print(f"Something went wrong. Error: {ex}!")
    else:
        print("Finished processing")
