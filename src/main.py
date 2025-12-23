import argparse
import pathlib
from markdown_io import MarkdownIO
import glob
import uuid
import re

def _is_in_asis(asis_path: pathlib.Path, markdown_path: pathlib.Path) -> bool:
    if asis_path in markdown_path.parents:
        return True
    return False

def make_uuid():
    return str(uuid.uuid4())

def convert_to_asis(plan_header, asis_path: pathlib.Path, markdown_path: pathlib.Path):
    if plan_header is None:
        return None
    lines = plan_header
    asis_lines = []
    for line in lines:
        if line.strip() == "":
            continue
        file_id = make_uuid()
        file_name = f"{file_id}/0.md"

        #markdown_pathのparentがasisの場合asisではなく../にする
        if asis_path == markdown_path.parent.parent:
            asis_lines.append(f"[{line.strip()}](../{file_name})")
        else:
            asis_lines.append(f"[{line.strip()}](asis/{file_name})")
        
        file_path = asis_path / file_name
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as ff:
            ff.write("\n\n")
            ff.write("# 計画\n\n")
            ff.write(f"# 日程\n\n")
            ff.write(f"# TODO\n\n")
    return asis_lines

def convert_url(data: str) -> str:
    # 正規表現で確認する,リンクの後は内容にかかわらずマッチさせる
    pattern = r"\[.*?\]\((.*?)\).*"
    match = re.match(pattern, data)
    if match:
        return data
    uuid_str = str(uuid.uuid4())
    return f"[{data}](asis/{uuid_str}/0.md)" 

def task_run(entry_point_path: pathlib.Path):
    asis_dir: pathlib.Path = entry_point_path / "asis"
    asis_dir.mkdir(parents=True, exist_ok=True)
    entry_md_path: pathlib.Path = entry_point_path / "main.md"
    #asis_md_list = asis_dir.glob("**/0.md")

    md_io = MarkdownIO(entry_md_path)
    header = md_io.get_body("計画")

    header.lines = [convert_url(line) for line in header.lines]

    md_io.update_body(header)
    md_io.save()

def main(args):
    workdir = pathlib.Path(args.dir)
    task_run(workdir)

def get_args():
    parser = argparse.ArgumentParser(description="A simple Hello World program.")
    parser.add_argument("--dir", type=str, required=True, help="workdir")
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    main(args)