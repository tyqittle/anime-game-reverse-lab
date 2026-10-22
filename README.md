# 二次元游戏逆向研究工程 · Anime Game Reverse Lab

**v0.3：以真实开源项目为核心，而非自己造一个小游戏。** 本仓库通过 Git 子模块固定纳入 UnityPy、Grasscutter、LunarCore 和 Godot Demo Projects 的原始源码；提供 `erlab-unity` 命令直接调用 UnityPy 解读合法取得的本地 Unity 文件。

**[真实上游源码接入与精确 commit](docs/UPSTREAM_INTEGRATION.md)** · **[来源与许可证](docs/OPEN_SOURCE_REFERENCES.md)**

## Windows 从零开始

```powershell
git clone https://github.com/tyqittle/anime-game-reverse-lab.git
cd anime-game-reverse-lab
powershell -ExecutionPolicy Bypass -File scripts/setup-upstreams.ps1 -Project all
python -m pip install -e ".[unity]"
erlab-unity inspect "C:\your-own\file.bundle"
erlab-unity export "C:\your-own\file.bundle" --out exports/example --types Texture2D,Sprite
```

普通资源清单分析仍支持：`erlab scan <folder> --out reports/v1.json`、`erlab summary`、`erlab diff`。

### 实际接入的现成开源项目

| 上游 | 实质接入 | 说明 |
| --- | --- | --- |
| [UnityPy](https://github.com/K0lb3/UnityPy) | **子模块 + pip 运行时实际解析** | Unity 资源类型统计、Sprite/Texture2D/文本导出 |
| [Grasscutter](https://github.com/Grasscutters/Grasscutter) | **完整源码子模块** | 某开放世界二游服务端重实现；AGPL-3.0 |
| [LunarCore](https://github.com/Melledy/LunarCore) | **完整源码子模块** | 某回合制二游服务端重实现；AGPL-3.0 |
| [Godot Demo Projects](https://github.com/godotengine/godot-demo-projects) | **完整源码子模块** | 现成平台动作与 JRPG 游戏项目；MIT，部分素材另核授权 |

**界限：** 已经真正接入上游源码并编写 UnityPy 调用接口；**没有**声称逆向完成任何商业游戏或取得其版权资源。Grasscutter 和 LunarCore 不是完整游戏客户端；运行它们可能需要额外环境及符合使用条款的资源。本仓库不包含商业游戏资源、专有密钥或绕过手段。

## 目录

- `src/erlab/`：清单、指纹、差异比较和 UnityPy 接口
- `third_party/`：**实际源码的固定版本 Git 子模块**，clone 后需初始化
- `games/`：多款商业二游的研究记录（不是游戏资源）
- `docs/`：许可证、证据与规范
- `web/`：此前自行写的动作演示，仅保留历史，不再当作逆向成果

本仓库的 MIT 许可证仅适用于**自有代码与文档**。外部子模块拥有独立版权与许可证。
