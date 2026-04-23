# md2wx

将 Markdown 文件转换为适合**微信公众号**发布的 HTML 页面。

## 特性

- **代码转图片**：Markdown 中的代码块通过 Pygments 渲染为语法高亮 PNG 图片，完美解决微信公众号代码显示差的问题
- **手机排版适配**：内容宽度 375px，正文字号 18px / 行高 1.8，目标约 20 字/行
- **模块化设计**：核心能力拆分为 `skills/md2wechat/` 模块，可复用、可扩展

## 安装

```bash
# 创建虚拟环境并安装依赖
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

依赖：markdown、pygments、Pillow、jinja2

## Git 协作分工

- **AI 负责**：`git add` 和 `git commit`（代码变更、生成产物）
- **用户负责**：`git push`（推送到 Gitee 仓库并触发 Pages 部署）

## 使用方法

### 单文件转换

```bash
python scripts/convert.py ~/csp-wiki/docs/search/dfs-stack.md
```

转换结果输出到 `docs/dfs-stack/`，包含：
- `index.html` — 文章页面
- `images/code_*.png` — 代码高亮图片

### 批量转换

```bash
# 转换某个目录下的所有 md 文件
for f in ~/csp-wiki/docs/search/*.md; do
    python scripts/convert.py "$f"
done
```

### 自定义参数

```bash
python scripts/convert.py article.md \
    -o docs/articles/custom-name \
    -t "自定义标题" \
    -s monokai
```

参数说明：
- `-o, --output-dir`：输出目录（默认 `docs/{文件名}`）
- `-t, --title`：文章标题（默认从 Markdown 一级标题提取）
- `-s, --style`：Pygments 代码高亮风格（如 `default`、`monokai`、`github-dark`）

## 项目结构

```
md2wx/
├── skills/                          # 模块化技能目录
│   └── md2wechat/
│       ├── SKILL.md                 # 技能说明文档
│       ├── parser.py                # Markdown 解析器
│       ├── code_renderer.py         # 代码高亮图片渲染器
│       ├── template.py              # 微信 HTML 模板引擎
│       └── converter.py             # 主转换器
├── scripts/
│   └── convert.py                   # 命令行入口
├── docs/                            # Gitee Pages 静态站点源目录
│   ├── index.html                   # 站点入口
│   ├── dfs-stack/
│           ├── index.html
│           └── images/
└── requirements.txt
```

## Gitee Pages 配置

1. 将代码推送至 Gitee 仓库
2. 进入 Gitee 仓库页面 → **服务 → Gitee Pages**
3. 部署来源选择 **`/docs` 目录**
4. 点击「启动」或「更新」
5. 访问地址：`https://{你的用户名}.gitee.io/md2wx/`

> 注意：Gitee Pages 对免费用户可能需要实名认证后才能开启。

## 在微信公众号中使用

1. 打开生成的 HTML 页面（本地或 Gitee Pages）
2. 复制页面内容
3. 粘贴到微信公众号编辑器中
4. 微调后即可发布

## 代码高亮风格预览

Pygments 内置风格可通过以下命令查看：

```bash
python -c "from pygments.styles import get_all_styles; print(list(get_all_styles()))"
```

常用推荐：`default`（明亮）、`monokai`（暗黑）、`friendly`、`manni`
