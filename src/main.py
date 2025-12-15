import argparse
import pathlib
from markdown_processor import MarkdownIO

def main(args):
    dir_name = args.dir
    base_path = pathlib.Path(dir_name)

    markdown_path = args.markdown

    asis_dir = base_path / "asis"
    asis_dir.mkdir(parents=True, exist_ok=True)

    # get seed list
    md_io = MarkdownIO(base_path, markdown_path)
    md_io.process()

def get_args():
    parser = argparse.ArgumentParser(description="A simple Hello World program.")
    parser.add_argument("--dir", type=str, required=True, help="workdir")
    parser.add_argument("--markdown", type=pathlib.Path, required=True, help="target markdown file")
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    main(args)