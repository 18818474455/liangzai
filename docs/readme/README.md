# README 视觉资产

本目录保存云享传靓仔 GitHub README 的可编辑源、渲染图与实机录屏。

## 目录

```text
docs/readme/
├── source/
│   ├── design-tokens.json
│   └── render_v0.py
├── rendered/
│   ├── hero-workstation.webp
│   ├── local-first-architecture.webp
│   ├── editable-ai-pipeline.webp
│   ├── multi-model-orchestration.webp
│   ├── open-core-map.webp
│   ├── portrait-proof.webp
│   ├── mask-proof.webp
│   ├── image-tools-proof.webp
│   ├── product-tour-poster.webp
│   └── social-preview.png
└── media/
    ├── download-qr.png
    ├── product-tour-720p.mp4
    ├── product-tour-frame.jpg
    └── wechat-qr.png
```

## 重新渲染

依赖 Python 3 与 Pillow。脚本使用 macOS 系统中的 SF Mono、Hiragino Sans GB 与 STHeiti 字体。

```bash
python3 docs/readme/source/render_v0.py
```

产品界面只能来自 `assets/shot-*.png` 的真实截图。脚本负责版式、说明图形与导出，不重画或生成软件 UI。

## 视频

原始录屏不进入仓库。仓内版本为 H.264、1280×720、24 fps、4,031,424 bytes，并带 `faststart`，通过 README 海报链接访问。GitHub README 不可靠支持仓内 MP4 内嵌播放器，因此不使用 `<video>` 标签。

## 联系二维码

- `wechat-qr.png`：从用户提供的微信名片中保留静区裁切，避免在 README 中展示无关留白。
- `download-qr.png`：指向 `https://github.com/18818474455/liangzai`。当前官网 `download.html` 的 Mac 链接仍是旧版，因此先让扫码用户进入包含当前正式安装包链接的产品总览页。

## 发布门禁

- 不展示尚未开放的「AI工具箱」「选片交付」。
- 不写未公开复现方法的性能数字。
- 不公开模型结构、权重、风格配方、密钥或闭源引擎实现。
- 发布前检查截图中的项目名、账号、手机号与人物素材授权。
- `social-preview.png` 需在 GitHub 仓库 Settings 中手动设置为 Social preview。
