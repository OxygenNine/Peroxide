# 简介

<img src="https://oxygennine.github.io/Peroxide/Images/peroxide-logo-titled.svg" alt="过氧化物基础版式logo" style="width: 100%; max-width: 400px; margin: 20px auto; background-color: #fff; padding: 10px; border-radius: 25px; display: block;">

<div style="text-align: center;">

![License CC4](https://img.shields.io/badge/license-CC4-yellow) ![Version 1.0.1](https://img.shields.io/badge/version-1.0.1_release-green) ![Creator OxygenNine](https://img.shields.io/badge/creator-OxygenNine-blue) ![Pure CSS](https://img.shields.io/badge/pure-CSS-purple) ![Wikidot Theme](https://img.shields.io/badge/wikidot-theme-red)

</div>



欢迎使用过氧化物（Peroxide）基础版式。这是一个为Wikidot网站设计的基础CSS版式。

此仓库同样用于开发过氧化物的衍生版式。未来，基于一氧化物版式的衍生版式都将用过氧化物重置。

# 使用

可以通过以下方式引入过氧化物基础版式：

1. 登录Wikidot网站，进入您的网站管理界面。
2. 点击“外观与表现”选项卡，然后设置“外部样式”。
3. 将以下地址复制粘贴到文本框：

```
https://oxygennine.github.io/Peroxide/peroxide.css
```

在任何一个页面上，也可以通过插入以下代码引入此版式：

```
[[include :scp-wiki-cn:theme:peroxide]]
```

关于版式特性，请参考它在SCP-CN Wiki上的发布页：https://scp-wiki-cn.wikidot.com/theme:peroxide

# 源码结构与构建

## 源码模块和合并产物的关系

仓库的 `CSS/` 目录下是 5 个**分模块、带注释**的源文件，它们按顺序拼接后成为完整的版式：

| 源文件 | 职责 |
| --- | --- |
| `CSS/Variables.css` | 定义全局变量：调色盘、字体族、布局尺寸、动画时长等 |
| `CSS/Base.css` | 框架骨架：页眉、顶栏、侧栏、主内容、页脚、弹窗、滚动条等 |
| `CSS/Elements.css` | 内容组件：SCP 图像块、评分栏、论坛、目录、按钮、引用、MathJax 等 |
| `CSS/Capabilities.css` | 兼容“一层氧化物”（Monoxide / Bedrock）版式，做变量映射与组件适配 |
| `CSS/Localization.css` | 用伪元素 + CSS 变量为 Wikidot 界面强行注入多语言文本 |

两种合并产物：

- **`peroxide.css`**（开发版，由 `build.bat` 生成）：仅按顺序拼接 5 个文件并保留注释，便于阅读与调试，体积约 220 KB。
- **`peroxide.min.css`**（生产版，由 `build_min.py` 生成）：在拼接的基础上做压缩（去注释、折叠空白、移除无意义空格），体积更小，用于正式发布。

> 拼接顺序固定为 `Variables → Base → Elements → Capabilities → Localization`，因为后续文件依赖前面文件定义的变量与基础结构。

## 如何构建 peroxide.min.css

`build_min.py` 是纯 Python 标准库脚本，无需安装任何第三方依赖。

```bash
# 在项目根目录执行，默认输出 peroxide.min.css
python build_min.py

# 也可指定输出路径
python build_min.py dist/theme.min.css
```

Windows 用户可直接双击 `build-min.bat`（脚本会自动探测 `python` / `py` 解释器）。

压缩脚本会**刻意保留** `calc()`、`color-mix()`、字符串、`url()` 等片段内部的空格——这些空格是 CSS 语法的强制要求（例如 `calc(100% - 2rem)` 的减号两侧、`color-mix(in srgb, …)` 的 `in srgb`），删掉会导致样式失效。

# 浏览器支持

版式采用**渐进增强**：纯文字内容在最古老的浏览器里依然可读；但许多视觉与交互特性依赖较新的 CSS。

- **不影响正常使用的渐进增强**（缺失时仅配色/细节不同）：
  - `:has()` 选择器（约 77 处，用于上下文状态微调）
  - `color-mix()`（约 18 处，用于从主题色自动派生明暗色阶）
- **重要功能严重依赖**（缺失会导致布局错乱或图标不可见，但文字仍可读）：
  - **CSS `mask`**（约 20 处，图标用 mask 着色，而非内联图片）
  - **`:is()`**（约 87 处）与 **`:where()`**（约 42 处，用于精简大量选择器）
  - **`display: grid` / `grid-template`**（约 40 处，页眉、侧栏、内容区等复杂栅格布局）
  - **`backdrop-filter`**（约 17 处，毛玻璃效果）

**建议使用以下或更新版本的浏览器**：Chrome / Edge 105+、Firefox 121+、Safari 16.4+。这些版本同时稳定支持 `:has()`、`color-mix()` 与 `mask`。使用不支持 `:is()/:where()` 或 Grid 的老旧浏览器时，可能出现布局错位、图标空白等问题，但不影响页面文字内容本身的阅读。

# 本地化（Localization.css）

## 工作原理

Wikidot 自身**不为大量界面文字提供翻译通道**——例如操作区的“关闭”按钮、文件列表里的文件类型标签等，始终以英文（或固定字符串）呈现。

Localization.css 的做法是：

1. 把所有需要翻译的界面文本定义成一组 CSS 自定义属性（变量）`--LOC-*`，并为不同语言设置不同取值：
   - 默认（`:root`）为英文；
   - `:root:lang(cn), :root:lang(zh), :root:lang(zh-cn)` 覆盖为中文；
   - `:root:lang(ja)` / `:root[lang="ja-corrections"]` 覆盖为日文。
2. 通过对 Wikidot 生成的对应 DOM 节点挂伪元素，用 `content: var(--LOC-xxx)` 把译文**强行附加**到界面上（例如 `#action-area …::after { content: var(--LOC-close); }`，在关闭按钮后追加“关闭”字样）。

全源码中共有约 54 处 `content: var(--LOC-*)`，覆盖了操作区、文件管理器、附件列表等 Wikidot 未开放翻译的界面。

## 如何提交新的翻译

1. 打开 `CSS/Localization.css`，所有翻译都集中在顶部的 `--LOC-*` 变量定义处。
2. **修正或补充已有语言**：在对应的 `:lang()` 区块里修改 `--LOC-*` 的值即可（只改值的引号内容，不要改动变量名，也不要改动引用它们的选择器）。
3. **新增一种语言**：在文件末尾新增一个 `:root:lang(xx) { … }` 区块，并把所有 `--LOC-*` 变量写满对应语言的字符串。
4. 提交：通过 Pull Request 推送到本仓库，或直接联系维护者 OxygenNine。

# 核心变量（Variables.css）

`Variables.css` 提供了全站统一的“设计令牌”（design tokens）。以下是最常被衍生版式覆盖、也最值得了解的一组：

- **`--p-theme-color` / `--p-theme-color-light` / `--p-theme-color-dark`**：主题强调色，用于链接、标题装饰、按钮、聚焦态等，决定整站视觉基调。衍生版式通常只改这三个值即可换肤。
- **`--p-gray-0` … `--p-gray-7`**：灰度层次调色盘（`0` 最白 → `7` 纯黑），用于背景、正文、次要文字、边框的分级。
- **`--p-font-sans-serif` / `--p-font-serif` / `--p-font-monospace`**：三大字体族（黑体 / 宋体 / 等宽），统一全站中英文排版。
- **`--p-main-content-width` / `--p-sidebar-width` / `--p-header-height`**：布局尺寸，控制主内容区最大宽度、侧栏宽度与页眉高度——衍生版式与布局覆盖（见 `CSS/Settings/`）常覆写这些变量。
- **`--p-border-radius-*` / `--p-animation-duration-*`**：圆角尺度与过渡动画时长，保证全站动效与外形一致。
- 此外还有大量 **`--p-*-w10…w90` / `-b10…b90`** 变量，它们是通过 `color-mix()` 从主题色自动派生的由浅到深色阶，专供 `:hover` / `:active` 等状态使用，无需手动维护。