"""代码高亮图片渲染器"""

import io
from PIL import Image
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import ImageFormatter

# 代码图片最小宽度（像素），与微信容器宽度对齐
MIN_CODE_IMAGE_WIDTH = 340


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
        font_name="Menlo",
        font_size=14,
        line_numbers=False,
        image_pad=12,
        line_pad=4,
        bg="#f6f8fa",
        style=style,
    )

    image_data = highlight(code, lexer, formatter)
    return _ensure_min_width(image_data)


def _ensure_min_width(image_data: bytes, min_width: int = MIN_CODE_IMAGE_WIDTH) -> bytes:
    """
    若代码图片宽度小于 min_width，则在两侧填充背景色使其达到目标宽度，
    避免短代码在文章中显得过窄。
    """
    img = Image.open(io.BytesIO(image_data))
    if img.width >= min_width:
        return image_data

    new_img = Image.new("RGB", (min_width, img.height), "#f6f8fa")
    x_offset = (min_width - img.width) // 2
    new_img.paste(img, (x_offset, 0))

    buf = io.BytesIO()
    new_img.save(buf, format="PNG")
    return buf.getvalue()
