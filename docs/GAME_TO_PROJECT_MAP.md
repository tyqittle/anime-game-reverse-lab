# 游戏 → 实际可获取的开源工程

> 仅记录**能够核验的开源对应关系**；空白不是遗漏，而是不编造项目、游戏数据或“已支持”的能力。

| 目标 | 可复用的真实项目 | 本仓库位置 | 当前完成度 |
| --- | --- | --- | --- |
| 原神 | [Grasscutter](https://github.com/Grasscutters/Grasscutter) | `third_party/Grasscutter/` | 已固定源码，**未验证**当前版本游戏可运行 |
| 崩坏：星穹铁道 | [LunarCore](https://github.com/Melledy/LunarCore) | `third_party/LunarCore/` | 已固定源码，**未验证**当前版本游戏可运行 |
| 蔚蓝档案 / 碧蓝航线 / 妮姬 / 绝区零 | [UnityPy](https://github.com/K0lb3/UnityPy) | `third_party/UnityPy/` + `erlab-unity` | 仅标准、可读取的 Unity 资源解析；各游戏专有容器支持**尚未证实** |
| 鸣潮 | 无已验证的兼容引擎适配器 | `games/wuthering-waves/` | 待调研，不能把 UnityPy 错当作通用 Unreal 解析器 |
| 开源游戏样例（非商业二游） | [Godot 官方 Platformer/JRPG](https://github.com/godotengine/godot-demo-projects) | `third_party/godot-demo-projects/2d/` | 可直接用 Godot 打开完整已有工程，不从零造小游戏 |

## 启动真正开源游戏示例

```powershell
git submodule update --init -- third_party/godot-demo-projects
powershell -ExecutionPolicy Bypass -File scripts/play-upstream-godot.ps1 -Game platformer
# 可选 jrpg:  -Game jrpg
```

需要系统已安装 Godot 兼容版本；启动脚本只调用**已有上游项目**的 `project.godot`。不会自动连接任何商业游戏服务。
