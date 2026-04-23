# md2wechat Skill

将 Markdown 文件转换为适合微信公众号/手机阅读的 HTML 页面，核心特性：

- **代码转图片**：Markdown 中的代码块通过 Pygments 渲染为语法高亮 PNG 图片，解决微信公众号代码显示差的问题
- **手机排版适配**：内容宽度 375px，正文字号 18px，行高 1.8，目标约 20 字/行
- **模块化设计**：解析器、图片渲染器、模板引擎独立拆分

## 使用与协作流程

```python
from skills.md2wechat import convert_file

convert_file(
    md_path="/path/to/article.md",
    output_dir="docs/article-name",
    title="文章标题",
)
```

### Git 协作分工

- **AI 负责**：`git add` 和 `git commit`（代码变更、生成产物）
- **用户负责**：`git push`（推送到 Gitee 仓库并触发 Pages 部署）

## 模块说明

| 模块 | 职责 |
|:---|:---|
| `parser.py` | Markdown 分割为「普通文本」和「代码块」片段 |
| `code_renderer.py` | 使用 Pygments ImageFormatter 将代码渲染为 PNG |
| `template.py` | Jinja2 微信文章 HTML 模板与 CSS |
| `converter.py` | 主转换流程编排 |

## 依赖

- markdown
- pygments
- Pillow
- jinja2
