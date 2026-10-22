# 离线单机游戏（真正复用已有完整开源游戏）

本工程以 [Godot Foundation / godot-demo-projects/2d/role_playing_game](https://github.com/godotengine/godot-demo-projects/tree/master/2d/role_playing_game) 作为**游戏本体**：地图、人物、NPC 对话、回合制战斗、动画及美术均来自真实上游，而非本项目重新创造的演示小游戏。固定上游 commit：`b761b4cd5718a7118f2c95eb55f181d0a5f004f1`，MIT；其他资产声明遵守上游原许可。

## Windows 快速启动

电脑需安装 Git、Python 3.10+ 和**能打开固定上游项目的 Godot（项目的配置声明 Godot 4.7 开发版本）**。Windows 双击 `scripts/run-offline.cmd`，或者：

```powershell
git clone https://github.com/tyqittle/anime-game-reverse-lab.git
cd anime-game-reverse-lab
powershell -ExecutionPolicy Bypass -File scripts/run-offline.ps1
```

首次会从官方仓库拉取实际的游戏源码；构建器把完整游戏复制至 `offline_game/build/solo_jrpg/`、注入本地存档插件并启动 Godot。想只构建、不运行：传 `-BuildOnly`。Linux/macOS：`bash scripts/run-offline.sh`。

你还可以在 [GitHub Actions](../../actions/workflows/offline-game.yml) 下载最新自动生成的 `OfflineJRPG-Godot-Source` 游戏工程，**这是 Godot 可编辑工程，不是 EXE / APK**，打开时仍需要兼容版本的 Godot。

## 游戏功能

原开源游戏实现的是**有限的 RPG 演示关卡**：WASD / 方向键移动、地图物件交互、NPC 对话和回合制战斗。我们新增：Esc 游戏菜单、F5 手动保存、F9 读取、移动后约每 6 秒自动保存、本地 JSON 存档备份。

存档由 Godot 保存到 `user://offline_game/slot1.json`，无账号、无需远程服务。当前存储地图格子位置和对手战败标记；**不保存战斗进行中的状态**，也不能兼容未经分析的商业手游存档。

源项目不会被修改；生成物可以删除并重新构建。项目中的 `UPSTREAM_LICENSE.md` 保留上游许可证，`OFFLINE_ORIGIN.json` 记录了准确来源及改动。

## 目前无法做的事

尚未给出要复活的“已停服手游”的名称或 APK。当前交付的游戏是**开源 RPG 的单机扩展**，不是商业 APK 的修改版，无法声称实现原游戏登录、关卡、联网协议或专有素材。此轮工具测试不等于对 Godot GUI/Windows EXE/Android APK 的完整实际验收。详见 [阶段 0 可行性报告](../docs/PHASE_0_FEASIBILITY.md)。
