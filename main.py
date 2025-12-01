from jinja2 import Environment, FileSystemLoader
from datetime import date
import os


def render_template(output_path: str = 'output.md') -> None:
	env = Environment(
		loader=FileSystemLoader('templates'),
		autoescape=False,
	)
	template = env.get_template('template.md.j2')

	context = {
		'title': 'サンプルドキュメント',
		'author': 'あなたの名前',
		'date': date.today().isoformat(),
		'summary': 'このドキュメントはJinja2テンプレートの例です。',
		'tags': ['example', 'jinja2', 'markdown'],
		'overview': 'このセクションでは概要を説明します。',
		'content': 'ここに本文を書きます。Markdown記法が使えます。',
		'sections': [
			{'title': '背景', 'body': '背景の説明を書く'},
			{'title': '実装', 'body': '実装の詳細を書く'},
		],
	}

	rendered = template.render(**context)

	os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
	with open(output_path, 'w', encoding='utf-8') as f:
		f.write(rendered)

	print(f'Wrote {output_path}')


if __name__ == '__main__':
	render_template()