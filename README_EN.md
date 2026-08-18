<p align="center">
  <img src="./docs/readme/rendered/hero-workstation.webp" alt="Liangzai: local-first event photo retouching with editable AI parameters">
</p>

<p align="center">
  <a href="./README.md">简体中文</a>
  &nbsp;·&nbsp;
  <a href="./README_EN.md"><b>English</b></a>
  &nbsp;·&nbsp;
  <a href="./CHANGELOG.md">Changelog</a>
  &nbsp;·&nbsp;
  <a href="./ROADMAP.md">Roadmap</a>
</p>

<p align="center">
  <a href="https://github.com/18818474455/liangzai/releases"><img src="https://img.shields.io/github/v/release/18818474455/liangzai?display_name=tag&style=flat-square" alt="GitHub release"></a>
  <a href="https://github.com/18818474455/liangzai/actions/workflows/docs.yml"><img src="https://github.com/18818474455/liangzai/actions/workflows/docs.yml/badge.svg" alt="Documentation checks"></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/docs-CC_BY_4.0-2ed8a7?style=flat-square" alt="Documentation license: CC BY 4.0"></a>
  <img src="https://img.shields.io/badge/macOS-Apple_Silicon-111827?style=flat-square&logo=apple" alt="macOS Apple Silicon">
  <img src="https://img.shields.io/badge/Windows-x64-111827?style=flat-square&logo=windows11" alt="Windows x64">
</p>

<p align="center">
  <a href="https://oss.ybpbyxc.com/uploads/2026-08-17/chroma-studio-0.1.19-build27-arm64.dmg"><b>Download for Mac</b></a>
  &nbsp;·&nbsp;
  <a href="https://oss.ybpbyxc.com/uploads/2026-08-15/chroma-studio-0.1.19-build26-x64.exe"><b>Download for Windows</b></a>
  &nbsp;·&nbsp;
  <a href="./docs/readme/media/product-tour-720p.mp4?raw=1">Watch the full product tour</a>
  &nbsp;·&nbsp;
  <a href="#open-components-clear-boundaries">Open components</a>
</p>

> [!IMPORTANT]
> `liangzai` is the product overview and open-source hub for Yunxiangchuan Liangzai. It is not the complete desktop application source. Reusable public components are MIT-licensed, this repository's documentation and technical diagrams are CC BY 4.0, and the production retouching engine, models, and style recipes remain commercial software.

## See the workflow

<p align="center">
  <img src="./assets/feature-tour.gif" alt="A quick tour of the Liangzai event photo retouching workspace">
</p>

Liangzai is a local-first desktop retouching workspace for weddings, conferences, exhibitions, ID photos, and other time-sensitive photography jobs. AI proposes editable settings; the photographer keeps control of the final image.

| Local-first | Editable AI | One workflow |
|:---|:---|:---|
| Decode, analysis, parameter stacks, preview, and export run locally | AI produces visible starting parameters instead of a baked result | Import, select, retouch, batch-sync, and export in one workspace |
| License checks do not upload images; cloud sync is user-initiated | Settings remain adjustable, reversible, and reusable | Stars, flags, color labels, and batch settings never modify the original |

**Import → local analysis → AI starting point → manual refinement → batch sync → local export or optional upload**

## What ships today

- Global tone and color: exposure, highlights, shadows, white balance, HSL, curves, split toning, standard `.cube` LUTs, and more.
- Portrait retouching: skin smoothing, shine and dark-circle reduction, whitening, complexion controls, face and body adjustments, and per-person scopes.
- Local editing: subject, background, sky, skin, lips, and iris masks; brush and gradient masks; color and luminance ranges.
- Image tools: ID-photo background replacement, sky replacement, background cleanup, crop, and rotation.
- Delivery: a notarized Apple Silicon build for macOS and an x64 build for Windows.

The main retouching path runs on the desktop. Network access is limited to licensing and cloud-space operations explicitly initiated by the user. “Local-first” does not mean the application never connects to the network.

## Open components, clear boundaries

### [`liangzai-cube-kit`](https://github.com/18818474455/liangzai-cube-kit) · MIT

