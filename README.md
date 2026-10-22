# 二游逆向研究与离线单机游戏

**当前可交付的游戏：** 基于官方现成 MIT 开源 Godot JRPG 做成可编辑的离线单机工程，不再把自制浏览器原型当作商业二游逆向成果。原开源游戏含地图探索、NPC 对话、回合制战斗及艺术资源；新增本机存档、自动存档、暂停菜单。

**[单机游戏运行说明](offline_game/README.md)** · **[阶段 0 真实可行性报告](docs/PHASE_0_FEASIBILITY.md)** · **[工程验收说明](docs/SINGLE_PLAYER_DELIVERY.md)**

## Windows 开始运行

电脑预先安装 **Git、Python 3.10+ 与支持该上游版本的 Godot**（该固定源码标记 Godot 4.7 开发特性）。克隆仓库后双击 `scripts/run-offline.cmd`，或者：

```powershell
git clone https://github.com/tyqittle/anime-game-reverse-lab.git
cd anime-game-reverse-lab
powershell -ExecutionPolicy Bypass -File scripts/run-offline.ps1
```

脚本自动拉取已固定的 [Godot 官方 JRPG 原游戏源代码](https://github.com/godotengine/godot-demo-projects/tree/master/2d/role_playing_game)，构建 `offline_game/build/solo_jrpg/project.godot`，然后调用 Godot 启动。**需要 Godot，不是双击 HTML 或现成 EXE。** 游戏 F5 存、F9 读、Esc 暂停；本地 JSON 位于 `user://offline_game/slot1.json`，不需要在线账号。

**GitHub Actions** 的 `offline-game` 工作流还会生成名为 `OfflineJRPG-Godot-Source` 的完整、可编辑 Godot 游戏工程工件；它不是打包好的 Windows EXE。

## 已真正复用的公开源码

| 项目 | 实际用途 | 许可证 |
| --- | --- | --- |
| [Godot Demo Projects / Role Playing Game](https://github.com/godotengine/godot-demo-projects) | 单机游戏本体、地图、角色、对话、战斗、美术 | MIT（注意原素材许可说明） |
| [UnityPy](https://github.com/K0lb3/UnityPy) | Unity 文件结构与有权使用的资源导出 | MIT |
| [Grasscutter](https://github.com/Grasscutters/Grasscutter) | 原神相关已有服务端重实现源码研究，不是此次游戏后端 | AGPL-3.0 |
| [LunarCore](https://github.com/Melledy/LunarCore) | 星穹铁道相关已有服务端重实现源码研究 | AGPL-3.0 |

这四个真实仓库已作为固定版本 Git 子模块接入。此前 `web/` 自写的 Project Ember 仅保留历史，不用于离线单机工程。开源游戏的文件版本/许可证见 [上游集成清单](docs/UPSTREAM_INTEGRATION.md)。

## 阶段 0：待获取真实停服手游客户端

```powershell
python -m pip install -e .
erlab-apk "C:\personal\game.apk" --out reports/phase0.json --markdown reports/phase0.md
```

`erlab-apk` 对个人合法持有的 APK 作**只读**、无联网的文件清单/DEX 字符串检查，提取引擎、网络 SDK 和候选域名线索，不修改 APK，也不保证可离线运行。

用户提供的模板中 `{游戏名}` 和 `{APK路径}` 尚未替换，当前没有真实客户端，因此**不能声明已经成功逆向任何商业手游、完成登录、还原协议或导出 Android 单机包**。本仓库自有代码为 MIT，外部开源项目各保留其许可；不提交商用游戏资源、密钥或账号数据。
