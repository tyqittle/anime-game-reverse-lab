# 二游逆向研究工作台 · Anime Game Reverse Lab

> 面向二次元游戏（不是“2D 游戏”）的**模块化、离线、可复现**研究仓库。专注于合法取得的本地资源、文件格式、素材组织、渲染与动画架构研究。

**当前阶段：v0.2 基础工具 + 原创可玩动作验证器**。已实现：文件头识别、资源清单扫描、SHA-256 去重线索、清单摘要、两次扫描差异分析、多游戏档案。未声称已经逆向出任何商业游戏，也不包含原游戏素材、反编译结果或解密密钥。

## 现在就能运行游戏：星烬计划（Project Ember）

**[直接打开离线动作原型](web/index.html)**：双击 `web/index.html`，或启用 GitHub Pages 后在仓库网站玩（无需额外引擎）。

- 可操作原创忍者型角色：移动、二段跳、3 段近战、闪避、飞刃；击败敌人、收集晶体、Boss 战、抵达撤离点。
- 帧率独立物理、分层视差背景、碰撞/命中、屏幕抖动、合成音效、触屏控制。
- 支持导入你有权使用的本地透明 PNG/WebP 替换角色外观，无上传。
- **这属于公开技术参考下的原创游戏重构验证项目，不是任何商业游戏的反编译版本。**

源代码：[`web/`](web/) · [操作说明](web/README.md) · [公开来源与许可证](docs/OPEN_SOURCE_REFERENCES.md)。

## 已可运行

要求：Python 3.10+；核心功能零第三方依赖。

```bash
# 直接运行（不需要安装）
python -m erlab --help     # 需先设置 PYTHONPATH=src；也可按下方安装

# 推荐安装方式：在仓库根目录
python -m pip install -e .
erlab games
erlab inspect path/to/file
# 读取你合法持有的本地样本目录，生成可共享的元数据清单
erlab scan path/to/local/gamefiles --out reports/scan-v1.json
erlab summary reports/scan-v1.json
# 两个版本的目录扫描比较
erlab diff reports/scan-v1.json reports/scan-v2.json --out reports/diff.json
```

**Windows 用户**：将本地样本文件夹拖到 `scripts/scan-windows.cmd` 上，可免安装以系统 Python 完成首次扫描；扫描结果写入 `reports/`。脚本不会上传文件到云端。

## 项目结构

```text
src/erlab/             可测试的核心 CLI 与格式检测库
samples/               你自己的本地游戏文件（Git 忽略，不提交）
games/                 按游戏独立管理的档案，统一结构
reports/               自动生成的扫描报告（Git 忽略）
docs/                  逆向方法、资源安全规范、开发路线
examples/              可公开的演示数据
scripts/               Windows 一键扫描、GitHub 发布辅助
.github/workflows/      CI 自动化单元测试
```

## 支持的研究对象

`games/` 已建立原神、鸣潮、绝区零、蔚蓝档案、胜利女神：妮姬、碧蓝航线的**空白研究档案**，统一字段但不臆测游戏实现细节，未来逐一补充可验证信息。可复制 `games/_template/profile.json` 增加新游戏。

## 工作流

1. 使用自己的合法样本，在本地保存至 `samples/<game-id>/`（这一路径默认不纳入 Git）。
2. `erlab scan` 生成清单：文件相对路径、尺寸、头部格式、SHA-256；不保存文件内容。
3. `erlab summary` 检查格式分布、未知格式数量。
4. 将可公开的**分析结论**整理到对应游戏 `notes.md`；记录来源与证据，区分“已验证”和“待确认”。
5. 对于新增样本，运行 `erlab diff` 比较变更，不重复研究未变更文件。

## 安全与边界

只研究拥有合法访问权的本地样本；不发布商业游戏素材、源码、密钥、凭证、破解工具或能绕过 DRM/反作弊/登录验证的内容；不连接或攻击游戏服务器。请查看 [研究规范](docs/RESEARCH_RULES.md)。

## 现有忍三项目

原有 `ninja-offline-lab` 可保持独立。本仓库以多游戏的素材文件结构和工具共用为目标，不改动原有仓库。

## 版本说明

- v0.2：增加原创可玩的横版动作引擎与 Boss 示例；不依赖商业游戏素材。
- v0.1：离线资源清点 + 基础格式检测 + 摘要/差异比较 + 游戏登记 + 测试。
- 尚未提供各商业游戏完整资产提取器、动态图展示器、反编译功能或商业游戏复刻成品。

MIT 许可证仅适用于**本仓库自创代码和文档**，不授予任何第三方游戏资产使用权。
