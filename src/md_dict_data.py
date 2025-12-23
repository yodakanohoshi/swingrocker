"""
マークダウンデータを辞書形式で保持・操作するモジュール
"""

from dataclasses import dataclass
from typing import Self

paragraph_key_types = str | None

@dataclass()
class Header:
    """
    ヘッダーの構造、MDDictDataとほかのオブジェクトの通信に使用される。
    単なるデータの内容だけでなく、キーを含み取り回しを容易にする。
    
    Attributes:
        key: ヘッダーのキー
        lines: ヘッダーに属する行のリスト
    """
    key: paragraph_key_types
    lines: list[str]

@dataclass()
class MDDictData:
    """
    Markdownのパース結果を保持するデータ構造
    Attributes:
        paragraph_dict: ヘッダーキーとその行リストの辞書
    """
    paragraph_dict: dict[paragraph_key_types, list[str]]

    def to_markdown(self) -> str:
        output = ""
        for key, lines in self.paragraph_dict.items():
            if key is not None:
                output += f"# {key}\n"
            output += "\n".join(lines) + "\n"
        return output
    
    def get(self, key: paragraph_key_types) -> Header:
        return Header(key, self.paragraph_dict.get(key, None))
    
    def update(self, header: Header) -> Self:
        self.paragraph_dict[header.key] = header.lines
        return self
    
    @classmethod
    def from_markdown(cls, content: str) -> "MDDictData":
        headers = {}
        current_header = None
        for line in content.splitlines():
            if line.startswith("# "):
                current_header = line[2:].strip()
                headers[current_header] = []
            elif current_header:
                headers[current_header].append(line)
        return cls(paragraph_dict=headers)
    
if __name__ == "__main__":
    def upascale_example(header: Header) -> Header:
        upscaled_lines = [line.upper() for line in header.lines]
        header.lines = upscaled_lines
        return header


    def main():
        sample_md = """# Header1
                This is some text under header 1.
                """ 
        md_dict = MDDictData.from_markdown(sample_md)
        header = md_dict.get("Header1")
        header = upascale_example(header) 
        md_dict.update(header)
        print(md_dict.to_markdown())
    main()