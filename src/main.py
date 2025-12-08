#!/usr/bin/env python3
import uuid
import argparse
import pathlib

def init_asis(path, asis_item: str=""):
    base = pathlib.Path(path)

    unique_id = uuid.uuid4()
    # 1. path/asisの下にuuidディレクトリを作成し、その下に0.mdを作成する
    target_dir = base / "asis" / str(unique_id)
    target_dir.mkdir(parents=True, exist_ok=True)
    target_file = target_dir / "0.md"
    with target_file.open("w", encoding="utf-8") as f:
        f.write(f"# Unique ID: {unique_id}\n")
        f.write(f"# Init Asis: {asis_item}\n")
    
    # 2. pathの中のtaksk.mdにuuidを書き込む。存在しない場合は新規作成する。
    ## その際の形式は - [*](asis/uuid/0.md)として書き込む。
    tasks_file = base / "tasks.md"
    with tasks_file.open("a", encoding="utf-8") as f:
        f.write(f"- [{asis_item}](asis/{unique_id}/0.md)\n")

def main(args) -> None:
    path = pathlib.Path(args.path)
    # path/plan.mdを一行ずつ読み込みinit_asisを実行する
    plan_file = path / "plan.md"
    if not plan_file.exists():
        print(f"Error: {plan_file} does not exist.")
        return

    asis_plan_list = []
    with plan_file.open("r", encoding="utf-8") as f:
        for line in f:
            asis_plan_list.append(line.strip())
    for asis_data in asis_plan_list:
        init_asis(path, asis_data)

def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", type=str, required=True)
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    main(args)