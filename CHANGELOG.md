# 更新记录

本文件记录公开桌面版本和总览仓的重要变化。桌面应用为商业软件；这里的版本记录不改变仓库的开源边界。

## Unreleased

- 增加英文 README、贡献指南、社区行为准则和公开路线图。
- 增加 Bug、功能建议与 Pull Request 模板。
- 增加文档内部链接自动检查。
- 开放 GitHub Discussions，统一问题、建议和工作流交流入口。

## 0.1.19 — 2026-08-17

### 正式交付

- macOS Apple Silicon：build 27，Developer ID 签名并完成 Apple 公证。
- Windows x64：build 26；尚未进行 Authenticode 签名，首次安装可能出现 SmartScreen 提示。

### 下载与校验

| 平台 | 下载 | SHA-256 |
|:---|:---|:---|
| macOS · Apple Silicon | [DMG](https://oss.ybpbyxc.com/uploads/2026-08-17/chroma-studio-0.1.19-build27-arm64.dmg) | `4f1a24217363e2d861aa13ebe820d7d03850ce58dd94307e47bd39a4b7f09844` |
| Windows · x64 | [EXE](https://oss.ybpbyxc.com/uploads/2026-08-15/chroma-studio-0.1.19-build26-x64.exe) | `8bd82700864ff67baf5cbd5a34db8a903bafa538ba5ba382f870c5e5b9cdb84e` |

### 已知边界

- Mac Intel x64 不是当前公证 GA 目标。
- Windows 安装包尚无 Authenticode 证书。
- 产品界面中的「AI工具箱」「选片交付」是规划入口，不作为当前已交付能力。
