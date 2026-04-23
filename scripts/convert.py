#!/usr/bin/env python3
"""Markdown 转微信公众号 HTML 的命令行入口"""

import sys
import argparse
from pathlib import Path

# 将项目根目录加入路径，以便导入 skills 模块
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from skills.md2wechat import convert_file


def main():
    parser = argparse.ArgumentParser(
        description="将 Markdown 文件转换为微信公众号可用的 HTML"
    )
    parser.add_argument("md_path", help="Markdown 文件路径")
    parser.add_argument(
        "-o", "--output-dir",
        default=None,
        help="输出目录（默认: docs/articles/{文章名}）"
    )
    parser.add_argument(
        "-t", "--title",
        default=None,
        help="文章标题（默认从 Markdown 一级标题提取）"
    )
    parser.add_argument(
        "-s", "--style",
        default="default",
        help="Pygments 代码高亮风格（默认: default）"
    )

    args = parser.parse_args()

    md_path = Path(args.md_path)
    if not md_path.exists():
        print(f"错误：文件不存在 {md_path}")
        sys.exit(1)

    # 默认输出目录（直接放在 docs/ 下，每篇文章一个独立目录）
    if args.output_dir is None:
        article_name = md_path.stem
        output_dir = PROJECT_ROOT / "docs" / article_name
    else:
        output_dir = Path(args.output_dir)

    print(f"转换: {md_path}")
    print(f"输出: {output_dir}")

    result_path = convert_file(
        md_path=str(md_path),
        output_dir=str(output_dir),
        title=args.title,
        code_style=args.style,
    )

    print(f"成功生成: {result_path}")


if __name__ == "__main__":
    main()
