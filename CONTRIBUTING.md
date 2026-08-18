# 参与云享传靓仔

感谢你愿意把真实问题、工作流经验或代码贡献回来。`liangzai` 是产品总览与开源导航仓；正式桌面引擎、模型和风格配方不在本仓库中。

## 从哪里开始

- 产品使用问题、经验交流：优先使用 [Discussions](https://github.com/18818474455/liangzai/discussions)。
- 可复现的软件问题：使用 [Bug 模板](https://github.com/18818474455/liangzai/issues/new?template=bug_report.yml)。
- 新工作流或能力建议：使用 [功能建议模板](https://github.com/18818474455/liangzai/issues/new?template=feature_request.yml)。
- 文档、技术图和链接修正：可以直接提交 Pull Request。
- `.cube` LUT 解析、插值或 CLI 改进：请到 [`liangzai-cube-kit`](https://github.com/18818474455/liangzai-cube-kit)。
- 插件类型与 Hello 示例：请到 [`liangzai-plugin-sdk`](https://github.com/18818474455/liangzai-plugin-sdk)。

安全漏洞、授权绕过、隐私泄露或包含用户照片的问题请按 [SECURITY.md](./SECURITY.md) 私下报告，不要创建公开 Issue。

## 提交高质量 Issue

请提供足够的复现信息，同时删除私人内容：

1. 云享传靓仔版本和 build 编号；
2. 操作系统、芯片架构与显卡信息；
3. 预期结果、实际结果和最短复现步骤；
4. 可公开的截图或日志；
5. 是否稳定复现，以及是否有临时绕过方法。

不要上传客户原片、手机号、账号、License 文件、访问令牌或未经授权的人像。

## Pull Request

1. 从 `main` 创建小而单一的分支；
2. 修改后运行 `python3 scripts/check_docs.py`；
3. 对视觉变化附上前后截图；
4. 说明修改原因、验证方式和影响范围；
5. 确认你有权按照本仓库许可证提交相关内容。

提交信息建议使用动词开头，例如 `Fix broken Windows download link`。维护者可能要求拆分过大的 PR。

## 开放边界

欢迎贡献：文档、翻译、无敏感信息的复现材料、公开测试方案、通用 LUT 工具与示例。

不在公开 PR 范围：正式修图引擎、模型权重、训练数据、授权实现、商业风格配方，以及不具备公开许可的素材。

参与本项目即表示你同意遵守 [社区行为准则](./CODE_OF_CONDUCT.md)。
