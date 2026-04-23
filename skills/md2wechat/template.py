"""微信文章 HTML 模板引擎"""

from jinja2 import Template

WECHAT_TEMPLATE = Template("""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>{{ title }}</title>
    <style>
        /* 基础重置 */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
                         "Helvetica Neue", Arial, "Noto Sans", sans-serif,
                         "Apple Color Emoji", "Segoe UI Emoji";
            background-color: #f5f5f5;
            color: #333;
            line-height: 1.8;
            -webkit-font-smoothing: antialiased;
        }

        /* 内容容器：手机宽度适配 */
        .article-container {
            max-width: 375px;
            margin: 0 auto;
            padding: 20px 16px;
            background-color: #fff;
            min-height: 100vh;
        }

        /* 文章标题 */
        .article-title {
            font-size: 20px;
            font-weight: bold;
            color: #1a1a1a;
            line-height: 1.4;
            margin-bottom: 16px;
            text-align: center;
        }

        /* 正文段落：18px 约 20 字/行 */
        .article-body p {
            font-size: 18px;
            line-height: 1.8;
            margin-bottom: 16px;
            text-align: justify;
            word-break: break-word;
        }

        /* 各级标题 */
        .article-body h1 {
            font-size: 19px;
            font-weight: bold;
            color: #1a1a1a;
            margin: 24px 0 12px 0;
            padding-bottom: 8px;
            border-bottom: 1px solid #eee;
        }

        .article-body h2 {
            font-size: 18px;
            font-weight: bold;
            color: #222;
            margin: 20px 0 10px 0;
        }

        .article-body h3 {
            font-size: 17px;
            font-weight: bold;
            color: #333;
            margin: 16px 0 8px 0;
        }

        /* 引用块 */
        .article-body blockquote {
            margin: 16px 0;
            padding: 12px 16px;
            background-color: #f8f9fa;
            border-left: 4px solid #d0d7de;
            color: #57606a;
            font-size: 17px;
            line-height: 1.7;
        }

        .article-body blockquote p {
            margin-bottom: 0;
            font-size: 17px;
        }

        /* 代码图片 */
        .code-image {
            display: block;
            max-width: 100%;
            height: auto;
            margin: 12px 0;
            border-radius: 6px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }

        /* 表格容器：横向滚动 */
        .article-body .table-wrapper {
            overflow-x: auto;
            margin: 16px 0;
            -webkit-overflow-scrolling: touch;
        }

        .article-body table {
            width: 100%;
            border-collapse: collapse;
            font-size: 15px;
            min-width: 300px;
        }

        .article-body th,
        .article-body td {
            padding: 8px 10px;
            border: 1px solid #d0d7de;
            text-align: left;
        }

        .article-body th {
            background-color: #f6f8fa;
            font-weight: 600;
        }

        .article-body tr:nth-child(even) {
            background-color: #fafafa;
        }

        /* 列表 */
        .article-body ul,
        .article-body ol {
            margin: 12px 0 12px 24px;
            font-size: 18px;
            line-height: 1.8;
        }

        .article-body li {
            margin-bottom: 6px;
        }

        /* 链接 */
        .article-body a {
            color: #0969da;
            text-decoration: none;
        }

        .article-body a:hover {
            text-decoration: underline;
        }

        /* 分隔线 */
        .article-body hr {
            border: none;
            border-top: 1px solid #e1e4e8;
            margin: 20px 0;
        }

        /* 强调 */
        .article-body strong {
            font-weight: bold;
            color: #1a1a1a;
        }

        .article-body em {
            font-style: italic;
        }

        /* 行内代码（如果存在） */
        .article-body code {
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
            font-size: 15px;
            background-color: #f6f8fa;
            padding: 2px 5px;
            border-radius: 3px;
            color: #cf222e;
        }

        /* 脚注/小字 */
        .article-body sub,
        .article-body sup {
            font-size: 13px;
        }
    </style>
</head>
<body>
    <div class="article-container">
        {% if title %}
        <div class="article-title">{{ title }}</div>
        {% endif %}
        <div class="article-body">
            {{ body_html }}
        </div>
    </div>
</body>
</html>
""")


def render_html(title: str, body_html: str) -> str:
    """
    渲染完整的微信文章 HTML 页面。

    Args:
        title: 文章标题
        body_html: 文章正文 HTML（已由 markdown 解析）

    Returns:
        完整的 HTML 字符串
    """
    return WECHAT_TEMPLATE.render(title=title, body_html=body_html)