An Adobe `.cube` LUT parser, serializer, trilinear interpolator, intensity mixer, and basic color-grading toolkit. Try it in the [browser playground](https://18818474455.github.io/liangzai-cube-kit/).

```bash
npm install liangzai-cube-kit
```

```ts
import { parseCube, applyCubeToRgba8 } from 'liangzai-cube-kit'

const output = applyCubeToRgba8(parseCube(cubeText), rgba8, 0.8)
```

### [`liangzai-plugin-sdk`](https://github.com/18818474455/liangzai-plugin-sdk) · MIT

Public manifest and host types with a runnable Hello example. It documents an interface boundary; the production desktop application does not currently load third-party plugins, and this SDK does not contain the image engine, models, or style LUTs.

### Single-feature algorithm experiments · MIT

These four repositories are early, standalone prototypes for learning and experimentation. They are **not extracted source code from the production retouching engine**, and their quality, robustness, and performance do not represent the shipping Liangzai product.

| Repository | What it demonstrates | Demo |
|:---|:---|:---|
| [Face Blemish Remover](https://github.com/18818474455/face-blemish-remover) | C++ frequency-separation and local-statistics repair with Android/iOS integration examples | Native source |
| [Face Age & Gender Estimation](https://github.com/18818474455/face-age-gender-estimation) | face-api.js face detection and appearance-based age/gender estimates | [GitHub Pages](https://18818474455.github.io/face-age-gender-estimation/) |
| [Body Slimming Demo](https://github.com/18818474455/body-slimming-demo) | BodyPix segmentation and Canvas displacement-field reshaping | [GitHub Pages](https://18818474455.github.io/body-slimming-demo/) |
| [Human Skin-tone Pixel Detection](https://github.com/18818474455/human-skin-tone-detection) | BodyPix-constrained skin-color pixel filtering and local enhancement | [GitHub Pages](https://18818474455.github.io/human-skin-tone-detection/) |

The repositories document privacy, bias, and safety boundaries for appearance-based estimates. None of these demos should be used for identity claims or high-risk decisions.

## Releases and verification

The current public build is `0.1.19`:

| Platform | Build | Distribution | SHA-256 |
|:---|:---|:---|:---|
| macOS · Apple Silicon | 27 | [Notarized DMG](https://oss.ybpbyxc.com/uploads/2026-08-17/chroma-studio-0.1.19-build27-arm64.dmg) | `4f1a24217363e2d861aa13ebe820d7d03850ce58dd94307e47bd39a4b7f09844` |
| Windows · x64 | 26 | [EXE installer](https://oss.ybpbyxc.com/uploads/2026-08-15/chroma-studio-0.1.19-build26-x64.exe) | `8bd82700864ff67baf5cbd5a34db8a903bafa538ba5ba382f870c5e5b9cdb84e` |

The macOS build is signed and notarized. The Windows build is not yet Authenticode-signed, so SmartScreen may warn on first launch. We do not publish speed or accuracy claims until the benchmark method and raw results can be reproduced publicly.

## Follow and contribute

Star the repository if you want release notes, public tests, and updates to the open LUT and plugin tools without joining a marketing group.

- Read the [changelog](./CHANGELOG.md), [public roadmap](./ROADMAP.md), and [contribution guide](./CONTRIBUTING.md).
- Use [Discussions](https://github.com/18818474455/liangzai/discussions) for questions and workflows.
- Report a [reproducible bug](https://github.com/18818474455/liangzai/issues/new?template=bug_report.yml) or propose a [feature](https://github.com/18818474455/liangzai/issues/new?template=feature_request.yml).
- Follow the [security policy](./SECURITY.md) for private vulnerability or privacy reports.

## Contact and license

- Product: [ybpbyxc.com](https://www.ybpbyxc.com)
- Enterprise, OEM, and private deployment: [Enterprise services](https://www.ybpbyxc.com/enterprise.html)
- Email: `007007007@163.com`
- WeChat: `cylbaw`
- WhatsApp: `@biandongdev`
- Company: Changsha Yuebei Pianbei Media Co., Ltd.

Documentation and presentation assets in this repository are licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The MIT licenses for `liangzai-cube-kit` and `liangzai-plugin-sdk` apply only to their respective repositories. The Liangzai desktop application, retouching engine, models, and style recipes are not covered by those licenses.
