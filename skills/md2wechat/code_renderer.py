"""代码高亮图片渲染器"""

from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import ImageFormatter


def render_code_to_image(code: str, language: str = "text", style: str = "default") -> bytes:
    """
    将代码字符串渲染为语法高亮 PNG 图片。

    Args:
        code: 代码文本
        language: 代码语言，如 cpp、python、java
        style: Pygments 配色风格，默认 "default"

    Returns:
        PNG 图片的二进制数据
    """
    # 去掉末尾多余的换行，避免图片底部空白
    code = code.rstrip("\n")
    if not code:
        code = " "

    # 获取词法分析器
    try:
        lexer = get_lexer_by_name(language)
    except Exception:
        try:
            lexer = guess_lexer(code)
        except Exception:
            from pygments.lexers.special import TextLexer
            lexer = TextLexer()

    formatter = ImageFormatter(
        image_format="PNG",
        font_name="Noto Sans Mono CJK SC",
        font_size=14,
        line_numbers=False,
        image_pad=12,
        line_pad=4,
        bg="#f6f8fa",
        style=style,
    )

    return highlight(code, lexer, formatter)
