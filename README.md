# 二次元游戏逆向研究工程 · Anime Game Reverse Lab

**v0.3：重用真实开源工程，而不是从零写一个小游戏。** 当前已经通过 Git 子模块固定引用了 UnityPy、Grasscutter、LunarCore、Godot 官方游戏示例的**实际源码**，并提供真正调用 UnityPy 的资源分析/导出 CLI。

**[游戏对应的现有开源项目](docs/GAME_TO_PROJECT_MAP.md)** · **[真实源码接入与版本](docs/UPSTREAM_INTEGRATION.md)** · **[许可证](docs/OPEN_SOURCE_REFERENCES.md)**

## Windows 快速开始

```powershell
git clone https://github.com/tyqittle/anime-game-reverse-lab.git
cd anime-game-reverse-lab
powershell -ExecutionPolicy Bypass -File scripts/setup-upstreams.ps1 -Project all
python -m pip install -e ".[unity]"
erlab-unity inspect "C:\your-own\file.bundle"
erlab-unity export "C:\your-own\file.bundle" --out exports/example --types Texture2D,Sprite

# 使用 Godot 引擎直接运行已有开源游戏源码（不是本项目自制小游戏）
powershell -ExecutionPolicy Bypass -File scripts/play-upstream-godot.ps1 -Game platformer
```

没有 Godot 时，仍可使用 Python 资源分析工具。普通扫描功能保留：`erlab scan <folder> --out reports/v1.json`、`erlab summary`、`erlab diff`。

| 已集成真实上游 | 用途 | 许可证 |
| --- | --- | --- |
| [UnityPy](https://github.com/K0lb3/UnityPy) | 解析标准 Unity 资产、类型索引、Texture/Sprite/Text 导出 | MIT |
| [Grasscutter](https://github.com/Grasscutters/Grasscutter) | 研究原神相关服务端重实现源码 | AGPL-3.0 |
| [LunarCore](https://github.com/Melledy/LunarCore) | 研究星穹铁道相关服务端重实现源码 | AGPL-3.0 |
| [Godot Demo Projects](https://github.com/godotengine/godot-demo-projects) | 已有的完整平台动作和 JRPG 开源游戏项目 | MIT，个别素材另核 |

**研究边界：** 已接入真实上游源码，不代表已逆向重建完整商业游戏。源码子模块在首次 clone 后需 `git submodule update --init` 才下载；无游戏客户端、私有游戏资源、密钥或绕过手段。商业游戏文件需有权访问且格式能被工具读取。

**原 `web/` 自制动作原型仅为历史保留**，不再将其算作逆向成果。本仓库自有代码为 MIT；各子模块保留各自版权与独立许可证。
