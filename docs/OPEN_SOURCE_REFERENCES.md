# 公开项目与素材来源（2026-10-23 校验）

| 项目 | 类型 | 授权 | 在本仓库的用途 | 官方地址 |
| --- | --- | --- | --- | --- |
| Godot Demo Projects | 开源游戏示例 | MIT | 参考可移植的 2D 平台动作物理、摄像机、关卡结构方案。**未复制其源码** | https://github.com/godotengine/godot-demo-projects |
| Godot 2D Platformer | 平台动作完整示范 | MIT（须核对每份附加资产） | 参考角色移动、跳跃、碰撞、投射物、敌人和关卡分层 | https://github.com/godotengine/godot-demo-projects/tree/master/2d/platformer |
| UnityPy | Unity 资源分析库 | MIT | 后续可选的**只读**本地资源类型与结构识别适配器，不默认安装 | https://github.com/K0lb3/UnityPy |
| Kenney New Platformer Pack | 开放素材包 | CC0 | 可由用户自行取得并导入获授权的 PNG/WebP；仓库默认没有再分发此素材包 | https://kenney.nl/assets/new-platformer-pack |

## 已真正实现的范围

- 公开技术路线被用来确定独立的模块接口；`web/js/engine.js`、`web/js/levels.js` 等是本项目自行编写，图像由 Canvas 代码实时绘制。
- 默认网页不引用第三方 CDN、不连原游戏服务器、不要求游戏客户端，也不会从其他游戏盗取资产。
- `games/` 是对商业二次元游戏的研究资料登记，而 `web/` 是**原创可玩验证关卡**；两者不应混淆为商业游戏的反编译/还原成果。
- 若今后真正复用某开源仓库代码，必须固定上游提交、保留版权声明/许可证，列明修改范围，而不仅仅贴一个链接。
- 若今后导入 Kenney 等素材，单独登记素材来源、许可证、下载时间、原始文件 SHA-256；任何“网上能下载”不等于“可以发布”。
