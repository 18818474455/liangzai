# 云享传靓仔 · 介绍页品牌

| 资产 | 路径 |
|------|------|
| 字标（白） | `docs/brand/logo-white.png` |
| 吉祥物 | `docs/brand/mascot.png` |
| PC 产品图标 | `docs/brand/pc-icon.png` |
| 工作台截图 | `docs/hero-desktop.png` |
| 当前正式工作台实拍 | `assets/shot-color.png` |
| 项目首页实拍 | `assets/shot-dashboard.png` |
| 人像 / 蒙版 / 换天 / 证件照实拍 | `assets/shot-*.png` |
| 能力图 | `docs/features/`、`assets/feature-tour.gif` |

色板取自官网 `product-pc.html`：

- 产品 UI：底 `#050607` / `#0D1017`，字 `#DBE2E6` / `#FFFFFF`
- README V2 画布：白 `#FFFFFF`、墨黑 `#1D1D1F`、浅灰 `#F5F5F7`
- 次字：`#86868B`
- 分隔线：`#D2D2D7`
- 品牌强调：薄荷绿 `#3DD6A5`
- 辅助强调：天青 `#5DDCF6`，只用于确有第二语义的技术路径

## README V2 设计系统

- **方向**：高端产品发布 / Editorial Minimalist。
- **视觉锚点**：Apple 产品发布页；真实软件窗口是“产品实物”。
- **字体**：渲染图使用 SF Pro + Hiragino Sans GB / STHeiti；README 正文服从 GitHub。
- **间距**：4 / 8 / 16 / 24 / 40 / 64 / 96 / 160。
- **圆角**：12 / 18 / 22；按控件、面板、主视觉分级。
- **阴影**：极弱，只用于把真实软件窗口从白底上抬起。
- **动效**：低强度，最多保留一个有解释作用的功能巡礼 GIF。
- **版式**：一节一个观点，大标题 → 一句解释 → 一张主图；长细节进 `<details>`。

## 禁止项

- 不用生成式 AI 重画产品 UI。
- 不用紫蓝渐变、霓虹电路、机器人、emoji 作为技术感替代品。
- 不做八张等规格截图卡片墙。
- 不编造 benchmark、客户数量、使用品牌或安全认证。
- 不把 `disabled: true` 的 AI 工具箱 / 选片交付当成正式能力。
- 不暴露模型、配方、密钥和闭源引擎实现细节。

## README V2 资产

- 源码：`docs/readme/source/`
- 渲染图：`docs/readme/rendered/`
- Hero：`hero-workstation.webp`
- 技术图：`local-first-architecture.webp`、`editable-ai-pipeline.webp`、`multi-model-orchestration.webp`、`open-core-map.webp`
- 实机证据：`portrait-proof.webp`、`mask-proof.webp`、`image-tools-proof.webp`
- 完整录屏：`docs/readme/media/product-tour-720p.mp4`，README 通过 `product-tour-poster.webp` 链接
- 社交封面：`social-preview.png`（需在 GitHub Settings 手动设置）
- 需求与技术方案：`docs/README-专业化重设计-需求与技术方案.md`
