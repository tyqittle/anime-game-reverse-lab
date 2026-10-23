# 明日方舟风格 · Windows PC 离线塔防（首个可玩关卡）

**这是真实开源塔防游戏的改造工程，不是官方明日方舟 APK 或已完成的原版复刻。**

## 已经使用的真正开源源码

- **底座：[Quiver / Outpost Assault](https://github.com/quiver-dev/tower-defense-godot4)**，MIT 许可，固定提交 `1cbd622116dbf5acc0f284f57ece22970338afe8`。
- 复用真实的 **MapTemplate、NavigationAgent、Spawner、TurretSlot、Turret、Shooter、Projectile、Enemy 及 HUD** 模块。
- 新增三职业部署费用映射、本地进度存档、选择界面、头像绑定和战斗 Q 图贴图适配。
- 这是教学原型级的**第一关**。沿用原开源工程的波次/关卡布局和攻击行为；不是原版 1-7 等官方关卡，也未实现官方角色技能、阻挡、养成。

## Windows 操作

需要 Git、Python 3.10+ 与 Godot 4.7+。也可以直接在本仓库 Actions 的 `arknights-pc-windows` 下载构建好的便携包（若该运行通过）。

```powershell
git clone https://github.com/tyqittle/anime-game-reverse-lab.git
cd anime-game-reverse-lab
.\scripts\run-arknights-pc.cmd
```

**使用你现有的立绘档案馆：**

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

Quiver 项目代码/资产应保留原项目 `LICENSE.txt` 和 `LICENSE_ASSETS.txt`。个人本地导入的明日方舟立绘与战斗 Q 素材，版权不属于 Quiver 或本仓库的 MIT 许可。不要把生成的包含商业游戏素材的构建物上传到 GitHub、公开发行或销售。游戏离线运行，不连接官方账户/服务。
