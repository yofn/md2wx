"""主转换器：编排 Markdown → 微信 HTML 的完整流程"""

import os
import re
from pathlib import Path

from .parser import split_markdown, markdown_to_html, process_latex
from .code_renderer import render_code_to_image
from .template import render_html


def _wrap_tables(html: str) -> str:
    """给 <table> 包裹横向滚动容器"""
    html = html.replace("<table>", '<div class="table-wrapper"><table>')
    html = html.replace("</table>", "</table></div>")
    return html


def _extract_title(md_text: str) -> tuple[str, str]:
    """
    从 Markdown 文本中提取一级标题，并返回(标题, 去掉标题后的正文)。
    """
    m = re.search(r'^#\s+(.+)$', md_text, re.MULTILINE)
    if not m:
        return "Untitled", md_text

    title = m.group(1).strip()
    # 移除第一个一级标题行（包括其前面的空行和后面的空行）
    start = m.start()
    end = m.end()
    # 也去掉后面紧跟的空行
    while end < len(md_text) and md_text[end] == "\n":
        end += 1

    cleaned = md_text[:start] + md_text[end:]
    return title, cleaned


def convert_file(
    md_path: str,
    output_dir: str,
    title: str = None,
    code_style: str = "default",
) -> str:
    """
    将 Markdown 文件转换为微信文章 HTML。

    Args:
        md_path: Markdown 文件路径
        output_dir: 输出目录（HTML 和图片将放在这里）
        title: 文章标题，默认从 Markdown 一级标题提取
        code_style: Pygments 代码高亮风格

    Returns:
        生成的 HTML 文件路径
    """
    md_path = Path(md_path)
    output_dir = Path(output_dir)
    images_dir = output_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    # 读取 Markdown
    md_text = md_path.read_text(encoding="utf-8")

    # 提取标题并移除正文中的重复标题
    extracted_title, md_text = _extract_title(md_text)
    if title is None:
        title = extracted_title

    # 分割为片段
    parts = split_markdown(md_text)

    # 处理每个片段
    body_parts = []
    code_index = 0

    for part_type, content in parts:
        if part_type == "text":
            # 普通文本：先处理 LaTeX 公式，再转 HTML
            content = process_latex(content)
            html = markdown_to_html(content)
            body_parts.append(html)
        elif part_type == "code":
            # 代码块渲染为图片
            lang = content["lang"]
            code = content["code"]
            image_data = render_code_to_image(code, language=lang, style=code_style)

            image_filename = f"code_{code_index}.png"
            image_path = images_dir / image_filename
            image_path.write_bytes(image_data)

            # 计算相对路径（HTML 在 output_dir，图片在 output_dir/images/）
            img_src = f"images/{image_filename}"
            body_parts.append(f'<img class="code-image" src="{img_src}" alt="code">')
            code_index += 1

    # 拼接正文 HTML
    body_html = "\n".join(body_parts)

    # 给表格加滚动容器
    body_html = _wrap_tables(body_html)

    # 推荐练习标题自动备注来源
    body_html = re.sub(
        r'(<h[1-6][^>]*>)推荐练习(</h[1-6]>)',
        r'\1推荐练习（洛谷）\2',
        body_html,
    )

    # 渲染完整页面
    full_html = render_html(title=title, body_html=body_html)

    # 写入文件
    output_path = output_dir / "index.html"
    output_path.write_text(full_html, encoding="utf-8")

    return str(output_path)
