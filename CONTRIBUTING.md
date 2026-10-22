# 贡献指南

尽量提交**工具逻辑与可复现验证**，而不是缺来源的大批未知二进制文件。

```bash
python -m unittest discover -s tests -v
```

对新增游戏：复制 `games/_template/profile.json`，修改 id/name，新增同目录 notes.md 并登记证据与版本。对新增格式：优先增加 `src/erlab/formats.py` 可验证的魔数检测及自制测试数据；扩展名只能作为候选线索。

严禁提交原游戏素材、私人数据、密钥或未获授权的反编译代码。遵守 `docs/RESEARCH_RULES.md`。
