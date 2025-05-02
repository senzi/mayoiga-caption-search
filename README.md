# Mayoiga Screenshot Search Tool

一个基于 Flask + daisyUI 的本地截图检索工具，用于模糊搜索动画《迷家》的台词并展示对应字幕截图，适合用于微博吐槽、关键词回顾等场景。

---

## 🧩 功能特性

- ✅ 模糊关键词搜索字幕（支持多个词同时匹配）
- ✅ 网格化截图展示，响应式布局
- ✅ 每张图附带「📋复制」按钮，点击即可复制图片用于微博粘贴
- ✅ 支持滚动懒加载，不卡浏览器
- ✅ 暗色 `dracula` 主题，适配夜间模式

---

## 📦 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/yourname/mayoiga-caption-search.git
cd mayoiga-caption-search
````

### 📥 下载截图数据包

> 👉 [点击下载 screenshots.zip（5400+字幕截图）](https://github.com/senzi/mayoiga-caption-search/releases/download/V1.0/screenshots.zip)
>
> 解压后将文件放置于项目根目录，然后运行：`python manage_archive.py`
> 或者自己手动解压

---

### 3. 解压截图

执行脚本自动解压截图：

```bash
python manage_archive.py
```

会解压到 `static/screenshots/` 目录下。

---

### 4. 安装依赖并运行

只需要 Flask 和 tqdm（用于截图生成）：

```bash
pip install flask tqdm
python app.py
```

打开浏览器访问：`http://127.0.0.1:5000`

---

## 🔍 搜索规则

* 输入关键词即可搜索字幕内容
* 多个关键词用空格或逗号隔开：**表示必须同时包含**
* 匹配成功将展示最多 50 张截图，支持滚动加载

---

## ✨ 示例截图

| 搜索       | 结果              |
| -------- | --------------- |
| `光宗`     | 展示所有出现“光宗”的台词截图 |
| `光宗 女司机` | 同时包含两个关键词的截图    |
| `不要下车`   | 截图一看就知道为什么不能下车  |

---

## 📁 项目结构说明

```
├── static/
│   └── screenshots/     ← 截图存放目录（由 screenshots.zip 解压而来）
├── templates/
│   └── index.html       ← 前端界面模板（使用 daisyUI CDN）
├── app.py               ← Flask 启动文件
├── manage_archive.py    ← 压缩/解压截图
└── screenshots.zip      ← 单独分发，不纳入版本控制
```

---

## 🙋 FAQ

**Q: 我复制按钮点击没反应？**
A: 请使用最新版 Chrome 浏览器，并确保是 `localhost` 或 `127.0.0.1` 访问，Clipboard API 在 HTTP 环境下会限制图像复制。

---

## 📜 License

本项目仅用于个人学习与非商业用途，禁止任何形式的传播和在线托管。
