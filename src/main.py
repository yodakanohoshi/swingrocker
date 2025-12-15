import argparse
import pathlib
from markdown_processor import MarkdownIO

def main(args):
    dir_name = args.dir
    base_path = pathlib.Path(dir_name)

    asis_dir = base_path / "asis"
    asis_dir.mkdir(parents=True, exist_ok=True)

    # get seed list
    main_md = base_path / "main.md"
    md_io = MarkdownIO(main_md)
    md_io.process()

def get_args():
    parser = argparse.ArgumentParser(description="A simple Hello World program.")
    parser.add_argument("--dir", type=str, required=True, help="workdir")
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    main(args)