import argparse
import uuid
import pathlib

class MarkdownIO:
    def __init__(self, markdown_path: pathlib.Path):
        self.markdown_path = markdown_path
        self.content = self._read_markdown()

    def _read_markdown(self):
        with open(self.markdown_path, "r", encoding="utf-8") as f:
            return f.read()
    
    def write_markdown(self, content):
        with open(self.markdown_path, "w", encoding="utf-8") as f:
            f.write(content)

    def process(self):
        headers = self.parse_headers()
        plan_header = self.get_plan_header(headers)
        asis_converted_plan = self.convert_to_asis(plan_header)
        asis_added_headers = self.add_asis(asis_converted_plan, headers)
        output_content = ""
        for header, lines in asis_added_headers.items():
            output_content += f"# {header}\n"
            output_content += "\n".join(lines) + "\n"
        self.write_markdown(output_content)

    def get_plan_header(self, headers):
        for header, lines in headers.items():
            print(f"header: {header}")
            if "計画" == header:
                return header, lines
        return None, None
    
    def convert_to_asis(self, plan_header):
        if plan_header is None:
            return None
        header, lines = plan_header
        asis_lines = []
        for line in lines:
            if line.strip() == "":
                continue
            file_id = make_uuid()
            file_name = f"{file_id}.md"
            asis_lines.append(f"[{line.strip()}](asis/{file_name})")
            asis_dir = self.markdown_path.parent / "asis"
            file_path = asis_dir / file_name
            with open(file_path, "w", encoding="utf-8") as ff:
                ff.write("\n\n")
                ff.write("# 計画\n\n")
                ff.write(f"# 日程\n\n")
                ff.write(f"# TODO\n\n")
        return asis_lines

    def add_asis(self, asis_converted_plan, headers):
        if asis_converted_plan is None:
            return
        if "実行" not in headers: # "実行" headerがなければ追加
            headers["実行"] = []
        headers["実行"].extend(asis_converted_plan)
        return headers
    
    # header 1層目をキーに辞書で内容を保持する
    def parse_headers(self):
        headers = {}
        current_header = None
        for line in self.content.splitlines():
            if line.startswith("# "):
                current_header = line[2:].strip()
                headers[current_header] = []
            elif current_header:
                headers[current_header].append(line)
        return headers

def make_uuid():
    return str(uuid.uuid4())

def main(args):
    dir_name = args.dir
    base_path = pathlib.Path(dir_name)

    asis_dir = base_path / "asis"
    asis_dir.mkdir(parents=True, exist_ok=True)

    # get seed list
    main_md = base_path / "main.md"
    md_io = MarkdownIO(main_md)
    md_io.process()

    #    for seed in seeds:
    #        file_id = make_uuid()
    #        file_name = f"{file_id}.md"
    #        file_path = asis_dir / file_name
    #        with open(file_path, "w") as ff:
    #            ff.write("# Hello World\n")
    #        f.write(f"[{seed}](asis/{file_id}.md)\n")

def get_args():
    parser = argparse.ArgumentParser(description="A simple Hello World program.")
    parser.add_argument("--dir", type=str, required=True, help="workdir")
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    main(args)