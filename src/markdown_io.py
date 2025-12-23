"""
マークダウンファイルの入出力と、1層目のヘッダー操作を行うモジュール
"""

import pathlib
from md_dict_data import MDDictData, Header

class MarkdownIO:
    """
    マークダウンファイルの入出力と、1層目のヘッダー操作
    Attributes:
        markdown_path (pathlib.Path): そのmarkdownファイルのパス
        markdown (MDDictData): Markdownデータ
    """
    def __init__(self, markdown_path: pathlib.Path):
        self.markdown_path: pathlib.Path = markdown_path
        self.markdown: MDDictData = MDDictData.from_markdown(self._read_markdown())

    def _read_markdown(self):
        with open(self.markdown_path, "r", encoding="utf-8") as f:
            return f.read()
    
    def _write_markdown(self, content):
        with open(self.markdown_path, "w", encoding="utf-8") as f:
            f.write(content)

    def save(self):
        """
        マークダウンファイルを保存
        """
        self._write_markdown(self.markdown.to_markdown())

    def get_body(self, key: str|None):
        """
        ヘッダーをキーで取得する。keyがない場合はNoneを返す
        
        parameters:
            key (str|None): ヘッダーのキー
        returns:
            Header: ヘッダーオブジェクト
        """
        return self.markdown.get(key)
    
    def update_body(self, header: Header):
        """
        ヘッダーを更新する。keyなどはヘッダーオブジェクトから取得

        parameters:
            header (Header): ヘッダーオブジェクト
        """
        self.markdown = self.markdown.update(header)

if __name__ == "__main__":
    def main():
        md_io = MarkdownIO(pathlib.Path("example.md"))
        header = md_io.get_body("計画")
        if header:
            header.lines.append("追加の行")
            md_io.update_body(header)
            md_io.save()
    main()