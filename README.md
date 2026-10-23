# 明日方舟 Windows 离线研究（目标是原版，不是教程 Demo）

**当前状态：阶段 0 / 开源项目已接入 / 缺少用户本人的 APK 或 PC 客户端样本 / 原版单机化尚未实现。** 请先看 [明日方舟阶段 0 实证可行性报告](docs/ARKNIGHTS_PHASE_0.md)。

2026-10-23 已将真实的开源工程作为固定提交的 Git 子模块接入：
- **[Stronghold Protocol](third_party/Arknights-Stronghold-Protocol)**：可玩《明日方舟》衍生「卫戍协议」单人塔防，GPL-3.0-or-later；**不是原版主线**。
- **[Darknights-server](third_party/Arknights-Darknights-server)**：原版客户端历史服务端模拟项目，Apache-2.0，**不保证支持当前客户端**。
- **[AssetStudioMod](third_party/Arknights-AssetStudioMod)**：Unity 资源研究工具，MIT。

它们是原仓库的真实代码，不是我新写的虚构游戏。以前的 `offline_game/` Godot JRPG 与《明日方舟》**没有关系，仍留在历史目录但不作为本项目的成品**。

## Windows：先运行真正的现成塔防（只是「卫戍协议」）

安装 Git 和 Node.js ≥22，克隆仓库后：

```powershell
git clone https://github.com/tyqittle/anime-game-reverse-lab.git
cd anime-game-reverse-lab
.\scripts\start-arknights-solo.cmd
```

脚本会拉取已固定版本的上游源码、安装依赖并尝试在本机 `http://127.0.0.1:3000` 启动。默认不下载版权美术/音频，可能缺少模型与音效。如果用户有权自行取得并选择下载上游素材：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/start-arknights-solo.ps1 -AllowAssetDownloads
```

这可能让上游执行数百 MB 的素材下载，软件代码 GPL **不代表游戏版权素材有再分发许可**。主仓库不上传它们。

## Windows：原版客户端 APK 只读分析（需你有权使用的 APK）

```powershell
python -m pip install -e .
erlab-apk "C:\path\to\owned\arknights.apk" --out reports/arknights-phase0.json --markdown reports/arknights-phase0.md
```

没有提供 APK，所以现在不能写出真实引擎/保护/域名报告，更不能宣称原版游戏已经无需服务器登录。后续所有修改只作用于复制件，支持差异追踪与撤销。

## 许可证及边界

主仓库自有代码 MIT；每个第三方子模块独立许可证，其中 Stronghold 为 GPL-3.0-or-later，第三方《明日方舟》美术、音频和游戏数据版权不包括在开源许可证内。不上传官方客户端、商业资源、专有密钥和账号；不运营对外私服。
