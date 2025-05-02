# PRD：迷家截图检索交互优化（daisyUI CDN 版）

## 背景

本地 Flask 项目已完成截图检索功能，现需提升用户界面与交互体验，便于通过网页浏览和复制截图进行微博吐槽。

---

## 目标

使用 daisyUI CDN 实现美观、响应式的前端界面，提供：

* 网格化截图浏览
* 滚动懒加载
* 每张截图的「📋复制图片」按钮

---

## 技术栈

| 项目    | 说明                                                   |
| ----- | ---------------------------------------------------- |
| CSS框架 | [daisyUI](https://daisyui.com/) via CDN（基于 Tailwind） |
| JS交互  | 原生 JavaScript（包含 Clipboard API 和懒加载）                 |
| 后端    | Flask 模板渲染，无需安装前端依赖                                  |

---

## 功能需求

### 1. 网格布局（截图浏览）

* 使用 `grid` 实现多列卡片展示（1–3列，随屏宽自适应）
* 每张截图以 `card` 组件呈现，包含图片、字幕、集数、按钮
* 卡片样式使用 daisyUI 的 `card`, `shadow`, `bg-base-100` 等类名

### 2. 滚动懒加载

* 初始加载前 40 张图
* 滚动至底部自动加载更多，直至展示全部匹配结果
* 推荐使用 `IntersectionObserver` 实现懒加载，避免过度占用 DOM

### 3. 图片复制按钮

* 每张截图下提供按钮：📋 复制
* 点击时通过 Clipboard API 将图像以 `image/png` 格式复制到系统剪贴板
* 成功后显示绿色 `toast`：`✅ 已复制`
* 失败后显示红色 `toast`：`❌ 当前浏览器不支持复制图片`

> ⚠️ Firefox 不支持图像复制，仅显示错误提示即可；Chrome、Edge 均支持

---

## 页面结构说明

```html
<head>
  <!-- daisyUI + Tailwind CDN -->
  <link href="https://cdn.jsdelivr.net/npm/daisyui@5" rel="stylesheet" type="text/css" />
  <link href="https://cdn.jsdelivr.net/npm/daisyui@5/themes.css" rel="stylesheet" type="text/css" />
  <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
</head>

<body>
  <!-- 搜索栏 -->
  <form>
    <input class="input input-bordered w-full" ...>
    <button class="btn btn-primary">搜索</button>
  </form>

  <!-- 结果区域 -->
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    <div class="card">
      <img src="...">
      <div class="card-body">
        <p>字幕文本</p>
        <p class="text-xs text-gray-400">S01E04</p>
        <button class="btn btn-sm btn-outline" onclick="copyImage()">📋 复制</button>
      </div>
    </div>
    ...
  </div>
</body>
```

---

## 文件结构建议

```
templates/
└── index.html           ← 页面 UI 改造主文件

static/
├── copy.js              ← 图片复制逻辑（Clipboard API）
├── lazyload.js          ← 滚动懒加载逻辑
└── toast.js             ← toast 显示（也可内联）
```

---

## 非功能性要求

* 无需安装依赖，只引入 CDN
* 所有 JS 控制应具备浏览器兼容性判断
* 图片复制需兼容 Chrome 贴图到微博的操作

---

## 接入规范

| 输入        | Flask 后端模板                                                    |
| --------- | ------------------------------------------------------------- |
| 图路径       | `url_for('serve_image', ep=item.episode, filename=item.file)` |
| 图描述       | `item.text`, `item.episode`                                   |
| 每张图唯一 key | 可用 `episode + filename` 拼接                                    |
