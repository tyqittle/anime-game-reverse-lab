# 单机工程构建/验收说明

基底：Godot Foundation [官方 2D Role Playing Game 示例](https://github.com/godotengine/godot-demo-projects/tree/master/2d/role_playing_game)，精确上游提交 `b761b4cd5718a7118f2c95eb55f181d0a5f004f1`。

真实上游提供 `game.tscn`（游戏）、`grid_movement/exploration.tscn`（地图）、`combat/combat.tscn`（战斗）、`dialogue/` 与图像素材。构建器仅增加 `addons/offline_mode/offline_manager.gd` Autoload，修改应用显示名；附加 `UPSTREAM_LICENSE.md` 和 `OFFLINE_ORIGIN.json` 溯源文件。

| 验收维度 | 状态 |
| --- | --- |
| 原始项目真实来源/版本 | 已核实 GitHub 上游和固定提交 |
| 构建器对模拟上游源码测试 | 已通过 |
| 阶段 0 APK 探测器合成文件单元测试 | 已通过 |
| GitHub Actions 克隆上游/构建并上传游戏工程 | 由 `.github/workflows/offline-game.yml` 验证 |
| Godot 引擎内完整 GUI / 战斗 / 重新进入存档 | **尚未在此环境实际运行** |
| Windows .exe / Android APK | **尚未导出** |
| 未知停服游戏客户端离线化 | **不可评估：缺游戏名称和真实 APK** |

**风险：** 上游示例 `project.godot` 标记 Godot 4.7 开发特性版本，可能需要 Godot 4.7 对应编辑器；使用旧稳定版不保证兼容。原开源示例只有示范内容，未扩建为长剧情商业游戏。

**回滚：** 原始上游子模块不改动；删除 `offline_game/build/solo_jrpg` 后可以重建。存档独立保存在 Godot 的 `user://offline_game/`，如需重置请单独备份或删除其中 JSON。
