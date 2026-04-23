"""Markdown 解析器：将文本分割为普通文本和代码块片段"""

import re
import markdown

# 匹配 ```lang\ncode\n``` 格式的代码块
CODE_BLOCK_RE = re.compile(
    r'^```(\w+)?\n(.*?)```$',
    re.MULTILINE | re.DOTALL,
)

# 修复列表前缺少空行的问题（标准 Markdown 要求列表前有空行）
LIST_FIX_RE = re.compile(r'^(.*[^\n])\n([ \t]*[-*+][ \t]+)', re.MULTILINE)


def _fix_list_spacing(text: str) -> str:
    """在列表标记前添加空行，确保 markdown 解析器正确识别列表"""
    return LIST_FIX_RE.sub(r'\1\n\n\2', text)


def split_markdown(text: str):
    """
    将 Markdown 文本分割为片段列表。

    每个片段是元组: ("text", raw_text) 或 ("code", {"lang": ..., "code": ...})

    Args:
        text: 原始 Markdown 文本

    Returns:
        list[tuple]
    """
    # 预处理：修复列表前空行
    text = _fix_list_spacing(text)

    parts = []
    last_end = 0

    for match in CODE_BLOCK_RE.finditer(text):
        # 代码块之前的普通文本
        if match.start() > last_end:
            parts.append(("text", text[last_end:match.start()]))

        language = match.group(1) or "text"
        code = match.group(2)

        # 去掉代码末尾多余的换行，保持整洁
        code = code.rstrip("\n")

        parts.append(("code", {"lang": language, "code": code}))
        last_end = match.end()

    # 最后一个代码块之后的普通文本
    if last_end < len(text):
        parts.append(("text", text[last_end:]))

    return parts


def markdown_to_html(text: str) -> str:
    """将 Markdown 文本转为 HTML（不包含代码块处理）"""
    return markdown.markdown(
        text,
        extensions=[
            "tables",
            "fenced_code",
        ],
    )
