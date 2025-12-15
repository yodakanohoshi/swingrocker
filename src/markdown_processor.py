import uuid
import pathlib

def make_uuid():
    return str(uuid.uuid4())

def convert_to_asis(plan_header, asis_path: pathlib.Path):
    if plan_header is None:
        return None
    lines = plan_header
    asis_lines = []
    for line in lines:
        if line.strip() == "":
            continue
        file_id = make_uuid()
        file_name = f"{file_id}.md"
        asis_lines.append(f"[{line.strip()}](asis/{file_name})")
        asis_dir = asis_path / "asis"
        file_path = asis_dir / file_name
        with open(file_path, "w", encoding="utf-8") as ff:
            ff.write("\n\n")
            ff.write("# 計画\n\n")
            ff.write(f"# 日程\n\n")
            ff.write(f"# TODO\n\n")
    return asis_lines

class Headers():
    def __init__(self, content: str):
        self.headers = self.parse_headers(content)

    def parse_headers(self, content: str):
        headers = {}
        current_header = None
        for line in content.splitlines():
            if line.startswith("# "):
                current_header = line[2:].strip()
                headers[current_header] = []
            elif current_header:
                headers[current_header].append(line)
        return headers

    def add_asis(self, asis_converted_plan):
        if asis_converted_plan is None:
            return
        if "実行" not in self.headers: # "実行" headerがなければ追加
            self.headers["実行"] = []
        self.headers["実行"].extend(asis_converted_plan)
        return self.headers

class MarkdownIO:
    def __init__(self, markdown_path: pathlib.Path):
        self.markdown_path = markdown_path
        self.content = self._read_markdown()

    def _read_markdown(self):
        with open(self.markdown_path, "r", encoding="utf-8") as f:
            return f.read()
    
    def _write_markdown(self, content):
        with open(self.markdown_path, "w", encoding="utf-8") as f:
            f.write(content)

    def process(self):
        headers = Headers(self.content)
        plan_header = headers.headers.get("計画", None)
        if plan_header is None:
            return
        asis_path = self.markdown_path.parent
        asis_converted_plan = convert_to_asis(plan_header, asis_path)
        asis_added_headers = headers.add_asis(asis_converted_plan)
        
        if asis_converted_plan is None:
            return

        output_content = ""
        for header, lines in asis_added_headers.items():
            output_content += f"# {header}\n"
            output_content += "\n".join(lines) + "\n"
        self._write_markdown(output_content)
        return