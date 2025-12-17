import argparse
import pathlib
from markdown_processor import MarkdownIO
import glob

def main(args):
    dir_name = args.dir
    base_path = pathlib.Path(dir_name)

    asis_dir = base_path / "asis"
    asis_dir.mkdir(parents=True, exist_ok=True)

    markdown_path = base_path / "main.md"

    asis_md_list = glob.glob(str(asis_dir / "**/0.md"))

    # get seed list main.md
    md_io = MarkdownIO(base_path, markdown_path)
    md_io.process()
    # asis_md
    for asis_md in asis_md_list:
        asis_md_path = pathlib.Path(asis_md)
        md_io = MarkdownIO(base_path, asis_md_path)
        md_io.process()


def get_args():
    parser = argparse.ArgumentParser(description="A simple Hello World program.")
    parser.add_argument("--dir", type=str, required=True, help="workdir")
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    main(args)