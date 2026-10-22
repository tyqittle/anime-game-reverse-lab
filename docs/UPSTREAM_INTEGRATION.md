# 实际复用的上游代码（不是“参考链接”）

`third_party/` 通过 Git 子模块 gitlink 引用上游**真实源码**，各固定到明确提交。普通 `git clone` 不下载子模块内容，需要运行 `git submodule update --init`。

| 路径 | 项目 | 固定 commit | 授权 | 已接入用途 |
| --- | --- | --- | --- | --- |
| `third_party/UnityPy` | [K0lb3/UnityPy](https://github.com/K0lb3/UnityPy) | `417d59522a998fdee9a9c2b29fe35f3063222457` | MIT | Python `erlab-unity` 直接调用 `UnityPy.load`、`env.objects`、`parse_as_object` 和 `image.save` |
| `third_party/Grasscutter` | [Grasscutters/Grasscutter](https://github.com/Grasscutters/Grasscutter) | `f373827a83d3e688fd3c6afb1e1c3759ca1d61c9` | AGPL-3.0 | 开放世界二游服务端行为研究源码，非游戏客户端 |
| `third_party/LunarCore` | [Melledy/LunarCore](https://github.com/Melledy/LunarCore) | `04b5de871c62895091c4d65243b2e03997e66f23` | AGPL-3.0 | 回合制二游服务端行为研究源码，非游戏客户端 |
| `third_party/godot-demo-projects` | [godotengine/godot-demo-projects](https://github.com/godotengine/godot-demo-projects) | `b761b4cd5718a7118f2c95eb55f181d0a5f004f1` | MIT（艺术/音乐另核） | 现成可在 Godot 导入的游戏工程：`2d/platformer/project.godot`、`2d/jrpg/project.godot` |

## 真正下载和使用上游

```powershell
git clone https://github.com/tyqittle/anime-game-reverse-lab.git
cd anime-game-reverse-lab
powershell -ExecutionPolicy Bypass -File scripts/setup-upstreams.ps1 -Project all
python -m pip install -e ".[unity]"
erlab-unity inspect "C:\your-own\sample.bundle" --types Texture2D,Sprite
erlab-unity export "C:\your-own\sample.bundle" --out exports/example --types Texture2D,Sprite
```

Mac/Linux：`bash scripts/setup-upstreams.sh all`。独立 Godot 游戏工程使用编辑器导入 `third_party/godot-demo-projects/2d/platformer/project.godot`。

**许可证不能混用：** Grasscutter/LunarCore 为 AGPL-3.0，不复制/重新标注为主仓库 MIT。其代码独立保留原版权和许可证，修改/再发布或经网络提供服务请遵循各自许可证义务。Godot 示例中的音乐/艺术素材可能另有授权，需逐项核实。

**现状边界：** 接入真实源码 ≠ 原神或星穹铁道完整复刻成功。上游可能不支持最新商业版本；这里没有客户端、专有素材、解密密钥、绕过手段，也没有验证完整商业游戏运行。此前 `web/` 自写原型仅历史保留。
