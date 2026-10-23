# 明日方舟风格 · Windows PC 离线塔防（首个可玩关卡）

**这是真实开源塔防游戏的改造工程，不是官方明日方舟 APK 或已完成的原版复刻。**

## 已经使用的真正开源源码

- **底座：[Quiver / Outpost Assault](https://github.com/quiver-dev/tower-defense-godot4)**，MIT 许可，固定提交 `1cbd622116dbf5acc0f284f57ece22970338afe8`。
- 复用真实的 **MapTemplate、NavigationAgent、Spawner、TurretSlot、Turret、Shooter、Projectile、Enemy 及 HUD** 模块。
- 新增三职业部署费用映射、本地进度存档、选择界面、头像绑定和战斗 Q 图贴图适配。
- 这是教学原型级的**第一关**。沿用原开源工程的波次/关卡布局和攻击行为；不是原版 1-7 等官方关卡，也未实现官方角色技能、阻挡、养成。

## Windows 操作

**直接玩：** 在 GitHub Actions 的 `arknights-pc-windows-portable` 工作流下载 `Arknights-PC-Offline-Prototype-Windows`，完整解压后双击 `PLAY.cmd`。便携包自带 Godot，不需要安装 Godot/Python/Git。首次运行会尝试从你的立绘仓库下载 3 张立绘到本机，成功后离线运行，且不再重复下载；网络不可用时能用开源工程原有美术先玩。把自己持有的透明 Q 版图片命名为 `slot_0.png`、`slot_1.png`、`slot_2.png` 放进 `game/arknights/assets/chibi/`，再次运行后自动绑定。**注意当前尚不包含由 Spine 骨骼导出的真实战斗 Q 版动画。**

**源码再开发：** 需要 Git、Python 3.10+ 与 Godot 4.7+。

```powershell
git clone https://github.com/tyqittle/anime-game-reverse-lab.git
cd anime-game-reverse-lab
.\scripts\run-arknights-pc.cmd
```

**默认从你的立绘仓库自动下载三张角色立绘到本机**：芬（先锋）、能天使（狙击）、阿米娅（术师）。只在本机第一次构建时下载，运行游戏无需联网。离线构建可传 `-SkipPortraitDownload`；GitHub Actions 构建不包含这些版权图片。也支持传入你现有的完整立绘档案馆：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run-arknights-pc.ps1 -Archive "D:\anime-character-archive" -Chibi "D:\my-arknights-q"
```

`-Archive` 必须是**本机已保存的** `anime-character-archive` 目录，包含 `data/characters.json` 和 `assets/portraits`。脚本仅复制第一批三个不重复的、能找到本地图像的《明日方舟》角色到**本机构建目录**，不推送角色版权图片到公开 GitHub。复制后的真实名字和立绘会显示在主页。

`-Chibi` 指向你拥有的、已经准备好的透明 Q 版角色图片目录，文件名支持 `slot_0.png`、`slot_1.png`、`slot_2.png` 或 `operator_0.png` 等。战斗部署后替换对应三个炮塔的外观层。不包含任何未授权商业素材，也不会把动态**立绘**误当作战斗小人。没有 Q 图时仍能运行上游原始炮塔动画。

## 运行玩法

- 首页展示三个角色卡片（未导入时为职业占位）。
- 点击“开始第一关”进入真实 Quiver 关卡；地图塔位点击安装 Gatling/Single/Missile 炮塔，分别映射先锋/狙击/术师，12/18/23 DP。
- 击杀、导航、敌人波次、弹道均运行原开源代码；DP 逐渐恢复。
- 通关标记和累计完成次数存本机 `user://arknights_td/progress.json`；关卡重开、返回首页可用。
- 后续阶段再将模型、攻击与基于格子的阻挡、朝向及具体干员技能替换为原作风格；不能把当前工程夸大成原版还原完成。

## 来源与版权

Quiver 的**代码是 MIT**，其随项目的**美术、音乐、音效另为 CC BY 4.0**。构建保留 `UPSTREAM_LICENSE.txt` 与 `UPSTREAM_ASSETS_LICENSE.txt` 并注明来源。个人本地导入的明日方舟立绘与战斗 Q 素材，版权不属于 Quiver 或本仓库的 MIT 许可。不要把生成的包含商业游戏素材的构建物上传到 GitHub、公开发行或销售。游戏离线运行，不连接官方账户/服务。
