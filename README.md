# 明日方舟风格 PC 离线塔防 · Anime Game Reverse Lab

**[当前可玩工程：arknights_pc/](arknights_pc/README.md)** · **[Windows 便携版构建](../../actions/workflows/arknights-pc-windows.yml)** · **[Godot 实机解析验证](../../actions/workflows/arknights-pc.yml)**

本仓库已经基于 [Quiver/Outpost Assault](https://github.com/quiver-dev/tower-defense-godot4) 的真实 MIT 塔防源码建立了 PC 本地关卡：敌人 AI、寻路、波次、炮塔与投射物来自原项目。增加了干员立绘入口、Q 版 PNG 显示适配、部署点费用与本地通关存档。启动 Windows 便携包不需要官方账号或服务器；第一次可从你已有的 [立绘档案馆](https://github.com/tyqittle/anime-character-archive) 下载芬、能天使、阿米娅三张立绘到本机缓存。

**现阶段是基于开源塔防的可玩改造原型，不是原版明日方舟的 PC 离线客户端。** 未还原官方格子阻挡、技能、关卡、养成和完整 Spine 小人动作，不能冒充原版。GitHub 上不打包商业游戏肖像和 Q 版角色素材。你自己的 Q 版透明 PNG 可通过本地文件导入。

其他研究与历史文件仍保留：
- [《明日方舟》阶段 0 客户端逆向可行性](docs/ARKNIGHTS_PHASE_0.md)
- [现成卫戍协议开源游戏](third_party/Arknights-Stronghold-Protocol)
- [历史 Darknights 服务端研究](third_party/Arknights-Darknights-server)
- [曾经的 Godot JRPG 演示（不是明日方舟）](offline_game/README.md)

开源代码和开源资源遵循各自许可证：本库自有代码 MIT；Quiver 原代码 MIT、其素材 CC BY 4.0；版权归属不同的官方《明日方舟》素材不随本库公开发布。仅用于个人本地研究和非商业用途。
